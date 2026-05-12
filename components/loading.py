from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import dcc, html


def loading_overlay(
    children: Any,
    loading_id: str,
    target_components: dict[str, str | list[str]] | None = None,
    message: str = "Procesando informaci\u00f3n...",
    spinner_color: str = "success",
    spinner_size: str = "md",
) -> dcc.Loading:
    """Return a reusable loading overlay for callback-driven content."""
    spinner = html.Div(
        [
            dbc.Spinner(color=spinner_color, size=spinner_size, type="border"),
            html.Div(
                message,
                style={
                    "fontFamily": "'Plus Jakarta Sans', sans-serif",
                    "fontSize": "0.95rem",
                    "fontWeight": "600",
                    "color": "#333",
                },
            ),
        ],
        style={
            "alignItems": "center",
            "display": "flex",
            "flexDirection": "column",
            "gap": "0.6rem",
            "justifyContent": "center",
            "padding": "1rem",
        },
    )

    return dcc.Loading(
        id=loading_id,
        children=children,
        custom_spinner=spinner,
        delay_hide=250,
        delay_show=250,
        fullscreen=False,
        overlay_style={
            "backgroundColor": "rgba(255, 255, 255, 0.72)",
            "filter": "blur(1px)",
            "visibility": "visible",
        },
        parent_style={"position": "relative"},
        show_initially=False,
        target_components=target_components,
    )
