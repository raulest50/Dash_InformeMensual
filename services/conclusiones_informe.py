from datetime import datetime

import pandas as pd

from services.informe_mensual_data import get_vmensual
from services.general import P1, P2, P3
from Constants import get_mes_name


NOMBRES_PRODUCTO = {
    P1: "gasolina corriente",
    P2: "ACPM",
    P3: "gasolina extra",
}


def _calificar_variacion(pct: float) -> str:
    """Devuelve un adjetivo de magnitud según el valor absoluto de la variación."""
    abs_pct = abs(pct)
    if abs_pct < 1:
        return "leve"
    if abs_pct < 3:
        return "moderada"
    if abs_pct < 10:
        return ""
    return "significativa"


def _describir_variacion(producto_key: str, pct: float, mes_nombre: str, anio_anterior: int) -> str:
    """Genera la frase descriptiva de variación para un producto."""
    nombre = NOMBRES_PRODUCTO[producto_key]
    calificador = _calificar_variacion(pct)
    pct_fmt = f"{abs(pct):.2f}".replace(".", ",")

    if pct < 0:
        direccion = "una disminución"
        if calificador:
            direccion = f"una disminución {calificador}"
    else:
        direccion = "un incremento"
        if calificador:
            direccion = f"un incremento {calificador}"

    return (
        f"{direccion} del {pct_fmt}% en las ventas de {nombre} "
        f"respecto a {mes_nombre.lower()} de {anio_anterior}"
    )


def _detectar_mes_informe(df: pd.DataFrame) -> tuple[int, int]:
    """
    Determina el mes del informe a partir de los datos.
    Si el mes más reciente en los datos coincide con el mes calendario actual,
    retrocede un mes (datos posiblemente incompletos).
    Retorna (anio, mes).
    """
    df["anio_despacho"] = pd.to_numeric(df["anio_despacho"], errors="coerce")
    df["mes_despacho"] = pd.to_numeric(df["mes_despacho"], errors="coerce")

    fechas = (
        df.groupby(["anio_despacho", "mes_despacho"])
        .size()
        .reset_index(name="n")
    )
    fechas = fechas.sort_values(["anio_despacho", "mes_despacho"])
    ultimo = fechas.iloc[-1]
    anio_max, mes_max = int(ultimo["anio_despacho"]), int(ultimo["mes_despacho"])

    hoy = datetime.now()
    if anio_max == hoy.year and mes_max == hoy.month:
        if mes_max == 1:
            return anio_max - 1, 12
        return anio_max, mes_max - 1

    return anio_max, mes_max


def _calcular_variaciones(df: pd.DataFrame, anio: int, mes: int) -> dict[str, float]:
    """
    Calcula la variación interanual (YoY) del volumen total para cada producto
    en el mes indicado: compara `anio` vs `anio - 1`.
    """
    g = (
        df.groupby(["anio_despacho", "mes_despacho", "producto"])["volumen_total"]
        .sum()
        .reset_index()
    )
    g["volumen_total"] = g["volumen_total"].astype(float)
    mes_df = g[g["mes_despacho"] == mes]

    variaciones = {}
    for prod in [P1, P2, P3]:
        prod_df = mes_df[mes_df["producto"] == prod]
        vol_actual = prod_df.loc[prod_df["anio_despacho"] == anio, "volumen_total"]
        vol_anterior = prod_df.loc[prod_df["anio_despacho"] == anio - 1, "volumen_total"]

        if vol_actual.empty or vol_anterior.empty or float(vol_anterior.iloc[0]) == 0:
            variaciones[prod] = 0.0
        else:
            variaciones[prod] = (
                (float(vol_actual.iloc[0]) - float(vol_anterior.iloc[0]))
                / float(vol_anterior.iloc[0])
                * 100
            )

    return variaciones


def generar_conclusiones(df: pd.DataFrame) -> dict:
    """
    Punto de entrada principal: a partir del DataFrame de vmensual genera
    todas las cadenas de texto del resumen ejecutivo.
    """
    anio, mes = _detectar_mes_informe(df)
    variaciones = _calcular_variaciones(df, anio, mes)

    mes_nombre = get_mes_name(mes)
    anio_anterior = anio - 1
    hoy = datetime.now()
    dia_hoy = f"{hoy.day:02d}"
    mes_elab_nombre = get_mes_name(hoy.month)

    desc_corriente = _describir_variacion(P1, variaciones[P1], mes_nombre, anio_anterior)
    desc_acpm = _describir_variacion(P2, variaciones[P2], mes_nombre, anio_anterior)
    desc_extra = _describir_variacion(P3, variaciones[P3], mes_nombre, anio_anterior)

    texto = (
        f"Reporte mensual de la variación de ventas {mes_nombre.lower()} {anio} "
        f"(conclusión generada el {dia_hoy} de {mes_elab_nombre.lower()} de {hoy.year}): "
        f"El informe mensual refleja {desc_corriente}. "
        f"En el caso del ACPM, se reporta {desc_acpm}. "
        f"Por su parte, se observa {desc_extra}."
    )

    titulo = f"RESUMEN EJECUTIVO INFORME MENSUAL DE VENTAS {mes_nombre.upper()} {anio}"
    subtitulo = f"Reporte mensual de la variación de ventas {mes_nombre.upper()} {anio}:"

    return {
        "mes_informe": mes_nombre,
        "anio_informe": anio,
        "titulo_resumen": titulo,
        "subtitulo_variacion": subtitulo,
        "texto_conclusiones": texto,
    }


_df = get_vmensual()
_resultado = generar_conclusiones(_df)

mes_informe: str = _resultado["mes_informe"]
anio_informe: int = _resultado["anio_informe"]
titulo_resumen: str = _resultado["titulo_resumen"]
subtitulo_variacion: str = _resultado["subtitulo_variacion"]
texto_conclusiones: str = _resultado["texto_conclusiones"]
