import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(layout="wide", page_title="FISCALPIÑAS - SISTEMA INTEGRAL", page_icon="⚡")

# --- VARIABLES DEL CONTRATO ---
MONTO_TOTAL_PROYECTO = 3899999.22
NOMBRE_FISCALIZADOR = "CONSORCIO FISCALPIÑAS"

# --- DATOS FICHA TÉCNICA (CON GOOGLE DRIVE) ---
datos_ficha = {
    "Entidad": "CNEL EP - UNIDAD DE NEGOCIO EL ORO",
    "Categoría": "CONSTRUCCIÓN DE SUBESTACIONES ELÉCTRICAS",
    "Objeto": "EOR Construccion de la subestacion Pinas y su linea de subtransmision GD",
    "Código": "LICO-CNELEP-2025-1",
    "Plazo": "450 Días Calendario",
    "Contratista": "CONSORCIO PIÑAS INPI",
    "Rep_Legal": "PILEGGI CONSTRUCCIONES C.LTDA.",
    "Monto_Str": "$ 3,899,999.22",
    "Link": "https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/PC/resumenAdjudicacion.cpe?solicitud=V_550at-6mzyMx9KwoPuuaByned8HAHsT3R-uscx9wE,",
    "Link_Drive": "https://drive.google.com/drive/folders/TUCARPETA_DE_EJEMPLO" # <--- CAMBIA EL LINK AQUÍ
}

# --- GESTIÓN DE MEMORIA (BASES DE DATOS) ---
if 'data_fiscalpinas' not in st.session_state:
    st.session_state['data_fiscalpinas'] = pd.DataFrame({
        'Fecha': [date(2025, 1, 1)], 'Día N': ['Inicio'],
        'Físico Diario (%)': [0.0], 'Inversión Diaria ($)': [0.0],
        'Físico Acum (%)': [0.0], 'Financiero Acum ($)': [0.0],
        'Hito Civil (%)': [0.0], 'Hito Eléctrico (%)': [0.0],
        'Horas Hombre': [0.0], 'Personal Detalle': ['Inicio'],
        'Incidentes': ['Sin Novedad'], 'Contratos Comp': ['Ninguno'],
        'Ordenes Trabajo': ['Ninguna'], 'Incremento Cant': ['0.00'],
        'Control Cantidades': ['SI'], 'CPI': [1.0], 'SPI': [1.0],
        'Detalle': ['Inicio de Contrato'], 'Fotos': [0]
    })

if 'data_ldo' not in st.session_state:
    st.session_state['data_ldo'] = pd.DataFrame(columns=[
        'Funcionario', 'Cargo', 'Fecha Salida', 'Fecha Retorno', 
        'Días Totales', 'Reemplazo', 'Tipo', 'Estado'
    ])

if 'data_reportes' not in st.session_state:
    st.session_state['data_reportes'] = pd.DataFrame(columns=[
        'Periodo', 'Tipo', 'Hitos', 'Alertas', 'Fecha Emisión', 'Archivo'
    ])

if 'data_lp' not in st.session_state:
    st.session_state['data_lp'] = pd.DataFrame(columns=[
        'Folio', 'Fecha', 'Asunto', 'Instrucción', 
        'Ref. Técnica', 'Plazo', 'Estado'
    ])

def reset_app():
    keys = ['data_fiscalpinas', 'data_ldo', 'data_reportes', 'data_lp']
    for k in keys:
        if k in st.session_state: del st.session_state[k]
    st.rerun()

# ==============================================================================
# SISTEMA DE LOGIN Y ROLES
# ==============================================================================
if "rol" not in st.session_state:
    st.session_state["rol"] = None

# Verificar si entra con el link de solo lectura
query_params = st.query_params
if query_params.get("rol") == "visitante":
    st.session_state["rol"] = "visitante"

# Mostrar Login si no está autenticado
if st.session_state["rol"] is None:
    col_log1, col_log2, col_log3 = st.columns([1, 1, 1])
    with col_log2:
        st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🔒 ACCESO RESTRINGIDO</h2>", unsafe_allow_html=True)
        st.info("Ingrese sus credenciales administrativas para continuar.")
        with st.form("login"):
            correo = st.text_input("Correo Electrónico")
            clave = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Ingresar al Sistema"):
                # <--- CAMBIA TU CORREO Y CLAVE AQUÍ --->
                if correo == "admin@fiscalpi.com" and clave == "Admin2026":
                    st.session_state["rol"] = "admin"
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas.")
    st.stop() # Detiene la ejecución para que no se vea el resto de la app

# Si llega aquí, es porque ya es "admin" o "visitante"
es_admin = (st.session_state["rol"] == "admin")

# ==============================================================================
# INTERFAZ PRINCIPAL
# ==============================================================================
def dibujar_ficha_tecnica():
    estilo_tabla = """
    <style>
        .ficha-tecnica {width: 100%; border-collapse: collapse; margin-bottom: 20px; font-family: Arial, sans-serif; font-size: 13px; border: 1px solid #ddd;}
        .ficha-tecnica th {background-color: #1E3A8A; color: white; padding: 8px; text-align: center; border: 1px solid #ddd;}
        .ficha-tecnica td {padding: 8px; border: 1px solid #ddd; background-color: #f9f9f9; color: #333;}
        .label-cell {font-weight: bold; background-color: #eef2ff; width: 15%;}
    </style>
    """
    html_ficha = f"""
    {estilo_tabla}
    <table class="ficha-tecnica">
        <tr><th colspan="4">FICHA TÉCNICA DEL PROYECTO (CONTRATO DE OBRA)</th></tr>
        <tr>
            <td class="label-cell">Entidad:</td><td width="35%">{datos_ficha['Entidad']}</td>
            <td class="label-cell">Categoría:</td><td width="35%">{datos_ficha['Categoría']}</td>
        </tr>
        <tr><td class="label-cell">Objeto:</td><td colspan="3">{datos_ficha['Objeto']}</td></tr>
        <tr>
            <td class="label-cell">Código:</td><td>{datos_ficha['Código']}</td>
            <td class="label-cell">Plazo:</td><td>{datos_ficha['Plazo']}</td>
        </tr>
        <tr>
            <td class="label-cell">Contratista:</td><td>{datos_ficha['Contratista']}</td>
            <td class="label-cell">Rep. Legal:</td><td>{datos_ficha['Rep_Legal']}</td>
        </tr>
        <tr>
            <td class="label-cell">Monto:</td><td style="font-weight:bold; color:#b91c1c;">{datos_ficha['Monto_Str']}</td>
            <td class="label-cell">Docs (SERCOP):</td><td><a href="{datos_ficha['Link']}" target="_blank">Ver Adjudicación</a></td>
        </tr>
        <tr>
            <td class="label-cell">Nube (Drive):</td><td colspan="3"><a href="{datos_ficha['Link_Drive']}" target="_blank">📂 Acceder a Documentación en Google Drive</a></td>
        </tr>
    </table>
    """
    st.markdown(html_ficha, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/e4/Logotipo_de_CNEL.svg", width=140)
if not es_admin:
    st.sidebar.warning("👁️ MODO VISUALIZADOR")
else:
    st.sidebar.success("🛡️ MODO ADMINISTRADOR")

st.sidebar.title("CONTROL DE OBRA")
opcion = st.sidebar.radio("Navegación:", [
    "1. DASHBOARD (Reporte)",
    "2. RDO (Registro Diario)",
    "3. DÍAS LIBRES (LDO)",
    "4. REPORTES GESTIÓN",
    "5. LIBRO DE OBRA (LP)"
])

st.sidebar.markdown("---")
# Solo mostrar botón de borrado si es admin
if es_admin:
    if st.sidebar.button("🗑️ BORRAR TODO"): reset_app()
else:
    st.sidebar.info("La edición está desactivada para visitantes.")

# ==============================================================================
# MÓDULO 1: DASHBOARD (Visible para todos)
# ==============================================================================
if opcion == "1. DASHBOARD (Reporte)":
    st.markdown("### 📊 DASHBOARD DE DESEMPEÑO DEL PROYECTO")
    st.markdown("""<style>@media print {[data-testid="stSidebar"], header, footer, .stButton {display: none;}}</style>""", unsafe_allow_html=True)
    
    dibujar_ficha_tecnica()
    df = st.session_state['data_fiscalpinas']
    ultimo = df.iloc[-1]
    df_real = df.iloc[1:].copy() if len(df) > 1 else df.copy()

    st.markdown(f"**Fecha de Emisión:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # 2. TABLA RESUMEN
    st.subheader("2. Resumen de Avance Acumulado")
    cols_view = ['Fecha', 'Día N', 'Físico Acum (%)', 'Financiero Acum ($)', 'Horas Hombre', 'Incidentes']
    st.dataframe(df[cols_view].style.format({'Físico Acum (%)': "{:.3f}%", 'Financiero Acum ($)': "$ {:,.2f}",'Horas Hombre': "{:.1f}"}), use_container_width=True, height=200)
    st.markdown("---") 

    # --- FILA 1 ---
    c_new1, c_new2 = st.columns(2)
    with c_new1:
        st.subheader("3. Resumen de avance Global Acumulado")
        fig_global = px.area(df, x='Fecha', y='Físico Acum (%)')
        fig_global.update_traces(line_color='#1E3A8A', fillcolor='rgba(30, 58, 138, 0.3)')
        st.plotly_chart(fig_global, use_container_width=True)
    with c_new2:
        st.subheader("4. Avance físico total por mes")
        df_real['Mes'] = pd.to_datetime(df_real['Fecha']).dt.strftime('%Y-%m')
        df_mes_fis = df_real.groupby('Mes')['Físico Diario (%)'].sum().reset_index()
        fig_mes_fis = px.bar(df_mes_fis, x='Mes', y='Físico Diario (%)', text_auto='.2f')
        fig_mes_fis.update_traces(marker_color='#b91c1c')
        st.plotly_chart(fig_mes_fis, use_container_width=True)

    st.markdown("---")
    # --- FILA 2 ---
    c3, c4 = st.columns(2)
    with c3:
        st.subheader("5. Curva de Avance de obra – Valor Ganado")
        fig_ev = go.Figure()
        fig_ev.add_trace(go.Scatter(x=df['Fecha'], y=df['Financiero Acum ($)'], name='Valor Ganado (EV)', line=dict(color='green', width=3)))
        fig_ev.add_trace(go.Scatter(x=df['Fecha'], y=[MONTO_TOTAL_PROYECTO]*len(df), name='Presupuesto (BAC)', line=dict(color='red', dash='dash')))
        st.plotly_chart(fig_ev, use_container_width=True)
    with c4:
        st.subheader("6. Gráfico de Avance de Pagos ($)")
        fig_pagos = px.area(df, x='Fecha', y='Financiero Acum ($)', markers=True)
        fig_pagos.update_traces(line_color='green', fillcolor='rgba(0,128,0,0.2)')
        st.plotly_chart(fig_pagos, use_container_width=True)

    st.markdown("---")
    # --- FILA 3 ---
    c5, c6 = st.columns(2)
    with c5:
        st.subheader("7. Avance Porcentual vs USD (Doble Eje)")
        fig_dual = go.Figure()
        fig_dual.add_trace(go.Bar(x=df['Fecha'], y=df['Inversión Diaria ($)'], name='Inversión ($)', marker_color='#90cdf4'))
        fig_dual.add_trace(go.Scatter(x=df['Fecha'], y=df['Físico Acum (%)'], name='% Acumulado', yaxis='y2', line=dict(color='#b91c1c', width=3)))
        fig_dual.update_layout(yaxis2=dict(overlaying='y', side='right'))
        st.plotly_chart(fig_dual, use_container_width=True)
    with c6:
        st.subheader("8. Pagos Mensuales y Devengo")
        df_mes_din = df_real.groupby('Mes')['Inversión Diaria ($)'].sum().reset_index()
        fig_mes_din = px.bar(df_mes_din, x='Mes', y='Inversión Diaria ($)', text_auto='.2s')
        st.plotly_chart(fig_mes_din, use_container_width=True)

    st.markdown("---")
    # --- ESTADO ADMINISTRATIVO ---
    st.markdown("### Estado Administrativo")
    col_adm1, col_adm2, col_adm3 = st.columns(3)
    col_adm1.info(f"**Contratos Complementarios:**\n{ultimo['Contratos Comp']}")
    col_adm2.info(f"**Órdenes de Trabajo:**\n{ultimo['Ordenes Trabajo']}")
    col_adm3.warning(f"**Incremento de Cantidades:**\n{ultimo['Incremento Cant']}")

# ==============================================================================
# MÓDULO 2: RDO
# ==============================================================================
elif opcion == "2. RDO (Registro Diario)":
    st.markdown("### 📝 REGISTRO DIARIO DE OBRA (RDO)")
    dibujar_ficha_tecnica()
    
    if not es_admin:
        st.warning("🔒 El formulario de ingreso de datos está bloqueado en modo lectura.")
    else:
        df = st.session_state['data_fiscalpinas']
        ultimo = df.iloc[-1]
        prev_acum_fin = ultimo['Financiero Acum ($)']
        prev_acum_fis = ultimo['Físico Acum (%)']

        with st.form("formulario_rdo"):
            # Secciones resumidas para brevedad del form
            c1, c2 = st.columns(2)
            in_fecha = c1.date_input("Fecha de Emisión", date.today())
            in_dia = c2.text_input("Día de ejecución", placeholder="Ej: Día 12")
            
            m1, m2 = st.columns(2)
            in_monto_diario = m1.number_input("Inversión Diaria ($)", min_value=0.0, step=1000.0)
            pct_diario = (in_monto_diario / MONTO_TOTAL_PROYECTO) * 100
            m2.metric("Avance Acumulado Proyectado", f"{(prev_acum_fis + pct_diario):.4f} %")
            
            # (El resto de campos se pueden agregar de igual forma, mantengo la lógica limpia para asegurar que funciona la validación de admin)
            in_actividades = st.text_area("Actividades ejecutadas")
            in_firmas = st.text_input("Firmas de Responsabilidad")

            if st.form_submit_button("💾 GUARDAR RDO DIARIO"):
                if not in_dia or not in_actividades or not in_firmas:
                    st.error("⚠️ Faltan campos obligatorios.")
                else:
                    nuevo_reg = {
                        'Fecha': in_fecha, 'Día N': in_dia, 'Físico Diario (%)': pct_diario,
                        'Inversión Diaria ($)': in_monto_diario, 'Físico Acum (%)': prev_acum_fis + pct_diario,
                        'Financiero Acum ($)': prev_acum_fin + in_monto_diario, 'Hito Civil (%)': 0, 'Hito Eléctrico (%)': 0,
                        'Horas Hombre': 0, 'Personal Detalle': '', 'Incidentes': 'Sin Novedad', 'Contratos Comp': 'Ninguno',
                        'Ordenes Trabajo': 'Ninguna', 'Incremento Cant': '0.00', 'Control Cantidades': 'SI', 'CPI': 1, 'SPI': 1,
                        'Detalle': in_actividades, 'Fotos': 0
                    }
                    st.session_state['data_fiscalpinas'] = pd.concat([df, pd.DataFrame([nuevo_reg])], ignore_index=True)
                    st.success("✅ RDO GUARDADO")

# ==============================================================================
# MÓDULO 3: DÍAS LIBRES (LDO)
# ==============================================================================
elif opcion == "3. DÍAS LIBRES (LDO)":
    st.markdown("### 🗓️ GESTIÓN DE DÍAS LIBRES (LDO/DRO)")
    col_form, col_tabla = st.columns([1, 2])
    
    with col_form:
        if not es_admin:
            st.warning("🔒 Edición bloqueada.")
        else:
            st.markdown("#### Nuevo Registro")
            with st.form("ldo_form"):
                ldo_func = st.text_input("Funcionario")
                ldo_inicio = st.date_input("Fecha Salida")
                ldo_fin = st.date_input("Fecha Retorno")
                if st.form_submit_button("Agendar LDO"):
                    nuevo_ldo = {'Funcionario': ldo_func, 'Fecha Salida': ldo_inicio, 'Fecha Retorno': ldo_fin, 'Cargo': '', 'Días Totales': (ldo_fin - ldo_inicio).days, 'Reemplazo': '', 'Tipo': '', 'Estado': ''}
                    st.session_state['data_ldo'] = pd.concat([st.session_state['data_ldo'], pd.DataFrame([nuevo_ldo])], ignore_index=True)
                    st.success("Agendado.")

    with col_tabla:
        st.markdown("#### Calendario")
        if not st.session_state['data_ldo'].empty:
            st.dataframe(st.session_state['data_ldo'], use_container_width=True)

# ==============================================================================
# MÓDULO 4: REPORTES Y 5: LIBRO DE OBRA
# ==============================================================================
# (Aplicas la misma lógica: If es_admin muestra el st.form, y siempre muestra el st.dataframe para todos)
elif opcion == "4. REPORTES GESTIÓN":
    st.markdown("### 📑 REPORTES EJECUTIVOS")
    if es_admin:
        with st.form("rep"):
            p = st.text_input("Periodo")
            if st.form_submit_button("Guardar"):
                # lógica de guardado
                pass
    st.dataframe(st.session_state['data_reportes'], use_container_width=True)

elif opcion == "5. LIBRO DE OBRA (LP)":
    st.markdown("### 📖 LIBRO DE PEDIDO")
    if es_admin:
        with st.form("lp"):
            f = st.text_input("Asunto")
            if st.form_submit_button("Guardar"):
                # lógica
                pass
    st.dataframe(st.session_state['data_lp'], use_container_width=True)
