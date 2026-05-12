import dash
from dash import html


def brand_logo():
    return html.Img(
        src=dash.get_asset_url("logoComce.png"),
        alt="COMCE-SOLDICOM",
        className="comce-logo",
    )
