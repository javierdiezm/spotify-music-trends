# Spotify Music Trends 🎵

Proyecto de análisis de datos musicales: extracción desde la API de Spotify, limpieza de datos y visualización final en un dashboard de Power BI.

## Objetivo

Comparar la actividad de 30 artistas/grupos de rock-pop español a través de su discografía — quién ha publicado más, la proporción de álbumes frente a singles, y cómo ha evolucionado esa actividad en el tiempo.

> **Nota:** en noviembre de 2024 y febrero de 2026, Spotify eliminó de su API varios campos y endpoints que se usan habitualmente en proyectos como este: `popularity` (artista, álbum y track), `followers`, el endpoint de top tracks del artista, y el campo `genres` quedó deprecado y vacío en la práctica. Por eso este proyecto se apoya en la **discografía** (fechas de lanzamiento, tipo de lanzamiento, número de tracks) en lugar de en popularidad o género.

## Estado del proyecto

🚧 En construcción. Progreso actual:

- [x] Conexión autenticada con la API de Spotify (Client Credentials)
- [x] Extracción de discografía de 30 artistas españoles
- [x] Limpieza y normalización de datos
- [x] Exportación a CSV final
- [ ] Dashboard en Power BI

## Estructura del proyecto

```
spotify-music-trends/
├── src/
│   ├── clean.py
│   ├── config.py                          # Conexión autenticada con la API de Spotify
│   └── extract.py
├── tests/
│   └── test_connection.py
├── data/
│   ├── raw/
│   │   └── artistas_espanoles.json        # JSON crudo tal cual devuelve la API
│   └── processed/
│       └── discografia_artistas_es.csv    # CSV limpio, listo para Power BI
├── .env                                    # Credenciales (no se sube, ver .gitignore)
├── .gitignore
└── README.md
```

## Requisitos

- Python 3.10+
- Una app registrada en el [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

## Instalación

1. Clona el repositorio
2. Instala las dependencias:
   ```bash
   pip install spotipy pandas python-dotenv
   ```
3. Crea un archivo `.env` en la raíz con tus credenciales:
   ```
   SPOTIFY_CLIENT_ID=tu_client_id
   SPOTIFY_CLIENT_SECRET=tu_client_secret
   ```

## Uso

```bash
python src/extract.py   # extrae discografía de la API a data/raw/
python src/clean.py     # limpia y exporta a data/processed/
```

El CSV resultante en `data/processed/` está listo para conectarse directamente en Power BI (Obtener datos → Texto/CSV).

## Licencia

Este proyecto es de uso personal.