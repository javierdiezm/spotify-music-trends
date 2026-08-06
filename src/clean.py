import json
import pandas as pd

RUTA_ENTRADA = "data/raw/artistas_espanoles.json"
RUTA_SALIDA = "data/processed/discografia_artistas_es.csv"

def cargar_datos_crudos():
    with open(RUTA_ENTRADA, "r", encoding="utf-8") as f:
        return json.load(f)

def aplanar_a_filas(datos_artistas):
    """Convierte la estructura anidada (artista -> lista de álbumes) en filas planas (una por álbum)."""
    filas = []
    for artista in datos_artistas:
        for album in artista["discografia"]:
            filas.append({
                "artista": artista["nombre"],
                "album": album["nombre"],
                "tipo": album["tipo"],
                "fecha_lanzamiento": album["fecha_lanzamiento"],
                "precision_fecha": album["precision_fecha"],
                "total_tracks": album["total_tracks"],
            })
    return pd.DataFrame(filas)

def parsear_fechas(df):
    """
    Convierte fecha_lanzamiento a datetime, respetando la precisión real.
    Cuando solo hay año o año-mes, pandas completa con 01 de enero / día 01 —
    lo hacemos explícito en vez de dejar que falle silenciosamente.
    """
    df["fecha_lanzamiento"] = pd.to_datetime(df["fecha_lanzamiento"], format="mixed")
    df["anio"] = df["fecha_lanzamiento"].dt.year
    return df

def eliminar_duplicados(df):
    """
    Un mismo álbum puede aparecer varias veces (remasters, ediciones por mercado).
    Nos quedamos con una fila por combinación artista+álbum+año,
    priorizando la que tenga más tracks (suele ser la edición "completa").
    """
    antes = len(df)
    df = df.sort_values("total_tracks", ascending=False)
    df = df.drop_duplicates(subset=["artista", "album", "anio"], keep="first")
    despues = len(df)
    print(f"Duplicados eliminados: {antes - despues} filas ({antes} → {despues})")
    return df

def resumen_calidad(df):
    """Imprime un resumen rápido para detectar problemas antes de pasar a Power BI."""
    print("\n--- Resumen de calidad ---")
    print(f"Total de filas (álbumes/singles): {len(df)}")
    print(f"Artistas únicos: {df['artista'].nunique()}")
    print(f"Rango de años: {df['anio'].min()} - {df['anio'].max()}")
    print(f"Tipos de lanzamiento: {df['tipo'].value_counts().to_dict()}")
    sin_tracks = (df["total_tracks"] == 0).sum()
    if sin_tracks:
        print(f"⚠️  {sin_tracks} álbumes con total_tracks = 0 (revisar)")

def main():
    datos = cargar_datos_crudos()
    df = aplanar_a_filas(datos)
    df = parsear_fechas(df)
    df = eliminar_duplicados(df)
    df = df.sort_values(["artista", "fecha_lanzamiento"])

    resumen_calidad(df)

    df.to_csv(RUTA_SALIDA, index=False, encoding="utf-8-sig")
    print(f"\n✅ Guardado en {RUTA_SALIDA}")

if __name__ == "__main__":
    main()