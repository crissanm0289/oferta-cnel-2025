import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(layout="wide", page_title="SISTEMA DE GESTIÓN RDO & DASHBOARD", page_icon="⚡")

# --- GESTIÓN DE MEMORIA (SESSION STATE) ---
if 'data_zona1' not in st.session_state:
    st.session_state['data_zona1'] = pd.DataFrame({
        'Fecha': [date(2025, 1, 1)],
        'Día N': ['Inicio'],
        'Físico Acum (%)': [0.0],
        'Financiero Acum ($)': [0.0],
        'Físico Diario (%)': [0.0],
        'Inversión Diaria ($)': [0.0],
        'Saldo ($)': [0.0],
        'Detalle': ['Inicio de Contrato'],
        'Fotos': [0]
    })

if 'data_zona2' not in st.session_state:
    st.session_state['data_zona2'] = pd.DataFrame({
        'Fecha': [date(2025, 1, 1)],
        'Día N': ['Inicio'],
        'Físico Acum (%)': [0.0],
        'Financiero Acum ($)': [0.0],
        'Físico Diario (%)': [0.0],
        'Inversión Diaria ($)': [0.0],
        'Saldo ($)': [0.0],
        'Detalle': ['Inicio de Contrato'],
        'Fotos': [0]
    })

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
        font-family: Arial, sans-serif; font-size: 12px; border: 1px solid #ddd;
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

# --- FICHA TÉCNICA (DATOS REALES Y COMPLETOS) ---
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
# MÓDULO 1: RDO WEB (19 PUNTOS)
# ==============================================================================
if modulo == "MÓDULO 1: RDO (Lista de 19 Puntos)":
    st.markdown(f'<div class="main-header">Módulo 1: Registro Diario de Obra (RDO)</div>', unsafe_allow_html=True)
    dibujar_ficha(ficha)

    key_data = 'data_zona1' if contrato_seleccionado == "ZONA 1 - SECTOR CAMARONERO" else 'data_zona2'
    df_actual = st.session_state[key_data]
    
    # --- MODO EDICIÓN ---
    modo_edicion = st.checkbox("🔓 Modificar Registro Anterior (Corrección de Historial)")
    
    defaults = {
        "fecha": date.today(),
        "dia_n": "",
        "clima_idx": 0,
        "incidente_idx": 0,
        "pct_acum": 0.0,
        "monto_acum": 0.0,
        "cpi": 0.0,
        "spi": 0.0,
        "personal": "",
        "actividad": "",
        "obs": "",
        "firma": "",
        "ot": "",
        "contrato_comp": "N/A",
        "incremento": "0.00%",
        "porcentaje_proy": ""
    }
    indice_a_editar = -1

    if modo_edicion:
        st.info("⚠️ MODO EDICIÓN: Seleccione el día que desea corregir.")
        opciones = df_actual.iloc[1:]['Fecha'].astype(str) + " - " + df_actual.iloc[1:]['Día N']
        if not opciones.empty:
            seleccion = st.selectbox("Seleccione Registro:", opciones)
            indice_a_editar = df_actual[df_actual['Fecha'].astype(str) + " - " + df_actual['Día N'] == seleccion].index[0]
            fila = df_actual.loc[indice_a_editar]
            
            defaults["fecha"] = fila['Fecha']
            defaults["dia_n"] = fila['Día N']
            defaults["pct_acum"] = float(fila['Físico Acum (%)'])
            defaults["monto_acum"] = float(fila['Financiero Acum ($)'])
            defaults["actividad"] = fila['Detalle']
            defaults["personal"] = "Personal registrado..." 
            defaults["firma"] = "Ing. Cristhian San Martin"
        else:
            st.write("No hay registros previos para editar.")

    # --- FORMULARIO CON 19 PUNTOS NUMERADOS ---
    with st.form("rdo_form", clear_on_submit=False):
        
        st.markdown("### A. Datos Generales")
        c1, c2 = st.columns(2)
        in_fecha = c1.date_input("1. Fechas de Ejecución", defaults["fecha"])
        in_dia = c2.text_input("4. Día de ejecución (Obligatorio)", defaults["dia_n"], placeholder="Ej: Día 15")
        
        c3, c4 = st.columns(2)
        c3.text_input("2. Datos Económicos del Contrato", "$ 67,490.10 (Fiscalización)", disabled=True)
        c4.text_input("3. Dato Económico total de los Proyectos", ficha['Monto_Str'], disabled=True)

        st.markdown("### B. Condiciones de Campo")
        col_clima, col_inc = st.columns(2)
        in_clima = col_clima.selectbox("5. Condiciones climáticas (Obligatorio)", ["", "Soleado", "Nublado", "Lluvia", "Tormenta"], index=defaults["clima_idx"])
        in_inc = col_inc.selectbox("19. Registro de Incidentes o accidentes", ["Sin Novedades", "Incidente Leve", "Accidente"], index=defaults["incidente_idx"])

        st.markdown("### C. Control de Avance")
        st.info(f"**6. Progreso General del Contrato de Obra (Acumulado):**")
        
        m1, m2, m3 = st.columns(3)
        in_pct = m1.number_input("6.i. % de Avance", min_value=0.0, max_value=100.0, value=defaults["pct_acum"], step=0.01)
        in_monto = m2.number_input("6.i. $ de Avance", min_value=0.0, value=defaults["monto_acum"], step=100.0)
        m3.metric("6.i. Avance Avaluado", f"$ {in_monto:,.2f}")

        st.markdown("**6.ii. Avance prorrateado de los proyectos por Hito**")
        col_h1, col_h2 = st.columns(2)
        col_h1.number_input("6.ii. Hito 1 (Civil) %", min_value=0.0, max_value=100.0, value=0.0)
        col_h2.number_input("6.ii. Hito 2 (Eléctrico) %", min_value=0.0, max_value=100.0, value=0.0)
        
        st.markdown("**7. Indicadores de Desempeño y estimaciones**")
        col_c, col_s = st.columns(2)
        in_cpi = col_c.number_input("7. CPI (Costo)", value=defaults["cpi"], step=0.01, help=">1: Ahorro")
        in_spi = col_s.number_input("7. SPI (Cronograma)", value=defaults["spi"], step=0.01, help=">1: Adelantado")
        
        cc1, cc2 = st.columns(2)
        cc1.selectbox("14. Control mediante Tabla de cantidades y Reporte", ["", "SI - Verificado", "NO"], index=0)
        cc2.text_input("15. Porcentaje total de los proyectos", defaults["porcentaje_proy"], placeholder="Ponderado...")

        st.markdown("**8. Curva de Avance – Valor Ganado**")
        fig_rdo = go.Figure()
        fig_rdo.add_trace(go.Scatter(y=[0, in_pct], mode='lines+markers', name='Tu Avance'))
        fig_rdo.update_layout(height=150, margin=dict(t=10, b=10))
        st.plotly_chart(fig_rdo, use_container_width=True)

        st.markdown("### D. Administrativo y Detalle")
        l1, l2, l3 = st.columns(3)
        l1.text_input("16. Registro de Contratos Complementarios", defaults["contrato_comp"])
        l2.text_input("17. Registro de Ordenes de trabajo", defaults["ot"])
        l3.text_input("18. Registro de Incremento de cantidades", defaults["incremento"])

        in_personal = st.text_area("13. Personal y Equipos (Obligatorio)", defaults["personal"], placeholder="Detalle cuadrilla...")
        in_activ = st.text_area("10. Actividades ejecutadas en el día (Obligatorio)", defaults["actividad"], placeholder="Descripción...")
        st.text_area("9. Observaciones de fiscalización", defaults["obs"])

        st.markdown("**11. Registro fotográfico & 12. Firmas**")
        c_foto, c_firma = st.columns(2)
        in_fotos = c_foto.file_uploader("11. Registro fotográfico (Obligatorio)", accept_multiple_files=True)
        in_firma = c_firma.text_input("12. Firmas de responsabilidad (Obligatorio)", defaults["firma"])

        btn_label = "GUARDAR CAMBIOS" if modo_edicion else "GUARDAR RDO DIARIO"
        submitted = st.form_submit_button(btn_label)
    
    # --- VALIDACIÓN Y GUARDADO ---
    if submitted:
        errores = []
        
        # 1. VALIDACIÓN DE CAMPOS VACÍOS
        if not in_dia: errores.append("• Falta: 4. Día de ejecución")
        if in_clima == "": errores.append("• Falta: 5. Condiciones climáticas")
        if not in_personal: errores.append("• Falta: 13. Personal y Equipos")
        if not in_activ: errores.append("• Falta: 10. Actividades ejecutadas")
        if not in_firma: errores.append("• Falta: 12. Firmas de responsabilidad")
        if not modo_edicion and not in_fotos: errores.append("• Falta: 11. Registro fotográfico")
        
        # 2. VALIDACIÓN DE FECHA DUPLICADA
        if not modo_edicion:
            fechas_existentes = df_actual['Fecha'].tolist()
            if in_fecha in fechas_existentes:
                 errores.append(f"⛔ LA FECHA {in_fecha.strftime('%d/%m/%Y')} YA EXISTE.\n   ➡️ Para corregir, active '🔓 Modificar Registro Anterior'.")

        if errores:
            st.error("⚠️ NO SE PUDO GUARDAR. REVISE LO SIGUIENTE:")
            for e in errores:
                st.write(e)
        else:
            # 3. CÁLCULOS
            if modo_edicion:
                idx_ref = indice_a_editar - 1 if indice_a_editar > 0 else 0
                prev_pct = df_actual.iloc[idx_ref]['Físico Acum (%)']
                prev_monto = df_actual.iloc[idx_ref]['Financiero Acum ($)']
            else:
                prev_pct = df_actual.iloc[-1]['Físico Acum (%)']
                prev_monto = df_actual.iloc[-1]['Financiero Acum ($)']

            diario_pct = in_pct - prev_pct
            diario_monto = in_monto - prev_monto
            if diario_pct < 0: diario_pct = 0
            if diario_monto < 0: diario_monto = 0

            nueva_fila = {
                'Fecha': in_fecha,
                'Día N': in_dia,
                'Físico Acum (%)': in_pct,
                'Financiero Acum ($)': in_monto,
                'Físico Diario (%)': diario_pct,
                'Inversión Diaria ($)': diario_monto,
                'Saldo ($)': ficha['Monto_Num'] - in_monto,
                'Detalle': in_activ,
                'Fotos': len(in_fotos) if in_fotos else 0
            }

            if modo_edicion:
                for col, val in nueva_fila.items():
                    df_actual.at[indice_a_editar, col] = val
                st.session_state[key_data] = df_actual
                st.success(f"✅ REGISTRO '{in_dia}' CORREGIDO EXITOSAMENTE.")
            else:
                df_nuevo = pd.concat([df_actual, pd.DataFrame([nueva_fila])], ignore_index=True)
                st.session_state[key_data] = df_nuevo
                st.success(f"✅ REGISTRO DEL DÍA {in_fecha} GUARDADO CORRECTAMENTE.")

            st.markdown("---")
            c_msg, c_btn = st.columns([3, 1])
            c_msg.info("Base de datos actualizada.")
            if c_btn.button("👉 Ir al DASHBOARD"):
                st.session_state.navegacion_radio = "MÓDULO 2: DASHBOARD (Lista de 8 Puntos)"
                cambiar_pagina("MÓDULO 2: DASHBOARD (Lista de 8 Puntos)")
                st.rerun()

# ==============================================================================
# MÓDULO 2: DASHBOARD (8 PUNTOS)
# ==============================================================================
elif modulo == "MÓDULO 2: DASHBOARD (Lista de 8 Puntos)":
    st.markdown(f'<div class="main-header">Módulo 2: Dashboard de Desempeño</div>', unsafe_allow_html=True)
    dibujar_ficha(ficha)
    st.markdown(f"#### 1. Fecha de emisión: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    key_data = 'data_zona1' if contrato_seleccionado == "ZONA 1 - SECTOR CAMARONERO" else 'data_zona2'
    df_dashboard = st.session_state[key_data].copy()

    if len(df_dashboard) > 1:
        df_final = df_dashboard.iloc[1:].reset_index(drop=True)
    else:
        df_final = df_dashboard

    st.markdown("### 2. % de Avance Acumulado (Tabla Detallada)")
    cols_mostrar = ['Fecha', 'Día N', 'Físico Diario (%)', 'Inversión Diaria ($)', 'Físico Acum (%)', 'Financiero Acum ($)', 'Saldo ($)']
    
    st.dataframe(
        df_final[cols_mostrar].style.format({
            'Físico Diario (%)': "{:.2f}%",
            'Inversión Diaria ($)': "$ {:,.2f}",
            'Físico Acum (%)': "{:.2f}%",
            'Financiero Acum ($)': "$ {:,.2f}",
            'Saldo ($)': "$ {:,.2f}"
        }),
        use_container_width=True,
        height=300
    )

    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("3. Gráfico de Resumen de avance Global Acumulado")
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=df_final['Fecha'], y=df_final['Físico Acum (%)'], fill='tozeroy', name='Físico Real'))
        st.plotly_chart(fig3, use_container_width=True)
        
        st.subheader("5. Gráficos de Avance de Pagos")
        fig5 = px.line(df_final, x='Fecha', y='Financiero Acum ($)', markers=True)
        st.plotly_chart(fig5, use_container_width=True)
        
        st.subheader("7. Gráfico de Pagos mensuales")
        fig7 = px.bar(df_final, x='Fecha', y='Inversión Diaria ($)', title="Planillado por Registro")
        st.plotly_chart(fig7, use_container_width=True)

    with c2:
        st.subheader("4. Gráfico de Avance físico total por proyecto por mes")
        fig4 = px.line(df_final, x='Fecha', y='Físico Acum (%)', markers=True)
        st.plotly_chart(fig4, use_container_width=True)
        
        st.subheader("6. Gráfico de Avance porcentual y en dólares")
        fig6 = go.Figure()
        fig6.add_trace(go.Scatter(x=df_final['Fecha'], y=df_final['Físico Acum (%)'], name='% Avance'))
        fig6.add_trace(go.Scatter(x=df_final['Fecha'], y=df_final['Financiero Acum ($)'], name='$ Inversión', yaxis='y2', line=dict(dash='dot')))
        fig6.update_layout(yaxis2=dict(overlaying='y', side='right', title="Monto USD"))
        st.plotly_chart(fig6, use_container_width=True)
        
        st.subheader("8. Gráfico de Devengo de anticipo")
        fig8 = px.area(df_final, x='Fecha', y='Inversión Diaria ($)', color_discrete_sequence=['red'])
        st.plotly_chart(fig8, use_container_width=True)
