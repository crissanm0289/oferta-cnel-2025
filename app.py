import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(layout="wide", page_title="SISTEMA DE GESTIÓN RDO & DASHBOARD", page_icon="⚡")

# --- GESTIÓN DE ESTADO (SESSION STATE) PARA NAVEGACIÓN ---
# Esto permite que el botón de "Ir al Dashboard" funcione de verdad
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "MÓDULO 1: RDO (Lista de 19 Puntos)"

# Función para cambiar de página
def cambiar_pagina(nombre_pagina):
    st.session_state.pagina_actual = nombre_pagina

# --- ESTILOS VISUALES ---
st.markdown("""
<style>
    .main-header {font-size: 24px; font-weight: bold; color: #1E3A8A; margin-bottom: 10px;}
    
    /* Etiquetas numéricas en Rojo y Negrita */
    .stTextInput label, .stDateInput label, .stSelectbox label, .stTextArea label, .stNumberInput label, .stSlider label {
        font-weight: bold !important;
        color: #b91c1c !important; 
        font-size: 15px !important;
    }

    /* Estilo Ficha Técnica */
    .ficha-tecnica {
        width: 100%; border-collapse: collapse; margin-bottom: 20px;
        font-family: Arial, sans-serif; font-size: 14px; border: 1px solid #ddd;
    }
    .ficha-tecnica th {background-color: #1E3A8A; color: white; padding: 8px; text-align: left;}
    .ficha-tecnica td {padding: 8px; border: 1px solid #ddd; background-color: #f9f9f9; color: #333;}
    
    /* Mensaje de Éxito Personalizado */
    .success-box {
        padding: 15px; background-color: #d4edda; color: #155724; 
        border: 1px solid #c3e6cb; border-radius: 5px; margin-top: 10px; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/e4/Logotipo_de_CNEL.svg", width=150)
st.sidebar.title("Configuración")

contrato_seleccionado = st.sidebar.selectbox(
    "Seleccione el Contrato/Zona:",
    ["ZONA 1 - SECTOR CAMARONERO", "ZONA 2 - SECTOR CAMARONERO"]
)

st.sidebar.markdown("---")

# Navegación controlada por Session State
modulo = st.sidebar.radio(
    "Navegación:", 
    ["MÓDULO 1: RDO (Lista de 19 Puntos)", "MÓDULO 2: DASHBOARD (Lista de 8 Puntos)"],
    index=0 if st.session_state.pagina_actual == "MÓDULO 1: RDO (Lista de 19 Puntos)" else 1,
    key="navegacion_radio",
    on_change=lambda: cambiar_pagina(st.session_state.navegacion_radio) # Sincronizar
)

st.sidebar.info(f"**Oferente:** Consorcio FiscalRed\n**Usuario:** Ing. Cristhian San Martin")

# --- DATOS FICHA TÉCNICA ---
def obtener_ficha_tecnica(zona):
    if zona == "ZONA 1 - SECTOR CAMARONERO":
        return {
            "Entidad": "CNEL EP - UNIDAD DE NEGOCIO EL ORO",
            "Categoría": "CONSTRUCCION DE REDES DE DISTRIBUCION",
            "Objeto": "EOR Construccion de redes electricas... ZONA 1 CAF GD",
            "Código": "COTO-CNELEP-2025-43",
            "Plazo": "150 Días",
            "Contratista": "CONSORCIO CAF ARENILLAS",
            "Rep_Legal": "OSCAR LUIS YANANGOMEZ SUQUILANDA",
            "Monto": "$ 399.743,03",
            "Link": "https://www.compraspublicas.gob.ec"
        }
    else:
        return {
            "Entidad": "CNEL EP - UNIDAD DE NEGOCIO EL ORO",
            "Categoría": "CONSTRUCCION DE REDES DE DISTRIBUCION",
            "Objeto": "EOR Construccion de redes electricas... ZONA 2 CAF GD",
            "Código": "COTO-CNELEP-2025-44",
            "Plazo": "150 Días",
            "Contratista": "CONSORCIO REDES HUNTER",
            "Rep_Legal": "CRISTHIAN MANUEL ROMERO FREIRE",
            "Monto": "$ 499.654,23",
            "Link": "https://www.compraspublicas.gob.ec"
        }

ficha = obtener_ficha_tecnica(contrato_seleccionado)

# --- DATOS GRÁFICOS (SIMULACIÓN AUTOMÁTICA) ---
def obtener_datos_graficos(zona):
    months = ['Nov', 'Dic', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    # Datos base para que el dashboard no se vea vacío
    if zona == "ZONA 1 - SECTOR CAMARONERO":
        monto = 399743.03
    else:
        monto = 499654.23
        
    df = pd.DataFrame({
        'Mes': months,
        'Físico Real (%)': [0, 5, 12, 25, 40, 55, 70, 85],
        'Programado (%)': [0, 8, 15, 30, 50, 65, 80, 100],
        'Devengo ($)': [x * (monto/1000) for x in [0, 2, 8, 15, 25, 35, 50, 75]],
        'Acumulado ($)': [x * (monto/100) for x in [0, 2, 8, 15, 25, 35, 50, 75]],
        'Anticipo ($)': [20000, 18000, 15000, 12000, 8000, 5000, 2000, 0]
    })
    return df, monto

df_data, monto_obra = obtener_datos_graficos(contrato_seleccionado)

# --- VISUALIZACIÓN FICHA TÉCNICA ---
def dibujar_ficha(datos):
    html_table = f"""
    <table class="ficha-tecnica">
        <tr><th colspan="4" style="text-align:center;">FICHA TÉCNICA (CONTRATO DE OBRA)</th></tr>
        <tr><td><strong>Objeto:</strong></td><td colspan="3">{datos['Objeto']}</td></tr>
        <tr>
            <td><strong>Contratista:</strong></td><td>{datos['Contratista']}</td>
            <td><strong>Monto:</strong></td><td>{datos['Monto']}</td>
        </tr>
    </table>
    """
    st.markdown(html_table, unsafe_allow_html=True)

# ==============================================================================
# MÓDULO 1: RDO WEB (FORMULARIO DE INGRESO)
# ==============================================================================
if modulo == "MÓDULO 1: RDO (Lista de 19 Puntos)":
    st.markdown(f'<div class="main-header">Módulo 1: Registro Diario de Obra (RDO)</div>', unsafe_allow_html=True)
    dibujar_ficha(ficha)
    st.warning("Formulario listo para ingreso de datos diarios.")

    # FORMULARIO
    with st.form("rdo_form", clear_on_submit=False): # No limpiar auto para que vea el mensaje
        
        # A. GENERALES (CAMPOS VACÍOS O DEFECTO)
        st.markdown("### A. Datos Generales")
        c1, c2 = st.columns(2)
        fecha_rdo = c1.date_input("1. Fechas de Ejecución", date.today())
        c2.text_input("4. Día de ejecución", "", placeholder="Ej: Día 15")
        
        c3, c4 = st.columns(2)
        c3.text_input("2. Datos Económicos del Contrato", "$ 67,490.10 (Fisc.)", disabled=True)
        c4.text_input("3. Dato Económico total de los Proyectos", ficha['Monto'], disabled=True)

        # B. CAMPO
        st.markdown("### B. Condiciones de Campo")
        col_clima, col_inc = st.columns(2)
        col_clima.selectbox("5. Condiciones climáticas", ["", "Soleado", "Nublado", "Lluvia", "Tormenta"], index=0)
        col_inc.selectbox("19. Registro de Incidentes", ["Sin Novedades", "Con Novedades"], index=0)

        # C. CONTROL DE AVANCE (CORREGIDO Y MEJORADO)
        st.markdown("### C. Control de Avance y Desempeño")
        st.info("**6. Progreso General del Contrato de Obra:**")
        
        m1, m2, m3 = st.columns(3)
        
        # Campos inicializados en 0.00 para llenado
        pct_avance = m1.number_input("6.i. % de Avance del Día", min_value=0.0, max_value=100.0, value=0.0, step=0.01)
        monto_avance = m2.number_input("6.i. $ de Avance del Día", min_value=0.0, value=0.0, step=100.0)
        
        # Calculado visual (si el usuario ingresa monto, esto lo refleja)
        m3.metric("6.i. Avance Avaluado (Automático)", f"$ {monto_avance:,.2f}")

        # --- MEJORA DEL PUNTO 6.ii (HITOS) ---
        st.markdown("**6.ii. Avance prorrateado por Hito (Ingreso Simplificado)**")
        col_h1, col_h2 = st.columns(2)
        
        # En lugar de texto confuso, usamos inputs numéricos claros
        hito1 = col_h1.number_input("Avance Hito 1 (Civil) %", min_value=0.0, max_value=100.0, value=0.0)
        hito2 = col_h2.number_input("Avance Hito 2 (Eléctrico) %", min_value=0.0, max_value=100.0, value=0.0)
        
        # Cálculo automático del promedio (opcional, solo visual)
        promedio_hitos = (hito1 + hito2) / 2
        st.caption(f"Promedio Ponderado Estimado: {promedio_hitos:.2f}%")
        # -------------------------------------

        st.text_input("7. Indicadores de Desempeño (CPI/SPI)", "", placeholder="Ej: CPI: 1.0, SPI: 1.0")
        
        cc1, cc2 = st.columns(2)
        cc1.selectbox("14. Control Tabla de Cantidades", ["", "SI - Verificado", "NO"], index=0)
        cc2.text_input("15. Porcentaje Total Proyectos", "", placeholder="Ej: 12.5%")

        # Gráfico (Se mantiene visualización)
        st.markdown("**8. Curva de Avance – Valor Ganado** (Visualización Referencial)")
        fig_rdo = go.Figure()
        fig_rdo.add_trace(go.Scatter(y=[0, 10, 20], mode='lines', name='Referencia'))
        fig_rdo.update_layout(height=150, margin=dict(t=10, b=10))
        st.plotly_chart(fig_rdo, use_container_width=True)

        # D. ADMIN
        st.markdown("### D. Administrativo y Detalle")
        l1, l2, l3 = st.columns(3)
        l1.text_input("16. Contratos Complementarios", "N/A")
        l2.text_input("17. Órdenes de Trabajo", "", placeholder="Nro OT")
        l3.text_input("18. Incremento Cantidades", "0.00%")

        st.text_area("13. Personal y Equipos", "", placeholder="Detalle cuadrilla y maquinaria...")
        st.text_area("10. Actividades Ejecutadas", "", placeholder="Descripción de trabajos...")
        st.text_area("9. Observaciones Fiscalización", "")

        st.markdown("**11. Registro Fotográfico & 12. Firmas**")
        c_foto, c_firma = st.columns(2)
        c_foto.file_uploader("Cargar Fotos", accept_multiple_files=True)
        c_firma.text_input("12. Firma Responsable", "Ing. Cristhian San Martin")

        # BOTÓN DE GUARDADO
        submitted = st.form_submit_button("GUARDAR RDO DIARIO")
    
    # --- LÓGICA DE GUARDADO Y MENSAJE ---
    if submitted:
        # 1. Mostrar Mensaje de Éxito
        fecha_str = fecha_rdo.strftime("%d/%m/%Y")
        st.success(f"✅ REGISTRO DEL DIA {fecha_str}, GUARDADO CORRECTAMENTE.")
        
        # 2. Botón/Link para ir al Dashboard
        st.markdown("---")
        col_msg, col_btn = st.columns([3, 1])
        col_msg.info("Los datos han sido sincronizados. Puede visualizar el impacto en los indicadores ahora.")
        
        # Botón mágico para cambiar de pestaña
        if col_btn.button("👉 Ver avance en DASHBOARD"):
            st.session_state.navegacion_radio = "MÓDULO 2: DASHBOARD (Lista de 8 Puntos)"
            cambiar_pagina("MÓDULO 2: DASHBOARD (Lista de 8 Puntos)")
            st.rerun() # Recarga la página para mostrar el dashboard

# ==============================================================================
# MÓDULO 2: DASHBOARD
# ==============================================================================
elif modulo == "MÓDULO 2: DASHBOARD (Lista de 8 Puntos)":
    st.markdown(f'<div class="main-header">Módulo 2: Dashboard de Desempeño</div>', unsafe_allow_html=True)
    dibujar_ficha(ficha)
    
    st.markdown(f"#### 1. Fecha de emisión: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # KPIs
    st.markdown("#### 2. % de Avance Acumulado (Tiempo Real)")
    k1, k2, k3 = st.columns(3)
    k1.metric("Avance Físico Global", "35.5%", "2.1% esta semana")
    k2.metric("Hito 1: Obra Civil", "85.0%")
    k3.metric("Hito 2: Eléctrico", "12.5%")

    st.markdown("---")

    # Gráficos
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("3. Gráfico Resumen Global Acumulado")
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=df_data['Mes'], y=df_data['Físico Real (%)'], fill='tozeroy', name='Ejecutado'))
        st.plotly_chart(fig3, use_container_width=True)
        
        st.subheader("5. Avance de Pagos (Acumulado)")
        fig5 = px.bar(df_data, x='Mes', y='Acumulado ($)', color_discrete_sequence=['green'])
        st.plotly_chart(fig5, use_container_width=True)
        
        st.subheader("7. Pagos Mensuales")
        fig7 = px.bar(df_data, x='Mes', y='Devengo ($)')
        st.plotly_chart(fig7, use_container_width=True)

    with c2:
        st.subheader("4. Avance Físico por Proyecto/Mes")
        fig4 = px.line(df_data, x='Mes', y='Físico Real (%)', markers=True)
        st.plotly_chart(fig4, use_container_width=True)
        
        st.subheader("6. % Avance vs Dólares")
        fig6 = go.Figure()
        fig6.add_trace(go.Scatter(x=df_data['Mes'], y=df_data['Físico Real (%)'], name='%'))
        fig6.add_trace(go.Bar(x=df_data['Mes'], y=df_data['Devengo ($)'], name='$', yaxis='y2', opacity=0.3))
        fig6.update_layout(yaxis2=dict(overlaying='y', side='right'))
        st.plotly_chart(fig6, use_container_width=True)
        
        st.subheader("8. Devengo de Anticipo")
        fig8 = px.area(df_data, x='Mes', y='Anticipo ($)', color_discrete_sequence=['red'])
        st.plotly_chart(fig8, use_container_width=True)
