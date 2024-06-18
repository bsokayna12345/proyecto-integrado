
#Instalar dependencias y configurar el entorno
FROM python:3.11-slim-buster

WORKDIR /app

#Instalar dependencias de Python
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

#Copiar el código del proyecto
COPY . .

#Recoger archivos estáticos
RUN python manage.py collectstatic --noinput

#Exponer el puerto
EXPOSE 8000

#Comando para correr la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "tienda.wsgi:application"]

