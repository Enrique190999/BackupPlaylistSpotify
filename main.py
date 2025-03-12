import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import sqlite3
import shutil
import os

# Configuración de la API de Spotify
CLIENT_ID = 'TU_CLIENT_ID'
CLIENT_SECRET = 'TU_CLIENT_SECRET'
REDIRECT_URI = 'http://localhost:8888/callback'

# Permisos necesarios
SCOPE = "playlist-read-private playlist-modify-public playlist-modify-private"

# Playlists
PLAYLIST_ORIGINAL = "ID_DE_TU_PLAYLIST_ORIGINAL"
PLAYLIST_RESPALDO = "ID_DE_TU_PLAYLIST_RESPALDO"

# Autenticación en Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

# Nombre de la base de datos
DB_NAME = "canciones_spotify.db"
BACKUP_DIR = "backups"

# Asegurar que el directorio de backups existe
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# Conexión con SQLite
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS canciones (
                    id TEXT PRIMARY KEY,
                    nombre TEXT,
                    artista TEXT,
                    fecha_agregada TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                  )''')
conn.commit()

def obtener_canciones(playlist_id):
    """ Obtiene las canciones de una playlist dada """
    results = sp.playlist_tracks(playlist_id)
    canciones = []

    for item in results["items"]:
        track = item["track"]
        canciones.append({
            "id": track["id"],
            "nombre": track["name"],
            "artista": ", ".join([artist["name"] for artist in track["artists"]])
        })

    return canciones

def obtener_canciones_guardadas():
    """ Obtiene las canciones ya almacenadas en la base de datos """
    cursor.execute("SELECT id FROM canciones")
    return {row[0] for row in cursor.fetchall()}

def guardar_canciones(canciones):
    """ Guarda nuevas canciones en la base de datos """
    cursor.executemany("INSERT INTO canciones (id, nombre, artista) VALUES (?, ?, ?)",
                       [(c["id"], c["nombre"], c["artista"]) for c in canciones])
    conn.commit()

def realizar_backup():
    """ Realiza un backup de la base de datos """
    backup_path = os.path.join(BACKUP_DIR, f"backup_{int(time.time())}.db")
    shutil.copy(DB_NAME, backup_path)
    print(f"Backup realizado: {backup_path}")

def transferir_canciones():
    """ Monitorea la playlist original y transfiere cada 5 canciones nuevas a la de respaldo """
    
    while True:
        canciones_originales = obtener_canciones(PLAYLIST_ORIGINAL)
        canciones_guardadas = obtener_canciones_guardadas()

        # Identificar nuevas canciones que no han sido almacenadas en la base de datos
        nuevas_canciones = [c for c in canciones_originales if c["id"] not in canciones_guardadas]

        if nuevas_canciones:
            print(f"Se han encontrado {len(nuevas_canciones)} canciones nuevas.")

            # Guardar en la base de datos
            guardar_canciones(nuevas_canciones)

            # Hacer backup antes de transferir
            realizar_backup()

            # Si hay 5 o más canciones nuevas, se transfieren a la playlist de respaldo
            if len(nuevas_canciones) >= 5:
                canciones_a_mover = [c["id"] for c in nuevas_canciones[:5]]

                sp.playlist_add_items(PLAYLIST_RESPALDO, canciones_a_mover)
                print(f"Se han transferido {len(canciones_a_mover)} canciones a la playlist de respaldo.")

        # Ajustar tiempo de revisión dinámicamente
        if len(nuevas_canciones) == 0:
            tiempo_espera = 300  # 5 minutos si no hay nuevas canciones
        elif len(nuevas_canciones) < 5:
            tiempo_espera = 120  # 2 minutos si hay menos de 5
        else:
            tiempo_espera = 60  # 1 minuto si hay muchas nuevas canciones

        print(f"Esperando {tiempo_espera} segundos para la siguiente revisión...")
        time.sleep(tiempo_espera)

# Iniciar la monitorización
transferir_canciones()
