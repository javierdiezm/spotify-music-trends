# src/extract.py
import json
import os
import time
import random
from config import get_spotify_client
from spotipy.exceptions import SpotifyException

ARTISTAS_ESPANOLES = [
    "El Canto del Loco", "Arde Bogotá", "Leiva", "Los Secretos", "Hombres G",
    "Loquillo", "La Maravillosa Orquesta del Alcohol", "Vetusta Morla",
    "Carolina Durante", "Love of Lesbian", "Izal", "Ultraligera", "Sidonie",
    "Viva Suecia", "La Oreja de Van Gogh", "Melendi", "Dorian", "Lori Meyers",
    "Estopa", "Extremoduro", "La Habitación Roja", "La Fuga"
]

RUTA_SALIDA = "data/raw/artistas_espanoles.json"

def cargar_progreso():
    """Carga lo ya extraído, si existe, para no repetir llamadas gastadas."""
    if os.path.exists(RUTA_SALIDA):
        with open(RUTA_SALIDA, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_progreso(datos):
    with open(RUTA_SALIDA, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def llamada_con_reintento(func, *args, **kwargs):
    intentos = 3  # bajamos de 5 a 3: si es cuota diaria, insistir no ayuda
    for intento in range(intentos):
        try:
            return func(*args, **kwargs)
        except SpotifyException as e:
            if e.http_status == 429:
                espera = int(e.headers.get("Retry-After", 2)) if e.headers else 2
                if espera > 3600:  # más de 1h: es cuota diaria, no rate limit normal
                    print(f"🛑 Límite de cuota diaria alcanzado (espera {espera/3600:.1f}h). Parando aquí.")
                    raise SystemExit(0)
                espera += random.uniform(0, 1)
                print(f"   Rate limit, esperando {espera:.1f}s...")
                time.sleep(espera)
            else:
                raise

def buscar_artista(sp, nombre):
    resultado = llamada_con_reintento(
        sp.search, q=f'artist:"{nombre}"', type="artist", limit=1, market="ES"
    )
    items = resultado["artists"]["items"]
    if not items:
        print(f"⚠️  No encontrado: {nombre}")
        return None
    encontrado = items[0]
    # Aviso si el nombre devuelto no coincide con el buscado (posible mal emparejamiento)
    if encontrado["name"].lower() != nombre.lower():
        print(f"❗ Revisar: buscabas '{nombre}' y la API devolvió '{encontrado['name']}'")
    return encontrado

def extraer_discografia(sp, artist_id):
    albumes = []
    offset = 0
    limite = 10
    while True:
        resultado = llamada_con_reintento(
            sp.artist_albums, artist_id,
            album_type="album,single", limit=limite, offset=offset
        )
        items = resultado["items"]
        if not items:
            break
        for album in items:
            albumes.append({
                "nombre": album["name"],
                "tipo": album["album_type"],
                "fecha_lanzamiento": album["release_date"],
                "precision_fecha": album["release_date_precision"],
                "total_tracks": album["total_tracks"],
            })
        if resultado.get("next") is None:
            break
        offset += limite
    return albumes

def main():
    sp = get_spotify_client()
    datos_artistas = cargar_progreso()
    ya_procesados = {a["nombre_buscado"] for a in datos_artistas}

    for nombre in ARTISTAS_ESPANOLES:
        if nombre in ya_procesados:
            print(f"⏭️  Ya procesado, saltando: {nombre}")
            continue

        artista = buscar_artista(sp, nombre)
        if artista is None:
            continue

        discografia = extraer_discografia(sp, artista["id"])

        datos_artistas.append({
            "nombre_buscado": nombre,  # para poder reanudar sin duplicar
            "id": artista["id"],
            "nombre": artista["name"],
            "generos": artista.get("genres", []),
            "discografia": discografia,
        })

        guardar_progreso(datos_artistas)  # <-- se guarda tras CADA artista, no al final
        print(f"✅ {artista['name']} — {len(discografia)} álbumes/singles")
        time.sleep(0.2)

    print(f"\nGuardados {len(datos_artistas)} de {len(ARTISTAS_ESPANOLES)} artistas.")

if __name__ == "__main__":
    main()