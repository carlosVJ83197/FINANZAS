import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Portal Patrimonial Carlos Vaca", layout="wide")

# --- SEGURIDAD ---
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
    st.title("🛡️ Sistema de Inteligencia Financiera")
    st.markdown("### Usuario: Carlos Vaca Jiménez | Estatus: Jubilado")

    archivo = st.sidebar.file_uploader("Actualizar datos (Subir Excel)", type=["xlsx"])

    if archivo:
        # 1. CARGA DE DATOS
        df_inv = pd.read_excel(archivo, sheet_name="Inversiones")
        df_tdc = pd.read_excel(archivo, sheet_name="Tarjetas")
        # Asumiendo que tienes una pestaña llamada 'Facturas' o 'Gastos'
        df_gastos = pd.read_excel(archivo, sheet_name="Facturas")

        # 2. MÉTRICAS PATRIMONIALES
        c1, c2, c3 = st.columns(3)
        c1.metric("Patrimonio Total", f"${df_inv['Monto'].sum():,.2f}")
        c2.metric("Pensión Mensual", "$120,000.00")
        
        # Cálculo de salud
        gasto_medico = df_gastos[df_gastos['Concepto'].str.contains('Médico|Salud|Dentista|Hospital', case=False, na=False)]['Monto'].sum()
        c3.metric("Gasto Médico Acumulado", f"${gasto_medico:,.2f}", delta="Deducible SAT")

        st.divider()

        # 3. ANÁLISIS MÉDICO DETALLADO
        st.subheader("🏥 Control de Salud y Gastos Médicos 2026")
        col_med1, col_med2 = st.columns([2, 1])

        with col_med1:
            # Gráfica de barras por categoría médica
            fig_med = px.bar(df_gastos, x='Concepto', y='Monto', color='Concepto', title="Desglose de Gastos en Salud")
            st.plotly_chart(fig_med, use_container_width=True)

        with col_med2:
            st.info("**Recordatorio del Analista:**")
            st.write(f"Has gastado **${gasto_medico:,.2f}** en lo que va de enero.")
            st.write("Asegúrate de tener el XML y PDF de cada gasto para maximizar tu devolución de impuestos.")
            if gasto_medico > 15000:
                st.warning("⚠️ El gasto médico está superando el promedio mensual esperado.")

        # 4. LISTADO DE TARJETAS
        st.subheader("💳 Próximos Pagos")
        st.dataframe(df_tdc[['Tarjeta', 'Fecha_Corte', 'Monto']], use_container_width=True)

    else:
        st.info("👋 Bienvenido, Carlos. Sube tu archivo 'libro Financiero.xlsx' para iniciar el análisis.")