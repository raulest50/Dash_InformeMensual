from __future__ import annotations

import json
import math
import re
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from matplotlib.path import Path as MplPath


APP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = APP_DIR / "data" / "municipal_maps"
AGGREGATED_PARQUET = DATA_DIR / "municipal_fuel_consumption.parquet"
GEOJSON_PATH = DATA_DIR / "colombiaMod_v4.json"

PRODUCT_LABELS = {
    "GASOLINA MOTOR CORRIENTE": "Gasolina motor corriente",
    "GASOLINA MOTOR EXTRA": "Gasolina motor extra",
    "BIODIESEL CON MEZCLA": "Diesel / biodiesel con mezcla",
}

ZERO_FILL_COLOR = "#eeeeee"
DEPARTMENT_BOUNDARY_COLOR = "#0B3D91"
DEPARTMENT_BOUNDARY_SAMPLE_OFFSET = 0.0005
SEGMENT_ROUND_DIGITS = 8
MAP_CENTER = {"lat": 4.5709, "lon": -74.2973}

MAP_COLORSCALE = [
    [0.0, ZERO_FILL_COLOR],
    [0.001, "#fff7ec"],
    [0.2, "#fee8c8"],
    [0.4, "#fdbb84"],
    [0.6, "#fc8d59"],
    [0.8, "#e34a33"],
    [1.0, "#b30000"],
]


def compact_key(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    text = str(value).strip().upper()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    return re.sub(r"[^A-Z0-9]", "", text)


def pair_key(departamento: object, municipio: object) -> str:
    return f"{compact_key(departamento)}|{compact_key(municipio)}"


@lru_cache(maxsize=1)
def load_consumption_data() -> pd.DataFrame:
    return pd.read_parquet(AGGREGATED_PARQUET, engine="pyarrow")


@lru_cache(maxsize=1)
def load_geojson() -> dict[str, Any]:
    with GEOJSON_PATH.open("r", encoding="utf-8") as file:
        geojson = json.load(file)

    for feature in geojson.get("features", []):
        props = feature.setdefault("properties", {})
        props["pair_key"] = pair_key(props.get("NAME_1"), props.get("NAME_2"))

    return geojson


def product_options() -> list[dict[str, str]]:
    products = sorted(load_consumption_data()["producto"].dropna().unique())
    return [{"label": PRODUCT_LABELS.get(product, product), "value": product} for product in products]


def year_options() -> list[dict[str, int]]:
    years = sorted(load_consumption_data()["anio_despacho"].dropna().astype(int).unique())
    return [{"label": str(year), "value": int(year)} for year in years]


def default_year() -> int:
    options = year_options()
    return int(options[-1]["value"])


def month_options(year: int) -> list[dict[str, str | int]]:
    df = load_consumption_data()
    months = (
        df.loc[df["anio_despacho"] == year, "mes_despacho"]
        .dropna()
        .astype(int)
        .drop_duplicates()
        .sort_values()
        .tolist()
    )
    return [{"label": "Todos", "value": "all"}] + [
        {"label": f"{month:02d}", "value": int(month)} for month in months
    ]


def _filter_consumption(product: str, year: int | None, month: int | None) -> pd.DataFrame:
    df = load_consumption_data()
    filtered = df[df["producto"] == product].copy()

    if year is not None:
        filtered = filtered[filtered["anio_despacho"] == year]
    if month is not None:
        filtered = filtered[filtered["mes_despacho"] == month]
    if filtered.empty:
        return pd.DataFrame()

    municipal = (
        filtered.groupby(
            [
                "departamento",
                "municipio",
                "pair_key",
                "in_geojson",
                "geojson_feature_index",
                "gid_2",
                "type_2",
            ],
            as_index=False,
            dropna=False,
        )
        .agg(
            volumen_total=("volumen_total", "sum"),
            registros=("registros", "sum"),
            has_observed_record=("has_observed_record", "max"),
        )
        .sort_values(["departamento", "municipio"])
        .reset_index(drop=True)
    )

    total = municipal["volumen_total"].sum()
    municipal["participacion_pct"] = 0.0 if total <= 0 else municipal["volumen_total"] / total * 100
    municipal["data_status"] = "observed"
    municipal.loc[
        ~municipal["has_observed_record"] & municipal["in_geojson"],
        "data_status",
    ] = "zero_filled_geojson"
    municipal.loc[
        ~municipal["has_observed_record"] & ~municipal["in_geojson"],
        "data_status",
    ] = "zero_filled_vmensual_no_geometry"
    return municipal


def selected_period_label(year: int | None, month: int | None) -> str:
    if year is None:
        return "todo el periodo"
    if month is None:
        return str(year)
    return f"{year}-{month:02d}"


def iter_polygon_rings(geometry: dict[str, Any]) -> Iterable[list[list[float]]]:
    geom_type = geometry.get("type")
    coordinates = geometry.get("coordinates", [])
    if geom_type == "Polygon":
        yield from coordinates
    elif geom_type == "MultiPolygon":
        for polygon in coordinates:
            yield from polygon


def iter_polygons(geometry: dict[str, Any]) -> Iterable[list[list[list[float]]]]:
    geom_type = geometry.get("type")
    coordinates = geometry.get("coordinates", [])
    if geom_type == "Polygon":
        yield coordinates
    elif geom_type == "MultiPolygon":
        yield from coordinates


def iter_ring_segments(
    ring: list[list[float]],
) -> Iterable[tuple[tuple[float, float], tuple[float, float]]]:
    points = [(float(point[0]), float(point[1])) for point in ring if len(point) >= 2]
    if len(points) < 2:
        return
    if points[0] != points[-1]:
        points = points + [points[0]]

    for start, end in zip(points, points[1:]):
        if start != end:
            yield start, end


def rounded_point(point: tuple[float, float]) -> tuple[float, float]:
    return (
        round(point[0], SEGMENT_ROUND_DIGITS),
        round(point[1], SEGMENT_ROUND_DIGITS),
    )


def segment_key(
    start: tuple[float, float],
    end: tuple[float, float],
) -> tuple[tuple[float, float], tuple[float, float]]:
    return tuple(sorted((rounded_point(start), rounded_point(end))))  # type: ignore[return-value]


def ring_to_path(ring: list[list[float]]) -> MplPath | None:
    points = [(float(point[0]), float(point[1])) for point in ring if len(point) >= 2]
    if len(points) < 3:
        return None
    if points[0] != points[-1]:
        points.append(points[0])
    codes = [MplPath.MOVETO] + [MplPath.LINETO] * (len(points) - 2) + [MplPath.CLOSEPOLY]
    return MplPath(points, codes)


def ring_bounds(ring: list[list[float]]) -> tuple[float, float, float, float] | None:
    points = [(float(point[0]), float(point[1])) for point in ring if len(point) >= 2]
    if not points:
        return None
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return min(xs), min(ys), max(xs), max(ys)


def build_department_shapes(features: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    department_shapes: dict[str, list[dict[str, Any]]] = {}
    for feature in features:
        props = feature.get("properties") or {}
        department = props.get("NAME_1")
        if not department:
            continue
        geometry = feature.get("geometry") or {}
        for polygon in iter_polygons(geometry):
            if not polygon:
                continue
            exterior = ring_to_path(polygon[0])
            bounds = ring_bounds(polygon[0])
            if exterior is None or bounds is None:
                continue
            holes = [
                hole_path
                for ring in polygon[1:]
                if (hole_path := ring_to_path(ring)) is not None
            ]
            department_shapes.setdefault(str(department), []).append(
                {"bounds": bounds, "exterior": exterior, "holes": holes}
            )
    return department_shapes


def point_in_department(point: tuple[float, float], shapes: list[dict[str, Any]]) -> bool:
    x, y = point
    for shape in shapes:
        min_x, min_y, max_x, max_y = shape["bounds"]
        if x < min_x or x > max_x or y < min_y or y > max_y:
            continue
        if not shape["exterior"].contains_point(point):
            continue
        if any(hole.contains_point(point) for hole in shape["holes"]):
            continue
        return True
    return False


def segment_sample_points(
    start: tuple[float, float],
    end: tuple[float, float],
) -> tuple[tuple[float, float], tuple[float, float]] | None:
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return None

    offset = min(DEPARTMENT_BOUNDARY_SAMPLE_OFFSET, length * 0.25)
    normal_x = -dy / length
    normal_y = dx / length
    mid_x = (start[0] + end[0]) / 2
    mid_y = (start[1] + end[1]) / 2
    return (
        (mid_x + normal_x * offset, mid_y + normal_y * offset),
        (mid_x - normal_x * offset, mid_y - normal_y * offset),
    )


@lru_cache(maxsize=1)
def department_boundary_lon_lat() -> tuple[list[float | None], list[float | None]]:
    features = load_geojson().get("features", [])
    department_shapes = build_department_shapes(features)
    boundary_segments: dict[
        tuple[tuple[float, float], tuple[float, float]],
        tuple[tuple[float, float], tuple[float, float]],
    ] = {}

    for feature in features:
        props = feature.get("properties") or {}
        department = props.get("NAME_1")
        if not department:
            continue
        shapes = department_shapes.get(str(department), [])
        geometry = feature.get("geometry") or {}
        for ring in iter_polygon_rings(geometry):
            for start, end in iter_ring_segments(ring):
                key = segment_key(start, end)
                if key[0] == key[1]:
                    continue
                sample_points = segment_sample_points(start, end)
                if sample_points is None:
                    continue
                first_point, second_point = sample_points
                if point_in_department(first_point, shapes) and point_in_department(
                    second_point,
                    shapes,
                ):
                    continue
                boundary_segments.setdefault(key, (start, end))

    lon: list[float | None] = []
    lat: list[float | None] = []
    for start, end in boundary_segments.values():
        lon.extend([start[0], end[0], None])
        lat.extend([start[1], end[1], None])
    return lon, lat


def empty_figure(message: str) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        height=320,
        margin={"r": 10, "t": 30, "l": 10, "b": 10},
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[
            {
                "text": message,
                "xref": "paper",
                "yref": "paper",
                "x": 0.5,
                "y": 0.5,
                "showarrow": False,
                "font": {"size": 15},
            }
        ],
    )
    return fig


def make_map_figure(
    product: str,
    year: int | None,
    month: int | None,
    scale: str = "log",
) -> tuple[go.Figure, dict[str, int | float]]:
    municipal = _filter_consumption(product, year, month)
    if municipal.empty:
        return empty_figure("No hay datos para el filtro seleccionado."), {}

    for_map = municipal[municipal["in_geojson"]].copy()
    if scale == "linear":
        for_map["color_value"] = for_map["volumen_total"]
        colorbar_title = "Volumen"
    else:
        for_map["color_value"] = np.log10(for_map["volumen_total"] + 1)
        colorbar_title = "log10(volumen + 1)"

    zmax = float(for_map["color_value"].max())
    if zmax <= 0:
        zmax = 1.0

    customdata = for_map[
        [
            "departamento",
            "municipio",
            "volumen_total",
            "registros",
            "data_status",
            "participacion_pct",
            "pair_key",
        ]
    ].to_numpy()

    fig = go.Figure()
    fig.add_trace(
        go.Choroplethmap(
            geojson=load_geojson(),
            locations=for_map["pair_key"],
            z=for_map["color_value"],
            featureidkey="properties.pair_key",
            colorscale=MAP_COLORSCALE,
            zmin=0,
            zmax=zmax,
            marker={
                "opacity": 0.86,
                "line": {"width": 0.35, "color": "#ffffff"},
            },
            customdata=customdata,
            hovertemplate=(
                "<b>%{customdata[1]}</b><br>"
                "%{customdata[0]}<br>"
                "Volumen: %{customdata[2]:,.0f}<br>"
                "Participacion: %{customdata[5]:.3f}%<br>"
                "Registros: %{customdata[3]:,.0f}<br>"
                "Estado: %{customdata[4]}"
                "<extra></extra>"
            ),
            colorbar={"title": colorbar_title, "thickness": 14},
        )
    )

    dept_lon, dept_lat = department_boundary_lon_lat()
    fig.add_trace(
        go.Scattermap(
            lon=dept_lon,
            lat=dept_lat,
            mode="lines",
            line={"color": DEPARTMENT_BOUNDARY_COLOR, "width": 1.2},
            hoverinfo="skip",
            showlegend=False,
        )
    )

    period = selected_period_label(year, month)
    product_label = PRODUCT_LABELS.get(product, product)
    fig.update_layout(
        title=f"{product_label} por municipio ({period})",
        map={"style": "carto-positron", "center": MAP_CENTER, "zoom": 4.2},
        height=700,
        margin={"r": 0, "t": 45, "l": 0, "b": 0},
        uirevision="municipal-consumption-map",
    )

    summary = {
        "total_volume": float(municipal["volumen_total"].sum()),
        "mapped_municipalities": int(for_map.shape[0]),
        "observed_municipalities": int(municipal["has_observed_record"].sum()),
        "zero_filled_municipalities": int((~municipal["has_observed_record"]).sum()),
        "without_geometry": int((~municipal["in_geojson"]).sum()),
    }
    return fig, summary


def get_pair_from_click(click_data: dict[str, Any] | None) -> str | None:
    if not click_data:
        return None
    points = click_data.get("points") or []
    if not points:
        return None
    point = points[0]
    if point.get("location"):
        return str(point["location"])
    customdata = point.get("customdata")
    if isinstance(customdata, list) and len(customdata) >= 7:
        return str(customdata[6])
    return None


def municipality_label(pair: str | None) -> str:
    if not pair:
        return "Municipio seleccionado"
    df = load_consumption_data()
    rows = df.loc[df["pair_key"] == pair, ["departamento", "municipio"]].drop_duplicates()
    if rows.empty:
        return "Municipio seleccionado"
    row = rows.iloc[0]
    return f"{row['municipio']} | {row['departamento']}"


def make_timeseries_figure(pair: str | None, product: str) -> go.Figure:
    if not pair:
        return empty_figure("Seleccione un municipio en el mapa.")

    df = load_consumption_data()
    global_periods = pd.to_datetime(
        {
            "year": df["anio_despacho"].astype(int),
            "month": df["mes_despacho"].astype(int),
            "day": 1,
        }
    )
    last_global_month = global_periods.max()

    selected = df[(df["pair_key"] == pair) & (df["producto"] == product)].copy()
    if selected.empty:
        return empty_figure("No hay serie disponible para el municipio seleccionado.")

    selected["fecha"] = pd.to_datetime(
        {
            "year": selected["anio_despacho"].astype(int),
            "month": selected["mes_despacho"].astype(int),
            "day": 1,
        }
    )
    selected = selected[selected["fecha"] < last_global_month].copy()
    if selected.empty:
        return empty_figure("No hay serie completa disponible antes del ultimo mes.")

    selected = selected.sort_values("fecha")

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=selected["fecha"],
            y=selected["volumen_total"],
            mode="lines+markers",
            line={"color": "#0D6ABF", "width": 2},
            marker={"size": 5},
            customdata=selected[["data_status", "registros"]].to_numpy(),
            hovertemplate=(
                "%{x|%Y-%m}<br>"
                "Volumen: %{y:,.0f}<br>"
                "Registros: %{customdata[1]:,.0f}<br>"
                "Estado: %{customdata[0]}"
                "<extra></extra>"
            ),
        )
    )
    fig.update_layout(
        height=320,
        margin={"r": 10, "t": 25, "l": 55, "b": 45},
        yaxis_title="Volumen",
        xaxis_title="Mes",
        hovermode="x unified",
    )
    return fig


def top_municipalities(product: str, year: int | None, month: int | None, limit: int = 10) -> list[dict[str, Any]]:
    municipal = _filter_consumption(product, year, month)
    if municipal.empty:
        return []
    top = municipal.sort_values("volumen_total", ascending=False).head(limit).copy()
    top["volumen_total"] = top["volumen_total"].round(0).astype("int64")
    top["participacion_pct"] = top["participacion_pct"].round(3)
    return top[["departamento", "municipio", "volumen_total", "participacion_pct"]].to_dict("records")
