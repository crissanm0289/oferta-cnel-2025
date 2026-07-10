import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
import requests

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(layout="wide", page_title="SISTEMA DE GESTIÓN RDO & DASHBOARD", page_icon="⚡")

# --- CONFIGURACIÓN DE TU BASE DE DATOS (GOOGLE SHEETS) ---
ID_HOJA_CALCULO = "1Tfr-YxL5pb5B0a8GhUFsm70cQJ1UJagtWMbYMzfJQg0"

# REEMPLAZA AQUÍ: Pega la URL larga que te dio Google Apps Script al implementar (PASO 2)
URL_WEB_APP_GOOGLE = "TU_URL_DE_APPS_SCRIPT_AQUI"

# --- GESTIÓN DE MEMORIA E INICIALIZACIÓN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "MÓDULO 2: DASHBOARD (Lista de 8 Puntos)"

def cambiar_pagina(nombre_pagina):
    st.session_state.pagina_actual = nombre_pagina

def reset_app():
    if 'logged_in' in st.session_state:
        st.session_state['logged_in'] = False
    st.session_state.pagina_actual = "MÓDULO 2: DASHBOARD (Lista de 8 Puntos)"
    st.rerun()

# --- ESTILOS VISUALES GENERALES ---
st.markdown("""
<style>
    .main-header {font-size: 24px; font-weight: bold; color: #1E3A8A; margin-bottom: 10px;}
    .stTextInput label, .stDateInput label, .stSelectbox label, .stTextArea label, .stNumberInput label, .stSlider label {
        font-weight: bold !important; color: #b91c1c !important; font-size: 15px !important;
    }
    .ficha-tecnica {
        width: 100%; border-collapse: collapse; margin-bottom: 20px; font-family: Arial, sans-serif; font-size: 12px; border: 1px solid #ddd;
    }
    .ficha-tecnica th {background-color: #1E3A8A; color: white; padding: 6px; text-align: center; border: 1px solid #ddd;}
    .ficha-tecnica td {padding: 6px; border: 1px solid #ddd; background-color: #f9f9f9; color: #333;}
    
    div.stButton > button:first-child {
        border-radius: 5px;
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

# DETERMINAR LA PESTAÑA DE LECTURA SEGÚN LA ZONA
nombre_pestaña = "ZONA_1" if contrato_seleccionado == "ZONA 1 - SECTOR CAMARONERO" else "ZONA_2"

# CONTROL DE ACCESOS Y MENÚ
if not st.session_state['logged_in']:
    st.sidebar.markdown("### 🔒 Acceso Administrativo")
    correo = st.sidebar.text_input("Correo Electrónico")
    clave = st.sidebar.text_input("Contraseña", type="password")
    
    if st.sidebar.button("Ingresar"):
        if correo == "cristhian@fiscalred.com" and clave == "admin123":
            st.session_state['logged_in'] = True
            st.session_state.pagina_actual = "MÓDULO 1: RDO (Lista de 19 Puntos)"
            st.rerun()
        else:
            st.sidebar.error("Credenciales incorrectas")
            
    st.sidebar.info("👀 Modo Visualizador Activo. Inicie sesión para ingresar o editar datos del RDO.")
    modulo = "MÓDULO 2: DASHBOARD (Lista de 8 Puntos)"
else:
    st.sidebar.success("🔓 Sesión iniciada")
    modulo = st.sidebar.radio(
        "Navegación:", 
        ["MÓDULO 1: RDO (Lista de 19 Puntos)", "MÓDULO 2: DASHBOARD (Lista de 8 Puntos)"],
        index=0 if st.session_state.pagina_actual == "MÓDULO 1: RDO (Lista de 19 Puntos)" else 1,
        key="navegacion_radio",
        on_change=lambda: cambiar_pagina(st.session_state.navegacion_radio)
    )
    st.sidebar.markdown("---")
    if st.sidebar.button("🗑️ RESETEAR SESIÓN", help="Cierra sesión y limpia los estados de la app"):
        reset_app()
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state['logged_in'] = False
        st.session_state.pagina_actual = "MÓDULO 2: DASHBOARD (Lista de 8 Puntos)"
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.info(f"**Oferente:** Consorcio FiscalRed\n**Usuario:** Ing. Cristhian San Martin")

# --- LECTURA EN TIEMPO REAL DESDE GOOGLE SHEETS ---
url_csv = f"https://docs.google.com/spreadsheets/d/{ID_HOJA_CALCULO}/gviz/tq?tqx=out:csv&sheet={nombre_pestaña}"
try:
    df_actual = pd.read_csv(url_csv)
except Exception:
    df_actual = pd.DataFrame({
        'Fecha': ['2025-01-01'], 'Día N': ['Inicio'], 'Físico Diario (%)': [0.0],
        'Inversión Diaria ($)': [0.0], 'Físico Acum (%)': [0.0], 'Financiero Acum ($)': [0.0],
        'Saldo ($)': [0.0], 'Detalle': ['Inicio de Contrato'], 'Fotos': [0]
    })

# --- FICHA TÉCNICA ---
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
            "Link": "https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/PC/informacionProcesoContratacion2.cpe?idSoliCompra=Mlped7h-x8tM2Mi5JzAbNVHBoqrlPkyFh2Yoxj85zQc",
            "Drive": "https://drive.google.com/drive/folders/1fOF924Rnr2mWbuCgpwu2qFdvYNwjko5M?usp=sharing"
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
            "Link": "https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/PC/informacionProcesoContratacion2.cpe?idSoliCompra=VJCoFonyH1vOnVROGwOunGmr6qD3pTr-znOrgilqON0,",
            "Drive": "https://drive.google.com/drive/folders/1JnLGiQNXOhhWx-lDX_hroJa0-vUwDAYr?usp=sharing"
        }

ficha = obtener_ficha_tecnica(contrato_seleccionado)

def dibujar_ficha(datos):
    html_table = f"""
    <table class="ficha-tecnica">
        <tr><th colspan="4">FICHA TÉCNICA DEL PROYECTO (CONTRATO DE OBRA)</th></tr>
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
            <td><strong>Link SERCOP:</strong></td><td><a href="{datos['Link']}" target="_blank">Ver en SERCOP</a></td>
        </tr>
        <tr>
            <td><strong>Nube Drive:</strong></td><td colspan="3"><a href="{datos['Drive']}" target="_blank">📂 Acceder a los respaldos en Google Drive</a></td>
        </tr>
    </table>
    """
    st.markdown(html_table, unsafe_allow_html=True)

# ==============================================================================
# MÓDULO 1: RDO WEB (INGRESO DIARIO)
# ==============================================================================
if modulo == "MÓDULO 1: RDO (Lista de 19 Puntos)":
    st.markdown(f'<div class="main-header">Módulo 1: Registro Diario de Obra (RDO)</div>', unsafe_allow_html=True)
    dibujar_ficha(ficha)

    if len(df_actual) > 0:
        ultimo_reg = df_actual.iloc[-1]
        try:
            prev_pct_acum = float(ultimo_reg['Físico Acum (%)'])
            prev_monto_acum = float(ultimo_reg['Financiero Acum ($)'])
        except Exception:
            prev_pct_acum = 0.0
            prev_monto_acum = 0.0
    else:
        prev_pct_acum = 0.0
        prev_monto_acum = 0.0

    modo_edicion = st.checkbox("🔓 Modificar Registro Anterior (Corrección)")
    
    defaults = {
        "fecha": date.today(), "dia_n": "", "clima_idx": 0, "incidente_idx": 0,
        "pct_diario": 0.0, "monto_diario": 0.0, "cpi": 0.0, "spi": 0.0,
        "personal": "", "actividad": "", "firma": "Ing. Cristhian San Martin"
    }
    indice_a_editar = -1

    if modo_edicion:
        st.info("⚠️ MODO EDICIÓN HISTÓRICA ACTIVO")
        df_validos = df_actual.iloc[1:] if len(df_actual) > 1 else df_actual
        opciones = df_validos['Fecha'].astype(str) + " - " + df_validos['Día N'].astype(str)
        
        if not opciones.empty:
            seleccion = st.selectbox("Seleccione Registro a corregir:", opciones)
            fecha_sel_str = seleccion.split(" - ")[0]
            dia_sel = seleccion.split(" - ")[1]
            mask = (df_actual['Fecha'].astype(str) == fecha_sel_str) & (df_actual['Día N'].astype(str) == dia_sel)
            if mask.any():
                indice_a_editar = df_actual[mask].index[0]
                fila = df_actual.loc[indice_a_editar]
                try:
                    defaults["fecha"] = datetime.strptime(str(fila['Fecha']), '%Y-%m-%d').date()
                except Exception:
                    defaults["fecha"] = date.today()
                defaults["dia_n"] = str(fila['Día N'])
                defaults["pct_diario"] = float(fila['Físico Diario (%)'])
                defaults["monto_diario"] = float(fila['Inversión Diaria ($)'])
                defaults["actividad"] = str(fila['Detalle'])
                
                idx_prev = indice_a_editar - 1
                if idx_prev >= 0:
                    prev_pct_acum = float(df_actual.iloc[idx_prev]['Físico Acum (%)'])
                    prev_monto_acum = float(df_actual.iloc[idx_prev]['Financiero Acum ($)'])
                else:
                    prev_pct_acum = 0.0
                    prev_monto_acum = 0.0
        else:
            st.warning("No hay registros suficientes para editar.")

    with st.form("rdo_form", clear_on_submit=False):
        st.markdown("### A. Datos Generales")
        c1, c2 = st.columns(2)
        in_fecha = c1.date_input("1. Fechas de Ejecución", defaults["fecha"])
        in_dia = c2.text_input("4. Día de ejecución (Obligatorio)", defaults["dia_n"], placeholder="Ej: Día 1")
        
        c3, c4 = st.columns(2)
        c3.text_input("2. Datos Económicos del Contrato", "$ 67,490.10 (Fiscalización)", disabled=True)
        c4.text_input("3. Dato Económico total de los Proyectos", ficha['Monto_Str'], disabled=True)

        st.markdown("### B. Condiciones de Campo")
        col_clima, col_inc = st.columns(2)
        in_clima = col_clima.selectbox("5. Condiciones climáticas (Obligatorio)", ["", "Soleado", "Nublado", "Lluvia", "Tormenta"], index=defaults["clima_idx"])
        in_inc = col_inc.selectbox("19. Registro de Incidentes o accidentes", ["Sin Novedades", "Incidente Leve", "Accidente"], index=defaults["incidente_idx"])

        st.markdown("### C. Control de Avance")
        st.info(f"**6. Progreso General (Ingreso de Avance del DÍA):**")
        m1, m2, m3 = st.columns(3)
        in_pct_diario = m1.number_input("6.i. % de Avance DEL DÍA", min_value=0.0, max_value=100.0, value=defaults["pct_diario"], step=0.01)
        in_monto_diario = m2.number_input("6.i. $ de Avance DEL DÍA", min_value=0.0, value=defaults["monto_diario"], step=100.0)
        
        nuevo_acum_monto = prev_monto_acum + in_monto_diario
        nuevo_saldo = ficha['Monto_Num'] - nuevo_acum_monto
        m3.metric("6.i. Avance Avaluado Acumulado (Automático)", f"$ {nuevo_acum_monto:,.2f}", f"Saldo: $ {nuevo_saldo:,.2f}")

        st.markdown("**6.ii. Avance prorrateado por Hito**")
        col_h1, col_h2 = st.columns(2)
        col_h1.number_input("6.ii. Hito 1 (Civil) %", min_value=0.0, max_value=100.0, value=0.0)
        col_h2.number_input("6.ii. Hito 2 (Eléctrico) %", min_value=0.0, max_value=100.0, value=0.0)
        
        st.markdown("**7. Indicadores de Desempeño y estimaciones**")
        col_c, col_s = st.columns(2)
        in_cpi = col_c.number_input("7. CPI (Costo)", value=defaults["cpi"], step=0.01)
        in_spi = col_s.number_input("7. SPI (Cronograma)", value=defaults["spi"], step=0.01)
        
        cc1, cc2 = st.columns(2)
        cc1.selectbox("14. Control mediante Tabla de cantidades y Reporte", ["", "SI - Verificado", "NO"], index=0)
        cc2.text_input("15. Porcentaje total de los proyectos", "", placeholder="Ponderado...")

        st.markdown("**8. Curva de Avance – Valor Ganado**")
        fig_rdo = go.Figure()
        fig_rdo.add_trace(go.Bar(x=["Anterior", "Nuevo"], y=[prev_pct_acum, prev_pct_acum + in_pct_diario], name='Crecimiento'))
        fig_rdo.update_layout(height=150, margin=dict(t=10, b=10))
        st.plotly_chart(fig_rdo, use_container_width=True)

        st.markdown("### D. Administrativo y Detalle")
        l1, l2, l3 = st.columns(3)
        l1.text_input("16. Registro de Contratos Complementarios", "Ninguno")
        l2.text_input("17. Registro de Ordenes de trabajo", "")
        l3.text_input("18. Registro de Incremento de cantidades", "0.00%")

        in_personal = st.text_area("13. Personal y Equipos (Obligatorio)", defaults["personal"], placeholder="Detalle cuadrilla...")
        in_activ = st.text_area("10. Actividades ejecutadas in el día (Obligatorio)", defaults["actividad"], placeholder="Descripción...")
        st.text_area("9. Observaciones de fiscalización", "")

        st.markdown("**11. Registro fotográfico & 12. Firmas**")
        c_foto, c_firma = st.columns(2)
        in_fotos = c_foto.file_uploader("11. Registro fotográfico (Obligatorio)", accept_multiple_files=True)
        in_firma = c_firma.text_input("12. Firmas de responsabilidad (Obligatorio)", defaults["firma"])

        btn_label = "ENVIAR MODIFICACIÓN HISTÓRICA" if modo_edicion else "GUARDAR RDO DIARIO"
        submitted = st.form_submit_button(btn_label)
    
    if submitted:
        errores = []
        if not in_dia: errores.append("• Falta: 4. Día de ejecución")
        if in_clima == "": errores.append("• Falta: 5. Condiciones climáticas")
        if not in_personal: errores.append("• Falta: 13. Personal y Equipos")
        if not in_activ: errores.append("• Falta: 10. Actividades Ejecutadas")
        if not in_firma: errores.append("• Falta: 12. Firmas de responsabilidad")
        if not modo_edicion and not in_fotos: errores.append("• Falta: 11. Registro fotográfico")
        
        if not modo_edicion:
            fechas_existentes = df_actual['Fecha'].astype(str).tolist()
            if len(fechas_existentes) > 1 and str(in_fecha) in fechas_existentes[1:]:
                 errores.append(f"⛔ LA FECHA {in_fecha.strftime('%d/%m/%Y')} YA EXISTE.")

        if errores:
            st.error("⚠️ NO SE PUDO GUARDAR. REVISE:")
            for e in errores: st.write(e)
        else:
            final_pct_acum = prev_pct_acum + in_pct_diario
            final_monto_acum = prev_monto_acum + in_monto_diario
            final_saldo = ficha['Monto_Num'] - final_monto_acum
            if final_pct_acum > 100: final_pct_acum = 100.0
            if final_monto_acum > ficha['Monto_Num']: final_monto_acum = ficha['Monto_Num']

            datos_nuevos = {
                "zona": nombre_pestaña,
                "fecha": str(in_fecha),
                "dia_n": in_dia,
                "pct_diario": float(in_pct_diario),
                "monto_diario": float(in_monto_diario),
                "pct_acum": float(final_pct_acum),
                "monto_acum": float(final_monto_acum),
                "saldo": float(final_saldo),
                "detalle": in_activ,
                "fotos": len(in_fotos) if in_fotos else 0
            }

            with st.spinner("Guardando en la nube de forma segura..."):
                try:
                    if URL_WEB_APP_GOOGLE == "TU_URL_DE_APPS_SCRIPT_AQUI":
                        st.error("❌ Por favor, inserta tu URL de Google Apps Script en la línea 16.")
                    else:
                        respuesta = requests.post(URL_WEB_APP_GOOGLE, json=datos_nuevos)
                        if respuesta.status_code == 200 and respuesta.json().get("status") == "success":
                            st.success("✅ REGISTRO GUARDADO DIRECTAMENTE EN LA NUBE.")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Error al procesar la inserción en la base de datos.")
                except Exception as e:
                    st.error(f"❌ Error de conexión: {str(e)}")

# ==============================================================================
# MÓDULO 2: DASHBOARD (8 PUNTOS)
# ==============================================================================
elif modulo == "MÓDULO 2: DASHBOARD (Lista de 8 Puntos)":
    st.markdown(f'<div class="main-header">Módulo 2: Dashboard de Desempeño</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    .print-instruction {
        background-color: #f0f2f6; border-left: 5px solid #1E3A8A;
        padding: 10px; margin-bottom: 20px; border-radius: 5px; color: #333;
    }
    @media print {
        section[data-testid="stSidebar"], header, footer, .stAppDeployButton, #MainMenu, .stButton, .print-instruction {
            display: none !important;
        }
        .block-container {
            padding: 0 !important; max-width: 100% !important;
        }
        * {
            -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important;
        }
        div[data-testid="stMarkdownContainer"], div[data-testid="stDataFrame"], .plotly-graph-div {
            page-break-inside: avoid !important;
        }
    }
    </style>
    
    <div class="print-instruction">
        ℹ️ <strong>Para exportar a PDF:</strong><br>
        Presione las teclas <kbd>Ctrl</kbd> + <kbd>P</kbd> (o Cmd+P).<br>
        En la ventana de impresión, elija "Guardar como PDF".
    </div>
    """, unsafe_allow_html=True)

    dibujar_ficha(ficha)
    st.markdown(f"#### 1. Fecha de emisión: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    if len(df_actual) > 1:
        df_final = df_actual.iloc[1:].reset_index(drop=True)
    else:
        df_final = pd.DataFrame(columns=['Fecha', 'Día N', 'Físico Diario (%)', 'Inversión Diaria ($)', 'Físico Acum (%)', 'Financiero Acum ($)', 'Saldo ($)'])
        df_final.loc[0] = [date.today().strftime('%Y-%m-%d'), 'Inicio', 0, 0, 0, 0, ficha['Monto_Num']]

    st.markdown("### 2. % de Avance Acumulado (Tabla Detallada)")
    cols_mostrar = ['Fecha', 'Día N', 'Físico Diario (%)', 'Inversión Diaria ($)', 'Físico Acum (%)', 'Financiero Acum ($)', 'Saldo ($)']
    
    # Conversiones rápidas para formatear sin errores visuales en tablas
    for col in ['Físico Diario (%)', 'Inversión Diaria ($)', 'Físico Acum (%)', 'Financiero Acum ($)', 'Saldo ($)']:
        df_final[col] = pd.to_numeric(df_final[col], errors='coerce').fillna(0.0)

    st.dataframe(
        df_final[cols_mostrar].style.format({
            'Físico Diario (%)': "{:.2f}%", 'Inversión Diaria ($)': "$ {:,.2f}",
            'Físico Acum (%)': "{:.2f}%", 'Financiero Acum ($)': "$ {:,.2f}", 'Saldo ($)': "$ {:,.2f}"
        }),
        use_container_width=True, height=300
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
        fig7 = px.bar(df_final, x='Fecha', y='Inversión Diaria ($)', title="Planillado Diario")
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
