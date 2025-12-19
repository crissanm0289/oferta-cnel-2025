import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(layout="wide", page_title="SISTEMA DE GESTIÓN RDO & DASHBOARD", page_icon="⚡")

# --- ESTILOS VISUALES (Negrita para los números) ---
st.markdown("""
<style>
    .main-header {font-size: 24px; font-weight: bold; color: #1E3A8A; margin-bottom: 20px;}
    /* Forzar que los labels de los inputs se vean grandes y claros */
    .stTextInput label, .stDateInput label, .stSelectbox label, .stTextArea label, .stNumberInput label {
        font-weight: bold !important;
        color: #b91c1c !important; /* Rojo oscuro para resaltar la numeración */
        font-size: 16px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
# Logo (si falla, borra la línea)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/e4/Logotipo_de_CNEL.svg", width=150)
st.sidebar.title("Configuración")

contrato_seleccionado = st.sidebar.selectbox(
    "Seleccione el Contrato:",
    ["ZONA 1 - SECTOR CAMARONERO", "ZONA 2 - SECTOR CAMARONERO"]
)

st.sidebar.markdown("---")
modulo = st.sidebar.radio("Navegación:", ["MÓDULO 1: RDO (Lista de 19 Puntos)", "MÓDULO 2: DASHBOARD (Lista de 8 Puntos)"])
st.sidebar.info(f"**Oferente:** Consorcio Fiscalred\n**Proceso:** Fiscalización Redes Eléctricas")

# --- DATOS SIMULADOS (Backend) ---
def obtener_datos(zona):
    months = ['Nov', 'Dic', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    if zona == "ZONA 1 - SECTOR CAMARONERO":
        fisico = [0, 8, 15, 30, 48, 65, 82, 100]
        programado = [0, 10, 20, 35, 50, 65, 80, 100]
        financiero = [0, 5, 12, 25, 40, 55, 70, 95]
        monto_total = 1500000.00
        anticipo = [x * 500 for x in financiero]
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
        'Devengo ($)': [x * (monto_total/1000) for x in financiero],
        'Acumulado ($)': [x * (monto_total/100) for x in financiero],
        'Anticipo ($)': anticipo
    })
    return df, monto_total

df_data, monto_obra = obtener_datos(contrato_seleccionado)

# ==============================================================================
# MÓDULO 1: RDO WEB (REGISTRO DIARIO DE OBRA) - NUMERACIÓN ESTRICTA
# ==============================================================================
if modulo == "MÓDULO 1: RDO (Lista de 19 Puntos)":
    st.markdown(f'<div class="main-header">Módulo 1: Registro Diario de Obra (RDO)</div>', unsafe_allow_html=True)
    st.warning("Formulario de Campo - Numeración conforme a TDR Pág. 28")

    with st.form("rdo_form"):
        # BLOQUE A
        st.markdown("### A. Datos Generales")
        c1, c2 = st.columns(2)
        # AQUÍ ESTÁ LA CORRECCIÓN: El número va DENTRO del string del label
        c1.date_input("1. Fechas de Ejecución", date.today())
        c2.text_input("4. Día de ejecución", "Día 15 - Jornada Ordinaria")
        
        c3, c4 = st.columns(2)
        c3.text_input("2. Datos Económicos del Contrato", "$ 67,490.10 (Fiscalización)")
        c4.text_input("3. Dato Económico total de los Proyectos", f"$ {monto_obra:,.2f} (Obra Civil/Eléctrica)")

        # BLOQUE B
        st.markdown("### B. Condiciones de Campo")
        col_clima, col_inc = st.columns(2)
        col_clima.selectbox("5. Condiciones climáticas", ["Soleado", "Nublado", "Lluvia Ligera", "Tormenta"])
        # Usamos selectbox o radio para el punto 19, con la etiqueta numerada
        col_inc.selectbox("19. Registro de Incidentes o accidentes", ["Sin Novedades", "Incidente Leve", "Accidente Grave"])

        # BLOQUE C
        st.markdown("### C. Control de Avance y Desempeño")
        
        # Puntos 6, 6.i, 6.ii
        st.info("**6. Progreso General del Contrato de Obra:**")
        m1, m2, m3 = st.columns(3)
        val_fis = df_data['Físico Real (%)'].iloc[5]
        
        # Usamos st.metric para visualización, pero ponemos el label claro
        m1.metric("6.i. % de Avance", f"{val_fis}%")
        m2.metric("6.i. $ de Avance", f"$ {(val_fis/100)*monto_obra:,.2f}")
        m3.metric("6.i. Avance Avaluado", f"$ {(val_fis/100)*monto_obra:,.2f}")
        
        st.text_input("6.ii. Avance prorrateado de los proyectos por Hito", "Hito #1: 100% (Terminado) | Hito #2: 45% (En ejecución)")

        # Puntos 7, 14, 15
        st.text_input("7. Indicadores de Desempeño y estimaciones", "CPI: 1.05 | SPI: 0.98 | Estimado al concluir: En presupuesto")
        
        cc1, cc2 = st.columns(2)
        cc1.selectbox("14. Control mediante Tabla de cantidades y Reporte de Avance diario", ["SI - Verificado en sitio", "NO"])
        cc2.text_input("15. Porcentaje total de los proyectos", f"{val_fis}% (Ponderado Global)")

        # Punto 8 (Gráfico)
        st.markdown("**8. Curva de Avance – Valor Ganado – Simbología**")
        fig_rdo = go.Figure()
        fig_rdo.add_trace(go.Scatter(x=df_data['Mes'], y=df_data['Programado (%)'], name='Línea Base (PV)', line=dict(dash='dash')))
        fig_rdo.add_trace(go.Scatter(x=df_data['Mes'], y=df_data['Físico Real (%)'], name='Valor Ganado (EV)', fill='tozeroy'))
        fig_rdo.update_layout(height=300, margin=dict(t=20, b=20))
        st.plotly_chart(fig_rdo, use_container_width=True)

        # BLOQUE D (Administrativo)
        st.markdown("### D. Control Administrativo y Legal")
        l1, l2, l3 = st.columns(3)
        l1.text_input("16. Registro de Contratos Complementarios", "Ninguno hasta la fecha")
        l2.text_input("17. Registro de Ordenes de trabajo", "OT-2025-001 (Aprobada)")
        l3.text_input("18. Registro de Incremento de cantidades de obra", "0.00%")

        # BLOQUE E (Detalle)
        st.markdown("### E. Detalle Diario y Evidencia")
        st.text_area("13. Personal y Equipos", "Cuadrilla A: 1 Capataz, 3 Linieros. Equipo: Grúa Canasta, Camioneta 4x4.")
        st.text_area("10. Actividades ejecutadas en el día", "Instalación de transformador de 50kVA en poste P-45. Tendido de red en baja tensión.")
        st.text_area("9. Observaciones de fiscalización", "Se solicita al contratista mejorar señalización vial en zona escolar.")
        
        st.markdown("**11. Registro fotográfico**")
        st.file_uploader("Cargar Evidencia (Punto 11)", accept_multiple_files=True)

        st.markdown("**12. Firmas de responsabilidad**")
        c_sig1, c_sig2 = st.columns(2)
        c_sig1.text_input("12. Firma: Fiscalizador (Usuario)", "FISCALIZADOR")
        c_sig2.text_input("12. Firma: Contratista (Residente)", "")

        st.form_submit_button("GUARDAR RDO DIARIO")


# ==============================================================================
# MÓDULO 2: DASHBOARD WEB (DESEMPEÑO) - NUMERACIÓN ESTRICTA
# ==============================================================================
elif modulo == "MÓDULO 2: DASHBOARD (Lista de 8 Puntos)":
    st.markdown(f'<div class="main-header">Módulo 2: Dashboard de Desempeño</div>', unsafe_allow_html=True)
    st.caption(f"Indicadores TDR para: {contrato_seleccionado}")

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
    # Usamos st.subheader para poner el número grande encima de cada gráfico
    
    col_izq, col_der = st.columns(2)

    with col_izq:
        # 3. Resumen Global
        st.subheader("3. Gráfico de Resumen de avance Global Acumulado")
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=df_data['Mes'], y=df_data['Físico Real (%)'], mode='lines+markers', name='Real Acumulado'))
        st.plotly_chart(fig3, use_container_width=True)

        # 5. Avance de Pagos
        st.subheader("5. Gráficos de Avance de Pagos (Acumulado)")
        fig5 = px.line(df_data, x='Mes', y='Acumulado ($)', markers=True)
        fig5.update_traces(line_color='green')
        st.plotly_chart(fig5, use_container_width=True)

        # 7. Pagos Mensuales
        st.subheader("7. Gráfico de Pagos mensuales (Planillas)")
        fig7 = px.bar(df_data, x='Mes', y='Devengo ($)', color='Devengo ($)')
        st.plotly_chart(fig7, use_container_width=True)

    with col_der:
        # 4. Avance físico por proyecto por mes
        st.subheader("4. Gráfico de Avance físico total por proyecto por mes")
        fig4 = px.bar(df_data, x='Mes', y='Físico Real (%)', title="Evolución Mensual")
        st.plotly_chart(fig4, use_container_width=True)

        # 6. Avance Porcentual y en Dólares
        st.subheader("6. Gráfico de Avance porcentual y en dólares")
        fig6 = go.Figure()
        fig6.add_trace(go.Scatter(x=df_data['Mes'], y=df_data['Físico Real (%)'], name='% Avance', yaxis='y1'))
        fig6.add_trace(go.Scatter(x=df_data['Mes'], y=df_data['Acumulado ($)'], name='$ Dólares', yaxis='y2', line=dict(dash='dot')))
        fig6.update_layout(yaxis=dict(title="%"), yaxis2=dict(title="$", overlaying='y', side='right'))
        st.plotly_chart(fig6, use_container_width=True)

        # 8. Devengo de Anticipo
        st.subheader("8. Gráfico de Devengo de anticipo")
        fig8 = px.area(df_data, x='Mes', y='Anticipo ($)')
        fig8.update_layout(title="Amortización Anticipo")
        st.plotly_chart(fig8, use_container_width=True)
