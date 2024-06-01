# Usa una imagen base oficial de Python
FROM python:3.11.9

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requerimientos y luego instala las dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido del proyecto al directorio de trabajo en el contenedor
COPY . /app/

# Expone el puerto en el que correrá la aplicación
EXPOSE 8000

# Define el comando por defecto para correr la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
