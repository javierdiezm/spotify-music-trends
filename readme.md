# Spotify Music Trends 🎵

Proyecto de análisis de datos musicales: extracción desde la API de Spotify, limpieza de datos y visualización final en un dashboard de Power BI.

## Objetivo

Explorar patrones en popularidad, géneros y mercados a partir de datos reales de Spotify — por ejemplo, qué géneros dominan en distintos países o cómo evoluciona la popularidad de un artista en el tiempo.

> **Nota:** los "audio features" (energía, bailabilidad, tempo...) fueron deprecados por Spotify para apps nuevas en noviembre de 2024, por lo que este proyecto se centra en popularidad, géneros, mercados y fechas de lanzamiento en su lugar.

## Estado del proyecto

🚧 En construcción. Progreso actual:

- [x] Conexión autenticada con la API de Spotify (Client Credentials)
- [ ] Extracción de artistas y top tracks
- [ ] Limpieza y normalización de datos
- [ ] Exportación a CSV final
- [ ] Dashboard en Power BI

## Estructura del proyecto

```
spotify-music-trends/
├── src/
│   ├── config.py                        # Conexión autenticada con la API de Spotify
│   └── extract.py
├── tests/
│   └── test_connection.py
├── data/
│   ├── raw/
│   |   └── artistas_espanoles.json      # JSON crudo tal cual devuelve la API
│   └── processed/                       # CSV limpio, listo para Power BI
├── .env                                 # Credenciales (no se sube, ver .gitignore)
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

*(Se irá completando a medida que avance el proyecto)*

## Licencia

Este proyecto es de uso personal.
