import streamlit as st
import requests
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA
# 'layout="wide"' aprovecha mejor el ancho del monitor para el dashboard
st.set_page_config(
    page_title="Weather Pro NI", 
    page_icon="🌤️", 
    layout="wide"
)

# 2. FUNCIÓN DE CONEXIÓN A LA API
# El decorador @st.cache_data evita peticiones repetidas innecesarias
@st.cache_data(ttl=600)
def consultar_clima(ciudad):
    try:
        # Recuperamos la llave de tu archivo .streamlit/secrets.toml
        api_key = st.secrets["openweather_key"]
        url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad},NI&appid={api_key}&units=metric&lang=es"
        
        respuesta = requests.get(url, timeout=5)
        if respuesta.status_code == 200:
            return respuesta.json()
        return None
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

# 3. INTERFAZ Y FILTROS
st.title("🌤️ Tabla Meteorológica de Nicaragua")
st.markdown("Consulta en tiempo real los datos climáticos de las principales ciudades.")

# Filtro lateral para navegación
st.sidebar.header("📍 Parámetros de Consulta")
ciudades = ["Rivas", "Managua", "Leon", "Granada", "Jinotega", "Matagalpa", "Chontales", "Boaco", "Bluefields"]
ciudad_fiel = st.sidebar.selectbox("Selecciona una ciudad:", ciudades)

# 4. PROCESAMIENTO Y VISUALIZACIÓN (Continuación del código anterior)
datos = consultar_clima(ciudad_fiel)

if datos:
    # ... (código de métricas que ya tienes) ...

    st.subheader(f"Análisis Estadístico para {ciudad_fiel}")
    
    # Creamos un diccionario con las métricas clave para análisis
    dict_stats = {
        "Métrica": ["Temperatura Real", "Sensación Térmica", "Temp. Mínima", "Temp. Máxima", "velocidad del viento", "Presión Atm."],
        "Valor": [
            f"{datos['main']['temp']} °C",
            f"{datos['main']['feels_like']} °C",
            f"{datos['main']['temp_min']} °C",
            f"{datos['main']['temp_max']} °C",
            f"{datos['main']['pressure']} hPa"
            f"{datos['wind']['speed']} k/h"
        ],
        "Estado": [
            "Normal" if datos['main']['temp'] < 30 else "Cálido",
            "N/A",
            "Mínimo hoy",
            "Máximo hoy",
            "Estable" if 1010 <= datos['main']['pressure'] <= 1015 else "Variable"
        ]
    }

    # Convertimos a DataFrame para mostrarlo como tabla profesional
    df_stats = pd.DataFrame(dict_stats)
    
    # Usamos st.dataframe para una tabla interactiva
    st.dataframe(df_stats, use_container_width=True, hide_index=True)

    # Cálculo de diferencia térmica (un dato estadístico extra)
    dif_termica = abs(datos['main']['temp'] - datos['main']['feels_like'])
    
    st.info(f"💡 **Dato del sistema:** Hay una diferencia de {dif_termica:.2f} °C entre la temperatura real y la sensación térmica debido a la humedad del {datos['main']['humidity']}%.")

else:
    st.warning("⚠️ No se pudieron generar estadísticas.")
# 5. PIE DE PÁGINA
st.markdown("---")
st.caption("Desarrollado con Streamlit y OpenWeather API.")