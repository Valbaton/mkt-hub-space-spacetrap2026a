import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

def cargar_datos_nube():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # Lectura de las 3 hojas requeridas en el V62
        df_rrss = conn.read(worksheet="Content_RRSS", ttl=0)
        df_comu = conn.read(worksheet="Content_Comunidad", ttl=0)
        df_acc  = conn.read(worksheet="Content_Account", ttl=0)
        
        # Limpieza estándar
        for df in [df_rrss, df_comu, df_acc]:
            df.columns = df.columns.str.strip()

        # Fix de coerción para proteger el dashboard en la nube
        df_rrss = df_rrss.astype(object).fillna('-')
        df_comu = df_comu.astype(object).fillna('-')
        df_acc  = df_acc.astype(object).fillna('-')
            
        if 'Post_Fecha' in df_rrss.columns:
            df_rrss['Post_Fecha'] = pd.to_datetime(df_rrss['Post_Fecha'], dayfirst=True, errors='coerce')
            
        return df_rrss, df_comu, df_acc

    except Exception as e:
        st.error(f"❌ Error crítico de conexión a la BBDD: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
