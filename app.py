import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. CONFIGURACIÓN DE PÁGINA (DEBE SER LO PRIMERO)
st.set_page_config(
    page_title="Weather Pro NI", 
    page_icon="🌤️", 
    layout="wide"
)

# 2. FUNCIÓN DE CONEXIÓN A LA API
@st.cache_data(ttl=600)
def consultar_clima(ciudad):
    try:
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

st.sidebar.header("📍 Parámetros de Consulta")
ciudades = ["Rivas", "Managua", "Leon", "Granada", "Jinotega", "Matagalpa", "Chontales", "Boaco", "Bluefields"]
ciudad_fiel = st.sidebar.selectbox("Selecciona una ciudad:", ciudades)

# 4. PROCESAMIENTO Y VISUALIZACIÓN
with st.spinner(f"Extrayendo datos climáticos de {ciudad_fiel}..."):
    datos = consultar_clima(ciudad_fiel)

if datos:
   
    # 4.1Obtener el código del icono de la API
    icono_codigo = datos['weather'][0]['icon']
    url_icono = f"http://openweathermap.org/img/wn/{icono_codigo}@4x.png"

    #4.2Mostrar la imagen en la barra lateral
    st.sidebar.markdown("---") # Separador visual
    st.sidebar.image(url_icono, caption=f"Clima en {ciudad_fiel}", use_container_width=True)
    
    #4.3 Mostrar descripción breve
    descripcion = datos['weather'][0]['description'].capitalize()
    st.sidebar.info(f"**Estado:** {descripcion}")

    # 4.4 Métricas Rápidas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Temperatura", f"{datos['main']['temp']} °C")
    col2.metric("Sensación", f"{datos['main']['feels_like']} °C")
    col3.metric("Humedad", f"{datos['main']['humidity']}%")
    col4.metric("Viento", f"{datos['wind']['speed']} m/s")

    st.divider()

    # 4.5 Tabla de Análisis Estadístico
   # Asegúrate de que cada lista tenga exactamente 6 elementos
    dict_stats = {
        "Métrica": [
            "Temperatura Real", "Sensación Térmica", "Temp. Mínima", 
            "Temp. Máxima", "Velocidad del viento", "Presión Atm."
        ],
        "Valor": [
            f"{datos['main']['temp']} °C",
            f"{datos['main']['feels_like']} °C",
            f"{datos['main']['temp_min']} °C",
            f"{datos['main']['temp_max']} °C",
            f"{datos['wind']['speed']} m/s",
            f"{datos['main']['pressure']} hPa"
        ],
        "Estado": [
            "Normal" if datos['main']['temp'] < 30 else "Cálido",
            "N/A",
            "Mínimo hoy",
            "Máximo hoy",
            "Brisa" if datos['wind']['speed'] < 5 else "Viento fuerte",
            "Estable" if 1010 <= datos['main']['pressure'] <= 1015 else "Variable"
        ]
    }
    
    # Esto ya no fallará
    df_stats = pd.DataFrame(dict_stats)
    st.dataframe(df_stats, use_container_width=True, hide_index=True)

    # 4.6 AQUÍ VA EL PUNTO 2 (GRÁFICO DE RADAR) ---
    st.subheader("📊 Perfil Climático Detallado")
    


    # Definimos las categorías que queremos comparar
    categories = ['Temp (°C)', 'Humedad (%)', 'Viento (m/s)', 'Nubes (%)', 'Presión (norm)']
    
    # Normalizamos la presión para que quepa en la escala (ej. 1013 hPa -> 50)
    presion_norm = (datos['main']['pressure'] - 950) / (1050 - 950) * 100

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
          r=[datos['main']['temp'], datos['main']['humidity'], datos['wind']['speed'], datos['clouds']['all'], presion_norm],
          theta=categories,
          fill='toself',
          name=ciudad_fiel,
          marker=dict(color='#00FFAA') # Un color llamativo para el radar
    ))

    fig_radar.update_layout(
      polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
      showlegend=False,
      template="plotly_dark",
      transition_duration=800 # Animación fluida al cambiar de ciudad
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)

    # 4.7 Gráfico Animado de Plotly
    st.subheader("📈 Comparativa Visual de Temperaturas")
    df_animado = pd.DataFrame({
        'Métrica': ['Mínima', 'Actual', 'Máxima'],
        'Temperatura (°C)': [datos['main']['temp_min'], datos['main']['temp'], datos['main']['temp_max']]
    })

    fig = px.bar(
        df_animado, 
        x='Métrica', 
        y='Temperatura (°C)',
        color='Métrica',
        text_auto='.1f',
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig.update_layout(transition_duration=800, yaxis_range=[0, 45], showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # 4.8 Mensaje Informativo
    dif_termica = abs(datos['main']['temp'] - datos['main']['feels_like'])
    st.info(f"💡 **Dato del sistema:** Hay una diferencia de {dif_termica:.2f} °C en {ciudad_fiel} debido a la humedad del {datos['main']['humidity']}%.")

else:
    st.warning("⚠️ No se pudieron obtener datos. Revisa tu configuración.")

# 5. PIE DE PÁGINA
st.markdown("---")
st.caption("Desarrollado con Streamlit y OpenWeather API.")