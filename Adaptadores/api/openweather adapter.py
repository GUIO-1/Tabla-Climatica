import requests
from Dominio.Puertos.servicio_clima import ServicioClima

class OpenWeatherAdapter(ServicioClima):
    def __init__(self, api_key):
        self.api_key = api_key

    def obtener_datos(self, ciudad: str):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad},NI&appid={self.api_key}&units=metric&lang=es"
        respuesta = requests.get(url, timeout=5)
        if respuesta.status_code == 200:
            return respuesta.json()
        raise Exception("No se pudo conectar con la API")