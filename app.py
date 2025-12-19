import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(layout="wide", page_title="SISTEMA INTEGRAL DE FISCALIZACIÓN", page_icon="⚡")

# --- ESTILOS CSS ---
st.markdown("""
<style>
    .main-header {font-size: 24px; font-weight: bold; color: #1E3A8A;}
    .metric-card {background-color: #f0f2f6; border-left: 5px solid #1E3A8A;}
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (SELECTOR DE CONTRATO) ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/e4/Logotipo_de_CNEL.svg", width=150)
st.sidebar.title("Configuración")

# AQUÍ ESTÁ EL CAMBIO CLAVE: SELECTOR DE CONTRATO
contrato_seleccionado = st.sidebar.selectbox(
    "Seleccione el Contrato:",
    ["ZONA 1 - SECTOR CAMARONERO", "ZONA 2 - SECTOR CAMARONERO"]
)

st.sidebar.markdown("---")
modulo = st.sidebar.radio("Navegación:", ["1. RDO WEB (Campo)", "2. DASHBOARD (Gerencial)"])
st.sidebar.info(f"**Usuario:** Consorcio Fiscalred\n**Perfil:** Jefe de Fiscalización\n**Estado:** CONECTADO")

# --- LÓGICA DE DATOS (SIMULACIÓN POR ZONA) ---
# Esto demuestra que el software maneja datos distintos para cada contrato
def obtener_datos(zona):
    months = ['Nov', 'Dic', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    
    if zona == "ZONA 1 - SECTOR CAMARONERO":
        # Zona 1: Proyecto más avanzado
        avance_fisico = [0, 8, 15, 30, 45, 65, 80, 100]
        avance_financiero = [0, 5, 12, 25, 40, 55, 70, 95]
        programado = [0, 10, 20, 35, 50, 65, 80, 100]
        presupuesto = 67490.10
        estado = "NORMAL"
        color_estado = "normal"
    else:
        # Zona 2: Proyecto con retraso inicial (Para mostrar que el sistema detecta alertas)
        avance_fisico = [0, 2, 5, 10, 20, 35, 50, 80] # Más lento
        avance_financiero = [0, 2, 5, 12, 22, 35, 55, 85]
        programado = [0, 10, 20, 35, 50, 65, 80, 100]
        presupuesto = 72500.00 # Monto simulado diferente
        estado = "ALERTA"
        color_estado = "off"

    return pd.DataFrame({
        'Mes': months,
        'Físico Real (%)': avance_fisico,
        'Financiero Real (%)': avance_financiero,
        'Programado (%)': programado,
        'Devengo ($)': [x * (presupuesto/100) for x in avance_financiero]
    }), presupuesto, estado, color_estado

df_data, monto_contrato, estado_obra, color_delta = obtener_datos(contrato_seleccionado)

# ==============================================================================
# MÓDULO 1: RDO WEB
# ==============================================================================
if modulo == "1. RDO WEB (Campo)":
    st.markdown(f'<div class="main-header">Registro Diario de Obra (RDO) - {contrato_seleccionado}</div>', unsafe_allow_html=True)
    st.caption("Ingreso de datos en sitio (Cumplimiento TDR: Innovación y Trazabilidad)")

    with st.form("rdo_form"):
        # A. Datos Generales
        st.subheader("A. Información del Día")
        c1, c2, c3 = st.columns(3)
        c1.date_input("Fecha de Ejecución", date.today())
        c2.text_input("Contrato / Zona", value=contrato_seleccionado, disabled=True)
        c3.selectbox("Proyecto Específico", ["Sitio Zapanal", "Barrio El Dorado", "Sitio Las Carmelitas", "Otro"])

        # B. Recursos y Clima
        st.subheader("B. Recursos y Clima")
        rc1, rc2 = st.columns(2)
        with rc1:
            st.selectbox("Condiciones Climáticas", ["Soleado", "Nublado", "Lluvia Ligera", "Lluvia Fuerte"])
            st.text_area("Personal Técnico y Obrero", "1 Residente, 2 Linieros, 2 Ayudantes...")
        with rc2:
            st.text_area("Maquinaria y Equipos", "1 Grúa, 2 Camionetas, Herramientas menores...")
            st.checkbox("¿Hubo accidentes hoy?", value=False)

        # C. Actividades
        st.subheader("C. Actividades y Avance")
        st.text_area("Descripción de Actividades Ejecutadas", "Izado de 5 postes en alimentador principal...")
        
        # Simulación de carga de fotos
        st.file_uploader("Evidencia Fotográfica (Georreferenciada)", accept_multiple_files=True)

        submitted = st.form_submit_button("GUARDAR INFORME DIARIO")
        if submitted:
            st.success(f"¡RDO guardado exitosamente para {contrato_seleccionado}! Sincronizado con base de datos central.")

# ==============================================================================
# MÓDULO 2: DASHBOARD
# ==============================================================================
elif modulo == "2. DASHBOARD (Gerencial)":
    st.markdown(f'<div class="main-header">Tablero de Control - {contrato_seleccionado}</div>', unsafe_allow_html=True)
    st.caption("Monitoreo de Desempeño y Hitos (Cumplimiento TDR: Dashboard Web)")

    # KPIs Principales
    k1, k2, k3, k4 = st.columns(4)
    ult_fisico = df_data['Físico Real (%)'].iloc[4] # Simulación mes actual
    ult_finan = df_data['Devengo ($)'].iloc[4]
    
    k1.metric("Avance Físico Acumulado", f"{ult_fisico}%", "vs. Programado")
    k2.metric("Estado del Contrato", estado_obra, delta_color=color_delta)
    k3.metric("Planillado Acumulado", f"${ult_finan:,.2f}")
    k4.metric("Presupuesto Referencial", f"${monto_contrato:,.2f}")

    st.markdown("---")

    # Gráficos
    g1, g2 = st.columns(2)
    
    with g1:
        st.markdown("##### Curva S: Programado vs Ejecutado")
        fig_s = go.Figure()
        fig_s.add_trace(go.Scatter(x=df_data['Mes'], y=df_data['Programado (%)'], name='Planificado', line=dict(dash='dash')))
        fig_s.add_trace(go.Scatter(x=df_data['Mes'], y=df_data['Físico Real (%)'], name='Ejecutado', fill='tozeroy'))
        st.plotly_chart(fig_s, use_container_width=True)

    with g2:
        st.markdown("##### Control Financiero (Devengo)")
        fig_bar = px.bar(df_data, x='Mes', y='Devengo ($)', title="Planillado Mensual ($)")
        st.plotly_chart(fig_bar, use_container_width=True)

    st.info("Nota: Este Dashboard se alimenta automáticamente de los reportes ingresados en el módulo RDO.")
