import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(layout="wide", page_title="SISTEMA DE GESTIÓN RDO & DASHBOARD", page_icon="⚡")

# --- ESTILOS VISUALES (Para que se vea formal) ---
st.markdown("""
<style>
    .main-header {font-size: 24px; font-weight: bold; color: #1E3A8A; margin-bottom: 20px;}
    .num-label {font-weight: bold; color: #b91c1c;} /* Color rojo oscuro para los números */
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
# Si el logo falla, puedes borrar la siguiente línea
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/e4/Logotipo_de_CNEL.svg", width=150)
st.sidebar.title("Configuración")

contrato_seleccionado = st.sidebar.selectbox(
    "Seleccione el Contrato/Zona:",
    ["ZONA 1 - SECTOR CAMARONERO", "ZONA 2 - SECTOR CAMARONERO"]
)

st.sidebar.markdown("---")
modulo = st.sidebar.radio("Ir a Módulo:", ["MÓDULO 1: RDO (19 Puntos)", "MÓDULO 2: DASHBOARD (8 Puntos)"])
st.sidebar.info(f"**Usuario:** Consorcio Fiscalred n\n**Perfil:** Oferente / Jefe Fiscalización")

# --- DATOS SIMULADOS (Backend) ---
def obtener_datos(zona):
    months = ['Nov', 'Dic', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    if zona == "ZONA 1 - SECTOR CAMARONERO":
        fisico = [0, 8, 15, 30, 48, 65, 82, 100]
        programado = [0, 10, 20, 35, 50, 65, 80, 100]
        financiero = [0, 5, 12, 25, 40, 55, 70, 95]
        monto_total = 1500000.00
        anticipo = [x * 500 for x in financiero] # Simulado
    else:
        fisico = [0, 5, 10, 15, 25, 40, 60, 85]
        programado = [0, 10, 20, 35, 50, 65, 80, 100]
        financiero = [0, 2, 8, 15, 25, 35, 50, 75]
        monto_total = 1450000.00
        anticipo = [x * 400 for x in financiero]

    df = pd.DataFrame({
        'Mes': months,
        'Físico Real (%)': fisico,
        'Programado (%)': programado,
        'Financiero Real (%)': financiero,
        'Devengo ($)': [x * (monto_total/1000) for x in financiero], # Mensual aprox
        'Acumulado ($)': [x * (monto_total/100) for x in financiero],
        'Anticipo ($)': anticipo
    })
    return df, monto_total

df_data, monto_obra = obtener_datos(contrato_seleccionado)

# ==============================================================================
# MÓDULO 1: RDO WEB (REGISTRO DIARIO DE OBRA) - 19 PUNTOS
# ==============================================================================
if modulo == "MÓDULO 1: RDO (19 Puntos)":
    st.markdown(f'<div class="main-header">Módulo 1: Registro Diario de Obra (RDO) Web</div>', unsafe_allow_html=True)
    st.warning("Formulario numerado según TDR para verificación de la Comisión Técnica.")

    with st.form("rdo_form"):
        # --- BLOQUE 1: DATOS INICIALES ---
        st.markdown("### A. Datos Generales")
        c1, c2 = st.columns(2)
        c1.date_input("1. Fechas de Ejecución", date.today())
        c2.text_input("4. Día de ejecución", "Día 15")
        
        c3, c4 = st.columns(2)
        c3.text_input("2. Datos Económicos del Contrato", "$ 67,490.10 (Fiscalización)")
        c4.text_input("3. Dato Económico total de los Proyectos", f"$ {monto_obra:,.2f} (Obra Civil/Eléctrica)")

        # --- BLOQUE 2: CAMPO ---
        st.markdown("### B. Condiciones de Campo")
        col_clima, col_inc = st.columns(2)
        col_clima.selectbox("5. Condiciones climáticas", ["Soleado", "Nublado", "Lluvia", "Tormenta"])
        col_inc.radio("19. Registro de Incidentes o accidentes", ["Sin Novedades", "Con Novedades"], horizontal=True)

        # --- BLOQUE 3: CONTROL DE AVANCE (EL GRUESO DEL PUNTAJE) ---
        st.markdown("### C. Control de Avance y Desempeño")
        st.info("**6. Progreso General del Contrato de Obra:**")
        
        # Punto 6.i
        m1, m2, m3 = st.columns(3)
        val_fis = df_data['Físico Real (%)'].iloc[5]
        m1.metric("6.i. % de Avance", f"{val_fis}%")
        m2.metric("6.i. $ de Avance", f"$ {(val_fis/100)*monto_obra:,.2f}")
        m3.metric("6.i. Avance Avaluado Acumulado", f"$ {(val_fis/100)*monto_obra:,.2f}")
        
        # Punto 6.ii
        st.text_input("6.ii. Avance prorrateado de los proyectos por Hito", "Hito #1: 100% | Hito #2: 45%")

        # Puntos 7, 14, 15
        st.text_input("7. Indicadores de Desempeño y estimaciones", "CPI: 1.05 (Bajo Presupuesto) | SPI: 0.98 (En Cronograma)")
        
        cc1, cc2 = st.columns(2)
        cc1.checkbox("14. Control mediante Tabla de cantidades y Reporte de Avance diario", value=True)
        cc2.text_input("15. Porcentaje total de los proyectos", f"{val_fis}% (Ponderado Global)")

        # Punto 8: GRÁFICO DENTRO DEL FORMULARIO
        st.markdown("**8. Curva de Avance – Valor Ganado – Simbología**")
        fig_rdo = go.Figure()
        fig_rdo.add_trace(go.Scatter(x=df_data['Mes'], y=df_data['Programado (%)'], name='Línea Base (PV)', line=dict(dash='dash')))
        fig_rdo.add_trace(go.Scatter(x=df_data['Mes'], y=df_data['Físico Real (%)'], name='Valor Ganado (EV)', fill='tozeroy'))
        fig_rdo.update_layout(height=300, margin=dict(t=20, b=20))
        st.plotly_chart(fig_rdo, use_container_width=True)

        # --- BLOQUE 4: ADMINISTRATIVO Y LEGAL ---
        st.markdown("### D. Control Administrativo y Legal")
        l1, l2, l3 = st.columns(3)
        l1.text_input("16. Registro de Contratos Complementarios", "N/A")
        l2.text_input("17. Registro de Ordenes de trabajo", "OT-2025-001")
        l3.text_input("18. Registro de Incremento de cantidades de obra", "0.00%")

        # --- BLOQUE 5: DETALLE DIARIO Y FIRMAS ---
        st.markdown("### E. Detalle Diario")
        st.text_area("13. Personal y Equipos", "Cuadrilla A: 1 Capataz, 3 Linieros. Equipo: Grúa Canasta, Camioneta 4x4.")
        st.text_area("10. Actividades ejecutadas en el día", "Instalación de transformador de 50kVA en poste P-45.")
        st.text_area("9. Observaciones de fiscalización", "Se solicita al contratista mejorar señalización vial.")
        
        st.markdown("**11. Registro fotográfico**")
        st.file_uploader("Cargar Evidencia (Punto 11)", accept_multiple_files=True)

        st.markdown("**12. Firmas de responsabilidad**")
        c_sig1, c_sig2 = st.columns(2)
        c_sig1.text_input("Firma: Fiscalizador (Usuario)", "Ing. Cristhian San Martin")
        c_sig2.text_input("Firma: Contratista (Residente)", "")

        st.form_submit_button("GUARDAR RDO (Cumple los 19 Puntos)")


# ==============================================================================
# MÓDULO 2: DASHBOARD (DESEMPEÑO) - 8 PUNTOS
# ==============================================================================
elif modulo == "MÓDULO 2: DASHBOARD (8 Puntos)":
    st.markdown(f'<div class="main-header">Módulo 2: Dashboard de Desempeño</div>', unsafe_allow_html=True)
    st.caption(f"Visualización de los 8 Puntos requeridos para: {contrato_seleccionado}")

    # 1. Fecha de emisión
    st.markdown(f"#### 1. Fecha de emisión: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # 2. % Avance Acumulado
    st.markdown("#### 2. % de Avance Acumulado por componentes o por hitos y por proyecto")
    k1, k2, k3 = st.columns(3)
    val_real = df_data['Físico Real (%)'].iloc[5]
    k1.metric("Avance Global", f"{val_real}%")
    k2.metric("Hito Civil", f"{val_real-5}%")
    k3.metric("Hito Eléctrico", f"{val_real+2}%")

    st.markdown("---")

    # GRÁFICOS SOLICITADOS (3 al 8)
    
    col_izq, col_der = st.columns(2)

    with col_izq:
        # 3. Resumen Global
        st.markdown("**3. Gráfico de Resumen de avance Global Acumulado**")
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=df_data['Mes'], y=df_data['Físico Real (%)'], mode='lines+markers', name='Real Acumulado'))
        st.plotly_chart(fig3, use_container_width=True)

        # 5. Avance de Pagos
        st.markdown("**5. Gráficos de Avance de Pagos (Acumulado)**")
        fig5 = px.line(df_data, x='Mes', y='Acumulado ($)', markers=True)
        fig5.update_traces(line_color='green')
        st.plotly_chart(fig5, use_container_width=True)

        # 7. Pagos Mensuales
        st.markdown("**7. Gráfico de Pagos mensuales (Planillas)**")
        fig7 = px.bar(df_data, x='Mes', y='Devengo ($)', color='Devengo ($)')
        st.plotly_chart(fig7, use_container_width=True)

    with col_der:
        # 4. Avance físico por proyecto por mes
        st.markdown("**4. Gráfico de Avance físico total por proyecto por mes**")
        fig4 = px.
