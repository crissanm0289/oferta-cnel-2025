import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(layout="wide", page_title="SISTEMA DE GESTIÓN RDO & DASHBOARD", page_icon="⚡")

# --- ESTILOS VISUALES ---
st.markdown("""
<style>
    .main-header {font-size: 24px; font-weight: bold; color: #1E3A8A; margin-bottom: 20px;}
    .section-header {font-size: 18px; font-weight: bold; color: #444; margin-top: 15px; border-bottom: 2px solid #1E3A8A;}
    .metric-container {background-color: #f0f2f6; padding: 10px; border-radius: 5px;}
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (SELECTOR DE CONTRATO) ---
# Si el link del logo falla, puedes borrar la línea siguiente
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/e4/Logotipo_de_CNEL.svg", width=150)
st.sidebar.title("Configuración")

contrato_seleccionado = st.sidebar.selectbox(
    "Seleccione el Contrato:",
    ["ZONA 1 - SECTOR CAMARONERO", "ZONA 2 - SECTOR CAMARONERO"]
)

st.sidebar.markdown("---")
modulo = st.sidebar.radio("Navegación:", ["1. RDO WEB (Checklist 19 Puntos)", "2. DASHBOARD (Checklist 8 Puntos)"])
st.sidebar.info(f"**Usuario:** Consorcio Fiscalred\n**Rol:** Oferente / Jefe de Fiscalización")

# --- GENERACIÓN DE DATOS DINÁMICOS (SEGÚN ZONA) ---
def obtener_datos(zona):
    months = ['Nov', 'Dic', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    if zona == "ZONA 1 - SECTOR CAMARONERO":
        # Zona 1: Buen ritmo
        fisico = [0, 8, 15, 30, 48, 65, 82, 100]
        programado = [0, 10, 20, 35, 50, 65, 80, 100]
        financiero = [0, 5, 12, 25, 40, 55, 70, 95]
        monto_total = 1500000.00 # Monto obra referencial
        presupuesto_fis = 67490.10
        estado = "NORMAL"
    else:
        # Zona 2: Retraso inicial recuperado
        fisico = [0, 2, 8, 15, 25, 45, 60, 85]
        programado = [0, 10, 20, 35, 50, 65, 80, 100]
        financiero = [0, 2, 6, 12, 20, 40, 55, 80]
        monto_total = 1450000.00
        presupuesto_fis = 67490.10
        estado = "ATENCIÓN"
    
    # Crear DataFrame
    df = pd.DataFrame({
        'Mes': months,
        'Físico Real (%)': fisico,
        'Programado (%)': programado,
        'Financiero Real (%)': financiero,
        'Devengo ($)': [x * (monto_total/1000) for x in financiero], # Simulado
        'Anticipo ($)': [x * (monto_total/2000) for x in financiero] # Simulado amortización
    })
    return df, monto_total, presupuesto_fis, estado

df_data, monto_obra, monto_fis, estado_obra = obtener_datos(contrato_seleccionado)

# ==============================================================================
# MÓDULO 1: RDO WEB (19 PUNTOS EXACTOS)
# ==============================================================================
if modulo == "1. RDO WEB (Checklist 19 Puntos)":
    st.markdown(f'<div class="main-header">Módulo 1: Registro Diario de Obra (RDO) Web</div>', unsafe_allow_html=True)
    st.info(f"Registrando datos para: **{contrato_seleccionado}**")

    # --- GRUPO 1: DATOS GENERALES (Puntos 1, 2, 3, 4) ---
    with st.expander("A. DATOS GENERALES (Puntos 1, 2, 3, 4)", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        c1.date_input("1. Fechas de Ejecución", date.today())
        c2.text_input("4. Día de ejecución", "Día 45")
        c3.text_input("2. Datos Económicos Contrato", f"${monto_fis:,.2f} (Fiscalización)")
        c4.text_input("3. Dato Económico Total Proyectos", f"${monto_obra:,.2f} (Obra)")

    # --- GRU
