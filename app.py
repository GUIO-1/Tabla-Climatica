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
st.title("🌤️ Dashboard Meteorológico de Nicaragua")
st.markdown("Consulta en tiempo real los datos climáticos de las principales ciudades.")

# Filtro lateral para navegación
st.sidebar.header("📍 Parámetros de Consulta")
ciudades = ["Rivas", "Managua", "Leon", "Granada", "Jinotega", "Matagalpa", "Bluefields"]
ciudad_fiel = st.sidebar.selectbox("Selecciona una ciudad:", ciudades)

# 4. PROCESAMIENTO Y VISUALIZACIÓN
datos = consultar_clima(ciudad_fiel)

if datos:
    # Mostramos los datos clave en métricas visuales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Temperatura", f"{datos['main']['temp']} °C")
    with col2:
        st.metric("Sensación", f"{datos['main']['feels_like']} °C")
    with col3:
        st.metric("Humedad", f"{datos['main']['humidity']}%")
    with col4:
        st.metric("Viento", f"{datos['wind']['speed']} m/s")

    st.divider()

    # Mapa Interactivo usando las coordenadas de la API
    st.subheader(f"Mapa de Ubicación: {ciudad_fiel}")
    df_coords = pd.DataFrame({
        'lat': [datos['coord']['lat']],
        'lon': [datos['coord']['lon']]
    })
    st.map(df_coords)
    
    # Detalle técnico opcional
  #/  with st.expander("Ver detalles técnicos (JSON)"):
     #/   st.json(datos)

else:
    st.warning("⚠️ No se pudieron obtener datos. Revisa tu archivo de secretos.")

# 5. PIE DE PÁGINA
st.markdown("---")
st.caption("Desarrollado con Streamlit y OpenWeather API.")