import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.config import get_spotify_client

sp = get_spotify_client()
resultado = sp.search(q="Bad Bunny", type="artist", limit=1)
print(resultado["artists"]["items"][0]["name"])