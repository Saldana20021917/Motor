# -*- coding: utf-8 -*-
"""Motor.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1r8BYEwa5oyF_kgfGBmwsdM8lMqm_JKfO
"""

from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import requests
import pandas as pd
import os


app = Flask(__name__)

# Clave de API de NewsAPI
API_KEY = "f2fe1d43327e4c7d9139fe4ae9d9d556"

# Obtener fechas para la consulta (últimos 7 días)
fecha_hasta = datetime.now()
fecha_desde = fecha_hasta - timedelta(days=7)
fecha_hasta_str = fecha_hasta.strftime('%Y-%m-%d')
fecha_desde_str = fecha_desde.strftime('%Y-%m-%d')

# Función para buscar noticias
def buscar_noticias(api_key, palabras_clave, idioma="es", fuentes=None, max_noticias=20):
    """
    Busca noticias relevantes utilizando NewsAPI.
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": " OR ".join(palabras_clave),  # Combinar palabras clave con "OR"
        "language": idioma,
        "from": fecha_desde_str,
        "to": fecha_hasta_str,
        "sortBy": "relevancy",  # Ordenar por relevancia
        "pageSize": max_noticias,
    }
    if fuentes:
        params["sources"] = ",".join(fuentes)

    headers = {"X-Api-Key": api_key}

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        articulos = response.json().get("articles", [])
        return [
            {
                "Título": articulo.get('title', 'Sin título'),
                "Fuente": articulo.get('source', {}).get('name', 'Desconocida'),
                "Descripción": articulo.get('description', 'Sin descripción'),
                "Enlace": articulo.get('url', 'Sin enlace'),
                "Fecha": articulo.get('publishedAt', 'Sin fecha'),
            }
            for articulo in articulos
        ]
    except requests.exceptions.RequestException as e:
        return {"error": f"Error al realizar la solicitud: {e}"}

# Endpoint para buscar noticias
@app.route('/buscar', methods=['POST'])
def buscar():
    data = request.json  # Datos enviados desde el frontend
    palabras_clave = data.get('palabras_clave', [])
    idioma = data.get('idioma', 'es')
    fuentes = data.get('fuentes', None)
    max_noticias = data.get('max_noticias', 20)

    if not palabras_clave:
        return jsonify({"error": "Debe proporcionar al menos una palabra clave"}), 400

    # Buscar noticias
    resultados = buscar_noticias(API_KEY, palabras_clave, idioma, fuentes, max_noticias)

    return jsonify(resultados)

# Endpoint raíz
@app.route('/')
def home():
    return "¡Bienvenido al Motor de Búsqueda de Noticias API!"
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  #asigna un puerto dinámico
    app.run(host='0.0.0.0', port=port)  
