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
st.sidebar.info(f"**Usuario:** Ing. Cristhian San Martin\n**Rol:** Oferente / Jefe de Fiscalización")

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

    # --- GRUPO 2: CONDICIONES Y RECURSOS (Puntos 5, 13, 19) ---
    with st.expander("B. CAMPO Y RECURSOS (Puntos 5, 13, 19)", expanded=True):
        col_a, col_b = st.columns(2)
        with col_a:
            st.selectbox("5. Condiciones climáticas", ["Soleado", "Nublado", "Lluvia"])
            st.text_area("13. Personal y Equipos", "Personal: 1 Jefe, 2 Fiscalizadores. Equipos: 2 Camionetas, 1 Estación Total.")
        with col_b:
            st.radio("19. Registro de Incidentes o accidentes", ["Sin Novedad", "Incidente Leve", "Accidente"], horizontal=True)
            st.text_input("Detalle de Incidente (si aplica)", "")

    # --- GRUPO 3: CONTROL DE AVANCE TÉCNICO (Puntos 6, 7, 8, 14, 15) ---
    with st.expander("C. CONTROL TÉCNICO (Puntos 6, 7, 8, 14, 15)", expanded=True):
        st.markdown("**6. Progreso General del Contrato de Obra:**")
        m1, m2, m3, m4 = st.columns(4)
        val_fis = df_data['Físico Real (%)'].iloc[4]
        m1.metric("i. % de Avance", f"{val_fis}%")
        m2.metric("i. $ de Avance", f"${(val_fis/100)*monto_obra:,.2f}")
        m3.metric("i. Avance Avaluado", f"${(val_fis/100)*monto_obra:,.2f}")
        m4.metric("ii. Avance Prorrateado Hito", "Hito 2: 45%")

        c_graph, c_inputs = st.columns([1, 1])
        with c_graph:
            st.markdown("**8. Curva de Avance - Valor Ganado - Simbología**")
            fig_mini = go.Figure()
            fig_mini.add_trace(go.Scatter(x=df_data['Mes'], y=df_data['Programado (%)'], name='Prog.', line=dict(dash='dash')))
            fig_mini.add_trace(go.Scatter(x=df_data['Mes'], y=df_data['Físico Real (%)'], name='Real', fill='tozeroy'))
            fig_mini.update_layout(height=200, margin=dict(l=0, r=0, t=20, b=0))
            st.plotly_chart(fig_mini, use_container_width=True)
        
        with c_inputs:
            st.text_input("7. Indicadores de Desempeño y estimaciones", "SPI: 0.98 | CPI: 1.02 | Estimado al concluir: En presupuesto")
            st.checkbox("14. Control tabla de cantidades y Reporte Diario", value=True)
            st.text_input("15. Porcentaje total de los proyectos", f"{val_fis}% Ponderado")

    # --- GRUPO 4: CONTROL LEGAL Y CAMBIOS (Puntos 16, 17, 18) ---
    with st.expander("D. CONTROL LEGAL Y CAMBIOS (Puntos 16, 17, 18)"):
        l1, l2, l3 = st.columns(3)
        l1.text_input("16. Registro Contratos Comp.", "Ninguno")
        l2.text_input("17. Registro Órdenes Trabajo", "OT-001 Aprobada")
        l3.text_input("18. Reg. Incremento Cantidades", "0.00%")

    # --- GRUPO 5: ACTIVIDADES Y CIERRE (Puntos 9, 10, 11, 12) ---
    with st.expander("E. ACTIVIDADES Y CIERRE (Puntos 9, 10, 11, 12)", expanded=True):
        st.text_area("9. Observaciones de fiscalización", "Se verifica cumplimiento de EPPs en todos los frentes.")
        st.text_area("10. Actividades ejecutadas en el día", "- Izado de postes en Sector 1.\n- Tendido de conductor fase A en Sector 2.")
        st.file_uploader("11. Registro fotográfico (Georreferenciado)", accept_multiple_files=True)
        
        st.markdown("**12. Firmas de responsabilidad**")
        f1, f2 = st.columns(2)
        f1.text_input("Firma Fiscalizador", "Ing. Cristhian San Martin")
        f2.text_input("Firma Contratista Residente", "")
        
    st.button("GUARDAR RDO DIARIO (Sincronizar)")

# ==============================================================================
# MÓDULO 2: DASHBOARD WEB (8 PUNTOS EXACTOS)
# ==============================================================================
elif modulo == "2. DASHBOARD (Checklist 8 Puntos)":
    st.markdown(f'<div class="main-header">Módulo 2: Dashboard de Desempeño</div>', unsafe_allow_html=True)
    
    # 1. Fecha de Emisión
    st.caption(f"**1. Fecha de emisión:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Contrato: {contrato_seleccionado}")

    # 2. % Avance Acumulado
    st.markdown("### 2. % de Avance Acumulado (Hitos / Proyectos)")
    k1, k2, k3, k4 = st.columns(4)
    val_fis_actual = df_data['Físico Real (%)'].iloc[5] # Mes actual simulado
    k1.metric("Avance Físico Global", f"{val_fis_actual}%")
    k2.metric("Componente Civil", f"{val_fis_actual - 5}%")
    k3.metric("Componente Eléctrico", f"{val_fis_actual + 2}%")
    k4.metric("Estado Hito Actual", "En Ejecución")

    st.markdown("---")

    # FILA 1 DE GRÁFICOS
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**3. Gráfico de Resumen de avance Global Acumulado**")
        # Usamos el gráfico de Curva S como resumen global
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=df_data['Mes'], y=df_data['Físico Real (%)'], name='Real', line=dict(color='green', width=3)))
        fig3.add_trace(go.Scatter(x=df_data['Mes'], y=df_data['Programado (%)'], name='Programado', line=dict(dash='dash', color='gray')))
        fig3.update_layout(title="Curva S Acumulada", yaxis_title="% Avance")
        st.plotly_chart(fig3, use_container_width=True)
    
    with c2:
        st.markdown("**4. Gráfico de Avance físico total por proyecto por mes**")
        # Simulación de barras mensuales
        fig4 = px.bar(df_data, x='Mes', y='Físico Real (%)', title="Evolución Mensual Física", color='Físico Real (%)')
        st.plotly_chart(fig4, use_container_width=True)

    # FILA 2 DE GRÁFICOS
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**5. Gráficos de Avance de Pagos & 7. Pagos Mensuales**")
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(x=df_data['Mes'], y=df_data['Devengo ($)'], name='Planillado ($)', marker_color='#1E3A8A'))
        fig5.update_layout(title="Planillas Mensuales ($)", yaxis_title="USD")
        st.plotly_chart(fig5, use_container_width=True)
    
    with c4:
        st.markdown("**6. Gráfico de Avance porcentual y en dólares**")
        fig6 = go.Figure()
        fig6.add_trace(go.Scatter(x=df_data['Mes'], y=df_data['Físico Real (%)'], name='% Físico', yaxis='y1', line=dict(color='orange')))
        fig6.add_trace(go.Bar(x=df_data['Mes'], y=df_data['Devengo ($)'], name='$ Dólares', yaxis='y2', opacity=0.3))
        fig6.update_layout(
            title="Correlación % vs $",
            yaxis=dict(title="%"),
            yaxis2=dict(title="$ USD", overlaying='y', side='right')
        )
        st.plotly_chart(fig6, use_container_width=True)

    # FILA 3: DEVENGO DE ANTICIPO
    st.markdown("**8. Gráfico de Devengo de anticipo**")
    fig8 = px.area(df_data, x='Mes', y='Anticipo ($)', title="Amortización de Anticipo Acumulada")
    fig8.update_traces(line_color='red')
    st.plotly_chart(fig8, use_container_width=True)
