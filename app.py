import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime, date

# --- CONFIGURACIÓN DE LA PÁGINA (Identidad Visual) ---
st.set_page_config(layout="wide", page_title="SISTEMA DE GESTIÓN RDO & DASHBOARD - OFERTA TÉCNICA", page_icon="⚡")

# --- ESTILOS CSS PARA QUE SE VEA PROFESIONAL (FORMAL) ---
st.markdown("""
<style>
    .main-header {font-size: 24px; font-weight: bold; color: #1E3A8A;}
    .sub-header {font-size: 18px; font-weight: bold; color: #333;}
    .metric-card {background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #1E3A8A;}
</style>
""", unsafe_allow_html=True)

# --- SIMULACIÓN DE DATOS (Para que la comisión vea gráficos llenos) ---
def get_dummy_data():
    months = ['Nov', 'Dic', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    avance_fisico = [0, 5, 12, 25, 40, 60, 85, 100]
    avance_financiero = [0, 0, 10, 20, 35, 50, 75, 100]
    avance_programado = [0, 10, 20, 35, 50, 65, 80, 100]
    return pd.DataFrame({
        'Mes': months,
        'Físico Real (%)': avance_fisico,
        'Financiero Real (%)': avance_financiero,
        'Programado (%)': avance_programado,
        'Devengo ($)': [x * 670 for x in avance_financiero] # Simulado base 67k
    })

df_dummy = get_dummy_data()

# --- BARRA LATERAL (Navegación) ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Logotipo_de_CNEL.svg/1200px-Logotipo_de_CNEL.svg.png", width=150) # Logo referencial
st.sidebar.title("Menú de Navegación")
modulo = st.sidebar.radio("Ir a:", ["1. RDO WEB (Innovación)", "2. DASHBOARD WEB (Desempeño)"])

st.sidebar.markdown("---")
st.sidebar.info("**Oferente:** CONSORCIO FISCALRED\n\n**Proceso:** Fiscalización Redes Eléctricas Zona 1 y 2")

# ==============================================================================
# MÓDULO 1: RDO WEB (REGISTRO DIARIO DE OBRA) - Cumplimiento TDR Pág 28
# ==============================================================================
if modulo == "1. RDO WEB (Innovación)":
    st.markdown('<div class="main-header">Módulo 1: Registro Diario de Obra (RDO) Web</div>', unsafe_allow_html=True)
    st.markdown("Plataforma digital para recopilación en tiempo real (Innovación).")

    # Puntos 1, 2, 3, 4: Datos Generales
    with st.expander("A. INFORMACIÓN GENERAL Y ECONÓMICA (Puntos 1-4)", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            fecha_rdo = st.date_input("1. & 4. Fecha de Ejecución / Día", date.today())
        with col2:
            st.text_input("2. Datos Económicos del Contrato", value="Contrato No. 001-2025 - $67,490.10")
        with col3:
            st.text_input("3. Dato Económico Total Proyectos", value="$1,500,000.00 (Referencial Obra)")

    # Puntos 5, 13, 19: Condiciones de Campo
    with st.expander("B. CONDICIONES DE CAMPO Y RECURSOS (Puntos 5, 13, 19)", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("5. Condiciones Climáticas", ["Despejado", "Nublado", "Lluvia Ligera", "Lluvia Fuerte"])
            st.text_area("13. Personal y Equipos (Detalle)", "1 Jefe, 2 Fiscalizadores, 1 Socializador, 3 Camionetas, 2 GPS...")
        with col2:
            st.warning("19. Registro de Incidentes o Accidentes")
            incidente = st.radio("¿Hubo incidentes hoy?", ["No", "Sí"])
            if incidente == "Sí":
                st.text_input("Descripción del Incidente", placeholder="Describa el evento...")

    # Puntos 6, 7, 8, 14, 15, 16, 17, 18: Control Técnico
    with st.expander("C. CONTROL TÉCNICO Y AVANCE (Puntos 6-8, 14-18)", expanded=True):
        st.write("6. Progreso General del Contrato de Obra")
        m1, m2, m3 = st.columns(3)
        m1.metric("i. % de Avance", "15.5%")
        m2.metric("i. $ de Avance", "$10,460.96")
        m3.metric("i. Avance Avaluado", "$10,460.96")
        
        st.info("ii. Avance prorrateado por Hito: Hito 1 (100%), Hito 2 (20%)")

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("8. Curva de Avance - Valor Ganado - Simbología")
            # Gráfico pequeño de curva S para el RDO
            fig_mini = go.Figure()
            fig_mini.add_trace(go.Scatter(x=df_dummy['Mes'], y=df_dummy['Físico Real (%)'], name='Real', line=dict(color='green')))
            fig_mini.add_trace(go.Scatter(x=df_dummy['Mes'], y=df_dummy['Programado (%)'], name='Programado', line=dict(color='blue', dash='dash')))
            fig_mini.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig_mini, use_container_width=True)
            
        with c2:
            st.subheader("Registros Adicionales")
            st.checkbox("14. Control tabla de cantidades y Reporte Diario (Verificado)")
            st.text_input("15. Porcentaje total de los proyectos (%)", "12.5%")
            st.text_input("16. Registro de Contratos Complementarios", "N/A")
            st.text_input("17. Registro de Órdenes de Trabajo", "OT-005")
            st.text_input("18. Registro de Incremento de Cantidades", "Sin incrementos")
            st.text_area("7. Indicadores de Desempeño y Estimaciones", "SPI: 0.98, CPI: 1.00")

    # Puntos 9, 10, 11, 12: Actividades y Cierre
    with st.expander("D. ACTIVIDADES, EVIDENCIA Y CIERRE (Puntos 9-12)", expanded=True):
        st.text_area("9. Observaciones de Fiscalización", placeholder="Ingrese observaciones del día...")
        st.text_area("10. Actividades ejecutadas en el día", placeholder="Detalle actividades...")
        
        st.write("11. Registro Fotográfico")
        st.file_uploader("Cargar fotos (Evidencia)", accept_multiple_files=True)
        
        st.write("12. Firmas de Responsabilidad")
        c1, c2, c3 = st.columns(3)
        c1.text_input("Firma Fiscalizador", "Ing. Juan Pérez")
        c2.text_input("Firma Contratista", "Ing. Contratista")
        c3.success("Validación Digital: OK")

    st.button("GUARDAR RDO DIARIO (Enviar a Base de Datos)")


# ==============================================================================
# MÓDULO 2: DASHBOARD WEB (DESEMPEÑO) - Cumplimiento TDR Pág 28
# ==============================================================================
elif modulo == "2. DASHBOARD WEB (Desempeño)":
    st.markdown('<div class="main-header">Módulo 2: Dashboard de Desempeño</div>', unsafe_allow_html=True)
    st.write("Visualización dinámica de indicadores para la toma de decisiones.")
    
    # 1. Fecha de emisión
    st.caption(f"1. Fecha de emisión del reporte: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # FILA SUPERIOR: Métricas Clave
    st.markdown("### Resumen Ejecutivo")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("2. % Avance Acumulado", "35%", "+2%")
    col2.metric("2. Avance por Hitos", "3/8 Hitos", "En cronograma")
    col3.metric("Devengado ($)", "$23,621.50")
    col4.metric("Estado", "NORMAL", delta_color="normal")

    st.markdown("---")

    # FILA 1 DE GRÁFICOS: Curvas S y Avance Físico
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("##### 3. Gráfico Resumen Avance Global & 8. Curva Valor Ganado")
        fig_s = go.Figure()
        fig_s.add_trace(go.Scatter(x=df_dummy['Mes'], y=df_dummy['Programado (%)'], name='Planificado', line=dict(color='blue', width=3)))
        fig_s.add_trace(go.Scatter(x=df_dummy['Mes'], y=df_dummy['Físico Real (%)'], name='Ejecutado (Valor Ganado)', fill='tozeroy', line=dict(color='green', width=3)))
        fig_s.update_layout(title="Curva S: Planificado vs Ejecutado", yaxis_title="% Avance")
        st.plotly_chart(fig_s, use_container_width=True)

    with c2:
        st.markdown("##### 4. Gráfico Avance Físico Total por Proyecto (Mes)")
        fig_bar = px.bar(df_dummy, x='Mes', y='Físico Real (%)', title="Avance Físico Mensualizado")
        fig_bar.update_traces(marker_color='#1E3A8A')
        st.plotly_chart(fig_bar, use_container_width=True)

    # FILA 2 DE GRÁFICOS: Financiero y Pagos
    c3, c4 = st.columns(2)

    with c3:
        st.markdown("##### 5. Gráficos de Avance de Pagos & 7. Pagos Mensuales")
        fig_pay = go.Figure()
        fig_pay.add_trace(go.Bar(x=df_dummy['Mes'], y=df_dummy['Devengo ($)'], name='Pago Mensual ($)', marker_color='orange'))
        fig_pay.update_layout(title="Historial de Planillas/Pagos ($)")
        st.plotly_chart(fig_pay, use_container_width=True)

    with c4:
        st.markdown("##### 6. Avance Porcentual vs Dólares & 8. Devengo Anticipo")
        # Gráfico combinado
        fig_combo = go.Figure()
        fig_combo.add_trace(go.Scatter(x=df_dummy['Mes'], y=df_dummy['Financiero Real (%)'], name='% Financiero', yaxis='y1'))
        fig_combo.add_trace(go.Scatter(x=df_dummy['Mes'], y=df_dummy['Devengo ($)'], name='$ Devengado (Amortización)', yaxis='y2', line=dict(dash='dot')))
        
        fig_combo.update_layout(
            title="Correlación Avance Físico vs Financiero (Amortización Anticipo)",
            yaxis=dict(title="% Avance"),
            yaxis2=dict(title="$ USD", overlaying='y', side='right')
        )
        st.plotly_chart(fig_combo, use_container_width=True)

    # DETALLE DE PROYECTOS (Tabla de datos)
    st.markdown("##### Detalle de Componentes / Proyectos")
    st.dataframe(df_dummy.style.highlight_max(axis=0), use_container_width=True)