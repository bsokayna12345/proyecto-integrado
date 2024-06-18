# Usa una imagen base de Python
FROM python:3.11-slim-buster

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos a la imagen
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación a la imagen
COPY . .

# Ejecuta colectstatic de Django para recopilar archivos estáticos
RUN python manage.py collectstatic --noinput

# Exponer el puerto en el que Gunicorn se ejecutará
EXPOSE 8000

# Comando para ejecutar Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "tienda.wsgi:application"]
