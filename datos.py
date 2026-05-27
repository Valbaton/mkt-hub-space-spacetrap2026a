import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

@st.cache_data(ttl=60)
def cargar_datos_nube():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # EL FIX: Caché de 60 segundos (ttl=60) para evitar bloqueos de la API de Google.
        # Si necesitas que tarde más en refrescar, pon ttl=300 (5 minutos).
        df_rrss = conn.read(worksheet="Content_RRSS", ttl=60)
        df_comu = conn.read(worksheet="Content_Comunidad", ttl=60)
        df_acc  = conn.read(worksheet="Content_Account", ttl=60)
        
        for df in [df_rrss, df_comu, df_acc]:
            df.columns = df.columns.str.strip()

        df_rrss = df_rrss.astype(object).fillna('-')
        df_comu = df_comu.astype(object).fillna('-')
        df_acc  = df_acc.astype(object).fillna('-')
            
        if 'Post_Fecha' in df_rrss.columns:
            df_rrss['Post_Fecha'] = pd.to_datetime(df_rrss['Post_Fecha'], dayfirst=True, errors='coerce')
            
        return df_rrss, df_comu, df_acc

    except Exception as e:
        st.error(f"❌ Error crítico de conexión a la base de datos.")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
