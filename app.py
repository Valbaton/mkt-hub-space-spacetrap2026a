import streamlit as st
import streamlit.components.v1 as components
from datos import cargar_datos_nube
from motor_ui import construir_dashboard

st.set_page_config(
    page_title="SPACETRAP - PROD", 
    page_icon="https://github.com/Valbaton/public_resources_gunova/blob/main/Assets/space_spaceevent2_perfil.jpg?raw=true", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

hide_st_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0 !important;}
    iframe {border: none;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

with st.spinner('Sincronizando base de datos con SPACE...'):
    # Ahora recibimos y pasamos únicamente los 3 dataframes necesarios
    df_r, df_c, df_a = cargar_datos_nube()
    
    if not df_r.empty or not df_a.empty:
        html_dashboard = construir_dashboard(df_r, df_c, df_a)
        # Altura ajustada a 1000px para albergar cómodamente la nueva UI
        components.html(html_dashboard, height=1000, scrolling=True)
    else:
        st.error("No se pudo conectar con la BBDD.")