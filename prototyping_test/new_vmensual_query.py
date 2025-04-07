

P1 = "GASOLINA CORRIENTE"
P2 = "ACPM"
P3 = "GASOLINA EXTRA"

C1 = "COMERCIALIZADOR INDUSTRIAL"
C2 = "ESTACION DE SERVICIO AUTOMOTRIZ"
C3 = "ESTACION DE SERVICIO FLUVIAL"






def get_query_vmensual():
    query = (
        f"SELECT SUM(volumen_despachado) as volumen_total, anio_despacho, mes_despacho, producto, municipio "
        f"WHERE subtipo_comprador IN ('{C1}', '{C2}', '{C3}') "
        f"AND producto IN ('{P1}', '{P2}', '{P3}') "
        f"GROUP BY anio_despacho, mes_despacho, producto, municipio "
        f"ORDER BY anio_despacho ASC "
        f"LIMIT 250000"
    )