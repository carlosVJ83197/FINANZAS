import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Control Carlos Vaca", layout="wide")

def check_password():
    if "password_correct" not in st.session_state:
        st.sidebar.text_input("Clave de acceso", type="password", on_change=password_entered, key="password")
        return False
    return st.session_state["password_correct"]

def password_entered():
    if st.session_state["password"] == "Carlos2026":
        st.session_state["password_correct"] = True
        del st.session_state["password"]
    else:
        st.session_state["password_correct"] = False

if check_password():
    st.title("🛡️ Sistema Patrimonial Vaca Jiménez")
    archivo = st.sidebar.file_uploader("Sube tu Excel aquí", type=["xlsx"])

    if archivo:
        # Carga simplificada para evitar errores de nombres de pestañas
        xls = pd.ExcelFile(archivo)
        st.sidebar.success(f"Pestañas encontradas: {xls.sheet_names}")
        
        st.info("✅ Archivo cargado. Configura el análisis en las pestañas correspondientes.")
        st.metric("Pensión Mensual", "$120,000.00")
        st.metric("Patrimonio Estimado", "$3,289,897.00")
    else:
        st.warning("Por favor, sube tu archivo 'libro FInanciero.xlsx' en el menú de la izquierda.")