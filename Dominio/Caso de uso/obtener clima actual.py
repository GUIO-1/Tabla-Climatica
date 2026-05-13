import streamlit as st
# Importamos los adaptadores y el caso de uso
from Adaptadores.api.openweather_adapter import OpenWeatherAdapter [cite: 67]
from Adaptadores.persistencia.sqlite_adapter import SQLiteAdapter [cite: 68]
from Dominio.Caso_de_uso.obtener_clima_actual import ObtenerClimaActual [cite: 69]

# --- ENSAMBLAJE (Inyección de dependencias) --- [cite: 89, 96]
api_key = st.secrets["openweather_key"]
servicio = OpenWeatherAdapter(api_key) [cite: 71]
repositorio = SQLiteAdapter("clima_cache.db") [cite: 72]

# Creamos el caso de uso inyectándole sus herramientas
consultar_clima = ObtenerClimaActual(servicio, repositorio) [cite: 74]

# --- INTERFAZ ---
# ... (tu código de sidebar y selección de ciudad)

if st.button("Consultar Clima"):
    with st.spinner("Buscando..."):
        # Solo llamamos al caso de uso, app.py no sabe nada de SQL ni Requests [cite: 78]
        datos, es_offline = consultar_clima.ejecutar(ciudad_fiel) [cite: 76]
        
        if es_offline:
            st.warning(f"⚠️ Mostrando datos guardados de {ciudad_fiel}.")
        
        if datos:
            # Aquí sigue tu código de visualización (métricas, gráficos radar, etc.)
            st.metric("Temperatura", f"{datos['main']['temp']} °C")