# Spotify Playlist Backup & Sync

## Descripción
Este script permite **monitorear una playlist de Spotify** y transferir automáticamente cada 5 canciones nuevas a una **playlist de respaldo**. Además, almacena un **historial completo** de todas las canciones en una base de datos SQLite y genera backups automáticos.

## Características
- **Monitoreo continuo** de una playlist de Spotify.
- **Transferencia automática** de canciones a una playlist de respaldo cada 5 nuevas canciones.
- **Almacenamiento en base de datos SQLite** para registrar todas las canciones agregadas.
- **Backups automáticos** de la base de datos antes de cada operación de volcado.
- **Ajuste dinámico del tiempo de revisión** para optimizar llamadas a la API de Spotify.

## Requisitos
1. **Cuenta de Spotify** (puede ser gratuita o premium).
2. **Credenciales de la API de Spotify:**
   - `CLIENT_ID`
   - `CLIENT_SECRET`
   - `REDIRECT_URI`
3. **Python 3.x** y las siguientes librerías:
   ```bash
   pip install spotipy
   ```
4. **Crear una app en [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)** y obtener los permisos adecuados.

## Instalación
1. **Clonar este repositorio:**
   ```bash
   git clone https://github.com/Enrique190999/BackupPlaylistSpotify.git
   cd spotify-backup
   ```
2. **Configurar credenciales:**
   Edita el archivo `config.py` (o configura variables de entorno) con tus credenciales de Spotify.

3. **Ejecutar el script:**
   ```bash
   python main.py
   ```

## Configuración
En el código, debes definir:
- `PLAYLIST_ORIGINAL`: ID de la playlist que deseas monitorear.
- `PLAYLIST_RESPALDO`: ID de la playlist donde se hará el respaldo.

Puedes obtener los IDs de tus playlists con la API de Spotify o desde la URL de la playlist en la app.

## Limitaciones de la API de Spotify
- **Límites de solicitudes**: La API impone restricciones de tasa de peticiones. Si excedes el límite, recibirás un error `429 Too Many Requests`.
- **Restricciones en la modificación de playlists**:
  - **Cuentas gratuitas** pueden agregar canciones a sus propias playlists.
  - No se puede modificar la playlist de otro usuario sin permisos.
  - El **máximo de canciones por playlist** es de ~10.000.
- **Autenticación y tokens**:
  - Los tokens de acceso expiran cada **1 hora**.
  - Se necesita un **refresh token** para renovar accesos automáticamente.
- **No hay webhooks en Spotify**, por lo que el script debe usar **polling** para detectar cambios en la playlist.

## Futuras Mejoras
- Exportación de playlists a CSV.
- Dashboard web con Flask/Django.
- Filtrar canciones por género/artista antes de transferir.

## Licencia
Este proyecto está bajo la licencia **MIT**. Puedes usarlo y modificarlo libremente.

---
### Autor
[Kikedev](https://github.com/Enrique190999)
