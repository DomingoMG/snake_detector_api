
## Activar el script en el powershell
.\.venv\Scripts\activate  

## Arrancar los servicios y escuchando los cambios
uvicorn main:app --host 0.0.0.0 --port 8000 --reload