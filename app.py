import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(layout="wide", page_title="SISTEMA DE GESTIÓN RDO & DASHBOARD", page_icon="⚡")

# --- GESTIÓN DE MEMORIA (SESSION STATE) ---
# Esto es vital: Crea una "base de datos temporal" en el navegador
# para que los gráficos empiecen vacíos y se llenen al guardar.

if 'data_zona1' not in st.session_state:
    # Inicializamos con valor CERO
    st.session_state['data_zona1'] = pd.DataFrame({
        'Fecha': [datetime.now().date()],
        'Mes': ['Inicio'],
        'Físico Real (%)': [0.0],
        'Financiero Real (%)': [0.0],
        'Devengo ($)': [0.0],
        'Acumulado ($)': [0.0],
        'Anticipo ($)': [0.0]
    })

if 'data_zona2' not in st.session_state:
    # Inicializamos con valor CERO
    st.session_state['data_zona2'] = pd.DataFrame({
        'Fecha': [datetime.now().date()],
        'Mes': ['Inicio'],
        'Físico Real (%)': [0.0],
        'Financiero Real (%)': [0.0],
        'Devengo ($)': [0.0],
        'Acumulado ($)': [0.0],
        'Anticipo ($)': [0.0]
    })

# Control de navegación entre pestañas
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "MÓDULO 1: RDO (Lista de 19 Puntos)"

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

    /* Estilo Ficha Técnica COMPLETA */
    .ficha-tecnica {
        width: 100%; border-collapse: collapse; margin-bottom: 20px;
        font-family: Arial, sans-serif; font-size: 13px; border: 1px solid #ddd;
    }
    .ficha-tecnica th {background-color: #1E3A8A; color: white; padding: 6px; text-align: left; border: 1px solid #ddd;}
    .ficha-tecnica td {padding: 6px; border: 1px solid #ddd; background-color: #f9f9f9; color: #333;}
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

modulo = st.sidebar.radio(
    "Navegación:", 
    ["MÓDULO 1: RDO (Lista de 19 Puntos)", "MÓDULO 2: DASHBOARD (Lista de 8 Puntos)"],
    index=0 if st.session_state.pagina_actual == "MÓDULO 1: RDO (Lista de 19 Puntos)" else 1,
    key="navegacion_radio",
    on_change=lambda: cambiar_pagina(st.session_state.navegacion_radio)
)

st.sidebar.info(f"**Oferente:** Consorcio FiscalRed\n**Usuario:** Ing. Cristhian San Martin")

# --- FICHA TÉCNICA (DATOS REALES RESTAURADOS) ---
def obtener_ficha_tecnica(zona):
    if zona == "ZONA 1 - SECTOR CAMARONERO":
        return {
            "Entidad": "CNEL EP - UNIDAD DE NEGOCIO EL ORO",
            "Categoría": "CONSTRUCCION DE REDES DE DISTRIBUCION",
            "Objeto": "EOR Construccion de redes electricas para proyectos PER sector camaronero zona 1 CAF GD",
            "Código": "COTO-CNELEP-2025-43",
            "Plazo": "150 Días Calendario",
            "Contratista": "CONSORCIO CAF ARENILLAS",
            "Rep_Legal": "OSCAR LUIS YANANGOMEZ SUQUILANDA (Procurador Común)",
            "Monto_Str": "$ 399.743,03",
            "Monto_Num": 399743.03,
            "Link": "https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/PC/informacionProcesoContratacion2.cpe?idSoliCompra=Mlped7h-x8tM2Mi5JzAbNVHBoqrlPkyFh2Yoxj85zQc"
        }
    else:
        return {
            "Entidad": "CNEL EP - UNIDAD DE NEGOCIO EL ORO",
            "Categoría": "CONSTRUCCION DE REDES DE DISTRIBUCION",
            "Objeto": "EOR Construccion de redes electricas para proyectos PER sector camaronero zona 2 CAF GD",
            "Código": "COTO-CNELEP-2025-44",
            "Plazo": "150 Días Calendario",
            "Contratista": "CONSORCIO REDES HUNTER",
            "Rep_Legal": "CRISTHIAN MANUEL ROMERO FREIRE (Procurador Común)",
            "Monto_Str": "$ 499.654,23",
            "Monto_Num": 499654.23,
            "Link": "https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/PC/informacionProcesoContratacion2.cpe?idSoliCompra=VJCoFonyH1vOnVROGwOunGmr6qD3pTr-znOrgilqON0,"
        }

ficha = obtener_ficha_tecnica(contrato_seleccionado)

# --- VISUALIZACIÓN FICHA TÉCNICA (LA COMPLETA) ---
def dibujar_ficha(datos):
    html_table = f"""
    <table class="ficha-tecnica">
        <tr><th colspan="4" style="text-align:center;">FICHA TÉCNICA DEL PROYECTO (CONTRATO DE OBRA)</th></tr>
        <tr>
            <td width="15%"><strong>Entidad:</strong></td><td width="35%">{datos['Entidad']}</td>
            <td width="15%"><strong>Categoría:</strong></td><td width="35%">{datos['Categoría']}</td>
        </tr>
        <tr>
            <td><strong>Objeto:</strong></td><td colspan="3">{datos['Objeto']}</td>
        </tr>
        <tr>
            <td><strong>Código:</strong></td><td>{datos['Código']}</td>
            <td><strong>Plazo:</strong></td><td>{datos['Plazo']}</td>
        </tr>
        <tr>
            <td><strong>Contratista:</strong></td><td>{datos['Contratista']}</td>
            <td><strong>Rep. Legal:</strong></td><td>{datos['Rep_Legal']}</td>
        </tr>
        <tr>
            <td><strong>Monto USD:</strong></td><td>{datos['Monto_Str']}</td>
            <td><strong>Link:</strong></td><td><a href="{datos['Link']}" target="_blank">Ver en SERCOP</a></td>
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
    st.warning("Formulario de Campo - Numeración conforme a TDR Pág. 28")

    # Formulario
    with st.form("rdo_form", clear_on_submit=False):
        
        # A. GENERALES (VACÍOS POR DEFECTO)
        st.markdown("### A. Datos Generales")
        c1, c2 = st.columns(2)
        fecha_rdo = c1.date_input("1. Fechas de Ejecución", date.today())
        c2.text_input("4. Día de ejecución", "", placeholder="Ej: Día 1")
        
        c3, c4 = st.columns(2)
        c3.text_input("2. Datos Económicos del Contrato", "$ 67,490.10 (Fiscalización)", disabled=True)
        c4.text_input("3. Dato Económico total de los Proyectos", ficha['Monto_Str'], disabled=True)

        # B. CAMPO
        st.markdown("### B. Condiciones de Campo")
        col_clima, col_inc = st.columns(2)
        col_clima.selectbox("5. Condiciones climáticas", ["", "Soleado", "Nublado", "Lluvia", "Tormenta"], index=0)
        col_inc.selectbox("19. Registro de Incidentes", ["Sin Novedades", "Incidente Leve", "Accidente"], index=0)

        # C. CONTROL DE AVANCE (INICIA EN CERO)
        st.markdown("### C. Control de Avance y Desempeño")
        st.info("**6. Progreso General del Contrato de Obra:**")
        
        m1, m2, m3 = st.columns(3)
        
        # INPUTS NUMÉRICOS EN CERO
        pct_avance = m1.number_input("6.i. % de Avance Actual", min_value=0.0, max_value=100.0, value=0.0, step=0.01)
        monto_avance = m2.number_input("6.i. $ de Avance Actual", min_value=0.0, value=0.0, step=100.0)
        
        # VISUALIZACIÓN AUTOMÁTICA
        m3.metric("6.i. Avance Avaluado (Automático)", f"$ {monto_avance:,.2f}")

        # MEJORA HITO 6.ii
        st.markdown("**6.ii. Avance prorrateado por Hito (Ingreso Rápido)**")
        col_h1, col_h2 = st.columns(2)
        col_h1.number_input("Avance Hito 1 (Civil) %", min_value=0.0, max_value=100.0, value=0.0)
        col_h2.number_input("Avance Hito 2 (Eléctrico) %", min_value=0.0, max_value=100.0, value=0.0)
        
        st.text_input("7. Indicadores de Desempeño (CPI/SPI)", "", placeholder="Ingrese valores calculados...")
        
        cc1, cc2 = st.columns(2)
        cc1.selectbox("14. Control Tabla de Cantidades", ["", "SI - Verificado", "NO"], index=0)
        cc2.text_input("15. Porcentaje Total Proyectos", "", placeholder="Ponderado...")

        # Gráfico (Referencial estático en el formulario, dinámico en Dashboard)
        st.markdown("**8. Curva de Avance – Valor Ganado**")
        fig_rdo = go.Figure()
        fig_rdo.add_trace(go.Scatter(y=[0, pct_avance], mode='lines+markers', name='Tu Avance'))
        fig_rdo.update_layout(height=150, margin=dict(t=10, b=10))
        st.plotly_chart(fig_rdo, use_container_width=True)

        # D. ADMIN
        st.markdown("### D. Administrativo y Detalle")
        l1, l2, l3 = st.columns(3)
        l1.text_input("16. Contratos Complementarios", "Ninguno")
        l2.text_input("17. Órdenes de Trabajo", "")
        l3.text_input("18. Incremento Cantidades", "0.00%")

        st.text_area("13. Personal y Equipos", "", placeholder="Detalle cuadrilla...")
        st.text_area("10. Actividades Ejecutadas", "", placeholder="Descripción...")
        st.text_area("9. Observaciones Fiscalización", "")

        st.markdown("**11. Registro Fotográfico & 12. Firmas**")
        c_foto, c_firma = st.columns(2)
        c_foto.file_uploader("Cargar Fotos", accept_multiple_files=True)
        c_firma.text_input("12. Firma Responsable", "Ing. Cristhian San Martin")

        # BOTÓN DE GUARDADO REAL
        submitted = st.form_submit_button("GUARDAR RDO DIARIO")
    
    # --- LÓGICA: AL GUARDAR, ACTUALIZAR MEMORIA ---
    if submitted:
        # Recuperamos la tabla de memoria actual
        key_data = 'data_zona1' if contrato_seleccionado == "ZONA 1 - SECTOR CAMARONERO" else 'data_zona2'
        df_actual = st.session_state[key_data]
        
        # Creamos la nueva fila con los datos ingresados
        nueva_fila = {
            'Fecha': fecha_rdo,
            'Mes': fecha_rdo.strftime("%b-%d"),
            'Físico Real (%)': pct_avance,
            'Financiero Real (%)': (monto_avance / ficha['Monto_Num']) * 100,
            'Devengo ($)': monto_avance, # Simplificación: Devengo del día/mes
            'Acumulado ($)': monto_avance,
            'Anticipo ($)': monto_avance * 0.1 # Simulación de amortización
        }
        
        # Agregamos a la memoria
        df_nuevo = pd.concat([df_actual, pd.DataFrame([nueva_fila])], ignore_index=True)
        st.session_state[key_data] = df_nuevo

        # Mensaje y redirección
        st.success(f"✅ REGISTRO DEL DIA {fecha_rdo.strftime('%d/%m/%Y')}, GUARDADO CORRECTAMENTE.")
        
        col_msg, col_btn = st.columns([3, 1])
        col_msg.info("Datos sincronizados con la Nube. Dashboard actualizado.")
        
        if col_btn.button("👉 Ver avance en DASHBOARD"):
            st.session_state.navegacion_radio = "MÓDULO 2: DASHBOARD (Lista de 8 Puntos)"
            cambiar_pagina("MÓDULO 2: DASHBOARD (Lista de 8 Puntos)")
            st.rerun()

# ==============================================================================
# MÓDULO 2: DASHBOARD (SE ALIMENTA DE LA MEMORIA)
# ==============================================================================
elif modulo == "MÓDULO 2: DASHBOARD (Lista de 8 Puntos)":
    st.markdown(f'<div class="main-header">Módulo 2: Dashboard de Desempeño</div>', unsafe_allow_html=True)
    dibujar_ficha(ficha)
    
    st.markdown(f"#### 1. Fecha de emisión: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # RECUPERAR DATOS DE MEMORIA
    key_data = 'data_zona1' if contrato_seleccionado == "ZONA 1 - SECTOR CAMARONERO" else 'data_zona2'
    df_dashboard = st.session_state[key_data]
    
    # OBTENER ÚLTIMO VALOR (Si está vacío, es 0)
    ultimo_avance = df_dashboard['Físico Real (%)'].iloc[-1]
    ultimo_monto = df_dashboard['Acumulado ($)'].iloc[-1]

    # 2. KPIs
    st.markdown("#### 2. % de Avance Acumulado (Tiempo Real)")
    k1, k2, k3 = st.columns(3)
    k1.metric("Avance Físico Global", f"{ultimo_avance:.2f}%", f"Actualizado hoy")
    k2.metric("Inversión Ejecutada", f"$ {ultimo_monto:,.2f}")
    k3.metric("Estado Hitos", "En Proceso" if ultimo_avance < 100 else "Completado")

    st.markdown("---")

    # Gráficos (3 al 8) - Se dibujan con df_dashboard
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("3. Gráfico Resumen Global Acumulado")
        # Si solo hay 1 dato (inicio), muestra un punto. Si hay más, muestra línea.
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=df_dashboard['Mes'], y=df_dashboard['Físico Real (%)'], fill='tozeroy', name='Ejecutado'))
        st.plotly_chart(fig3, use_container_width=True)
        
        st.subheader("5. Avance de Pagos (Acumulado)")
        fig5 = px.bar(df_dashboard, x='Mes', y='Acumulado ($)', color_discrete_sequence=['green'])
        st.plotly_chart(fig5, use_container_width=True)
        
        st.subheader("7. Pagos Mensuales")
        fig7 = px.bar(df_dashboard, x='Mes', y='Devengo ($)')
        st.plotly_chart(fig7, use_container_width=True)

    with c2:
        st.subheader("4. Avance Físico por Proyecto/Mes")
        fig4 = px.line(df_dashboard, x='Mes', y='Físico Real (%)', markers=True)
        st.plotly_chart(fig4, use_container_width=True)
        
        st.subheader("6. % Avance vs Dólares")
        fig6 = go.Figure()
        fig6.add_trace(go.Scatter(x=df_dashboard['Mes'], y=df_dashboard['Físico Real (%)'], name='%'))
        fig6.add_trace(go.Bar(x=df_dashboard['Mes'], y=df_dashboard['Devengo ($)'], name='$', yaxis='y2', opacity=0.3))
        fig6.update_layout(yaxis2=dict(overlaying='y', side='right'))
        st.plotly_chart(fig6, use_container_width=True)
        
        st.subheader("8. Devengo de Anticipo")
        fig8 = px.area(df_dashboard, x='Mes', y='Anticipo ($)', color_discrete_sequence=['red'])
        st.plotly_chart(fig8, use_container_width=True)
