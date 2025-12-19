import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(layout="wide", page_title="SISTEMA DE GESTIÓN RDO & DASHBOARD", page_icon="⚡")

# --- GESTIÓN DE MEMORIA (SESSION STATE) ---
if 'data_zona1' not in st.session_state:
    # Inicializamos con un registro "Cero" para que los cálculos de diferencias funcionen
    st.session_state['data_zona1'] = pd.DataFrame({
        'Fecha': [date(2025, 1, 1)],
        'Día N': ['Inicio'],
        'Físico Acum (%)': [0.0],
        'Financiero Acum ($)': [0.0],
        'Físico Diario (%)': [0.0], # Calculado
        'Inversión Diaria ($)': [0.0], # Calculado
        'Saldo ($)': [0.0], # Se recalcula luego
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

# Control de navegación
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "MÓDULO 1: RDO (Ingreso)"

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

    /* Estilo Ficha Técnica Compacta */
    .ficha-tecnica {
        width: 100%; border-collapse: collapse; margin-bottom: 15px;
        font-family: Arial, sans-serif; font-size: 13px; border: 1px solid #ddd;
    }
    .ficha-tecnica th {background-color: #1E3A8A; color: white; padding: 5px; text-align: left; border: 1px solid #ddd;}
    .ficha-tecnica td {padding: 5px; border: 1px solid #ddd; background-color: #f9f9f9; color: #333;}
    
    /* Alerta de Error Personalizada */
    .error-box {
        padding: 10px; background-color: #f8d7da; color: #721c24; 
        border: 1px solid #f5c6cb; border-radius: 5px; margin-bottom: 10px; font-weight: bold;
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

modulo = st.sidebar.radio(
    "Navegación:", 
    ["MÓDULO 1: RDO (Ingreso)", "MÓDULO 2: DASHBOARD (Reporte)"],
    index=0 if st.session_state.pagina_actual == "MÓDULO 1: RDO (Ingreso)" else 1,
    key="navegacion_radio",
    on_change=lambda: cambiar_pagina(st.session_state.navegacion_radio)
)

st.sidebar.info(f"**Oferente:** Consorcio FiscalRed\n**Usuario:** Ing. Cristhian San Martin")

# --- FICHA TÉCNICA (DATOS REALES) ---
def obtener_ficha_tecnica(zona):
    if zona == "ZONA 1 - SECTOR CAMARONERO":
        return {
            "Entidad": "CNEL EP - UNIDAD DE NEGOCIO EL ORO",
            "Objeto": "EOR Construccion de redes electricas... ZONA 1 CAF GD",
            "Código": "COTO-CNELEP-2025-43",
            "Contratista": "CONSORCIO CAF ARENILLAS",
            "Monto_Str": "$ 399.743,03",
            "Monto_Num": 399743.03,
            "Link": "https://www.compraspublicas.gob.ec"
        }
    else:
        return {
            "Entidad": "CNEL EP - UNIDAD DE NEGOCIO EL ORO",
            "Objeto": "EOR Construccion de redes electricas... ZONA 2 CAF GD",
            "Código": "COTO-CNELEP-2025-44",
            "Contratista": "CONSORCIO REDES HUNTER",
            "Monto_Str": "$ 499.654,23",
            "Monto_Num": 499654.23,
            "Link": "https://www.compraspublicas.gob.ec"
        }

ficha = obtener_ficha_tecnica(contrato_seleccionado)

def dibujar_ficha(datos):
    html_table = f"""
    <table class="ficha-tecnica">
        <tr><th colspan="4" style="text-align:center;">FICHA TÉCNICA DEL PROYECTO</th></tr>
        <tr>
            <td width="15%"><strong>Objeto:</strong></td><td colspan="3">{datos['Objeto']}</td>
        </tr>
        <tr>
            <td><strong>Contratista:</strong></td><td>{datos['Contratista']}</td>
            <td><strong>Monto USD:</strong></td><td>{datos['Monto_Str']}</td>
        </tr>
    </table>
    """
    st.markdown(html_table, unsafe_allow_html=True)

# ==============================================================================
# MÓDULO 1: RDO WEB (INGRESO Y EDICIÓN)
# ==============================================================================
if modulo == "MÓDULO 1: RDO (Ingreso)":
    st.markdown(f'<div class="main-header">Módulo 1: Registro Diario de Obra (RDO)</div>', unsafe_allow_html=True)
    dibujar_ficha(ficha)

    # --- LÓGICA DE EDICIÓN VS NUEVO ---
    key_data = 'data_zona1' if contrato_seleccionado == "ZONA 1 - SECTOR CAMARONERO" else 'data_zona2'
    df_actual = st.session_state[key_data]
    
    # Selector de Modo
    modo_edicion = st.checkbox("🔓 Modificar Registro Anterior (Solo para correcciones)")
    
    defaults = {
        "fecha": date.today(),
        "dia_n": "",
        "clima_idx": 0,
        "incidente_idx": 0,
        "pct": 0.0,
        "monto": 0.0,
        "cpi": 0.0,
        "spi": 0.0,
        "personal": "",
        "actividad": "",
        "obs": "",
        "firma": ""
    }
    
    indice_a_editar = -1 # -1 significa nuevo registro

    if modo_edicion:
        st.warning("⚠️ MODO EDICIÓN ACTIVO: Está modificando datos históricos.")
        # Selector de registro a editar (excluyendo el inicial 0)
        opciones_fecha = df_actual.iloc[1:]['Fecha'].astype(str) + " - " + df_actual.iloc[1:]['Día N']
        if not opciones_fecha.empty:
            seleccion = st.selectbox("Seleccione el registro a corregir:", opciones_fecha)
            # Buscar datos originales
            indice_a_editar = df_actual[df_actual['Fecha'].astype(str) + " - " + df_actual['Día N'] == seleccion].index[0]
            fila = df_actual.loc[indice_a_editar]
            
            # Cargar datos en defaults
            defaults["fecha"] = fila['Fecha']
            defaults["dia_n"] = fila['Día N']
            defaults["pct"] = float(fila['Físico Acum (%)'])
            defaults["monto"] = float(fila['Financiero Acum ($)'])
            defaults["actividad"] = fila['Detalle']
            # Nota: Algunos campos como texto largo no se guardaron en el DF simple de demo, 
            # pero para la demo asumimos recarga o ingreso nuevo en esos campos.
            defaults["personal"] = "Personal registrado..." 
            defaults["firma"] = "Ing. Cristhian San Martin"
        else:
            st.info("No hay registros previos para editar.")

    with st.form("rdo_form", clear_on_submit=False):
        st.markdown("### A. Datos Generales")
        c1, c2 = st.columns(2)
        in_fecha = c1.date_input("1. Fechas de Ejecución", defaults["fecha"])
        in_dia = c2.text_input("4. Día de ejecución (Obligatorio)", defaults["dia_n"], placeholder="Ej: Día 15")
        
        c3, c4 = st.columns(2)
        c3.text_input("2. Datos Económicos Contrato", "$ Fiscalización (Ref)", disabled=True)
        c4.text_input("3. Monto Total Obra", ficha['Monto_Str'], disabled=True)

        st.markdown("### B. Condiciones de Campo")
        col_clima, col_inc = st.columns(2)
        in_clima = col_clima.selectbox("5. Condiciones climáticas (Obligatorio)", ["", "Soleado", "Nublado", "Lluvia", "Tormenta"], index=defaults["clima_idx"])
        in_inc = col_inc.selectbox("19. Registro de Incidentes", ["Sin Novedades", "Incidente Leve", "Accidente"], index=defaults["incidente_idx"])

        st.markdown("### C. Control de Avance")
        st.info("**6. Progreso General (Acumulado a la fecha):**")
        
        m1, m2, m3 = st.columns(3)
        in_pct = m1.number_input("6.i. % Físico ACUMULADO", min_value=0.0, max_value=100.0, value=defaults["pct"], step=0.01)
        in_monto = m2.number_input("6.i. $ Inversión ACUMULADA", min_value=0.0, value=defaults["monto"], step=100.0)
        m3.metric("Saldo por Ejecutar (Estimado)", f"$ {ficha['Monto_Num'] - in_monto:,.2f}")

        st.markdown("**7. Indicadores de Desempeño**")
        col_cpi, col_spi = st.columns(2)
        in_cpi = col_cpi.number_input("7.i. CPI (Costo)", value=defaults["cpi"], step=0.01)
        in_spi = col_spi.number_input("7.ii. SPI (Cronograma)", value=defaults["spi"], step=0.01)

        st.markdown("### D. Detalle y Firmas")
        in_personal = st.text_area("13. Personal y Equipos (Obligatorio)", defaults["personal"], placeholder="Ej: 1 Residente, 2 Linieros...")
        in_activ = st.text_area("10. Actividades Ejecutadas (Obligatorio)", defaults["actividad"], placeholder="Ej: Izado de 3 postes...")
        
        st.markdown("**11. Registro Fotográfico & 12. Firmas**")
        c_foto, c_firma = st.columns(2)
        in_fotos = c_foto.file_uploader("Cargar Fotos (Obligatorio)", accept_multiple_files=True)
        in_firma = c_firma.text_input("12. Firma Responsable (Obligatorio)", defaults["firma"])

        btn_texto = "GUARDAR CAMBIOS" if modo_edicion else "GUARDAR RDO DIARIO"
        submitted = st.form_submit_button(btn_texto)
    
    # --- LÓGICA DE VALIDACIÓN Y GUARDADO ---
    if submitted:
        errores = []
        # 1. Validación de Campos Vacíos
        if not in_dia: errores.append("- Falta: 4. Día de ejecución")
        if in_clima == "": errores.append("- Falta: 5. Condiciones climáticas")
        if not in_personal: errores.append("- Falta: 13. Personal y Equipos")
        if not in_activ: errores.append("- Falta: 10. Actividades Ejecutadas")
        if not in_firma: errores.append("- Falta: 12. Firma Responsable")
        # Validación de fotos solo si es nuevo registro (en edición podría no volver a subir)
        if not modo_edicion and not in_fotos: errores.append("- Falta: 11. Registro Fotográfico")

        if errores:
            st.error("⚠️ NO SE PUDO GUARDAR. POR FAVOR COMPLETE:")
            for e in errores:
                st.write(e)
        else:
            # 2. Cálculos
            # Para calcular lo "Diario", necesitamos el acumulado anterior
            if modo_edicion:
                # En edición, recalculamos con base en el anterior al editado (o el mismo si es el primero)
                idx_ref = indice_a_editar - 1 if indice_a_editar > 0 else 0
                prev_pct = df_actual.iloc[idx_ref]['Físico Acum (%)']
                prev_monto = df_actual.iloc[idx_ref]['Financiero Acum ($)']
            else:
                # En nuevo, el anterior es el último
                prev_pct = df_actual.iloc[-1]['Físico Acum (%)']
                prev_monto = df_actual.iloc[-1]['Financiero Acum ($)']
            
            diario_pct = in_pct - prev_pct
            diario_monto = in_monto - prev_monto
            saldo = ficha['Monto_Num'] - in_monto

            nueva_fila = {
                'Fecha': in_fecha,
                'Día N': in_dia,
                'Físico Acum (%)': in_pct,
                'Financiero Acum ($)': in_monto,
                'Físico Diario (%)': diario_pct if diario_pct >= 0 else 0,
                'Inversión Diaria ($)': diario_monto if diario_monto >= 0 else 0,
                'Saldo ($)': saldo,
                'Detalle': in_activ,
                'Fotos': len(in_fotos) if in_fotos else 0
            }

            if modo_edicion:
                # Actualizar fila existente
                for key, val in nueva_fila.items():
                    df_actual.at[indice_a_editar, key] = val
                st.session_state[key_data] = df_actual
                st.success(f"✅ REGISTRO '{in_dia}' MODIFICADO CORRECTAMENTE.")
            else:
                # Guardar Nuevo
                df_nuevo = pd.concat([df_actual, pd.DataFrame([nueva_fila])], ignore_index=True)
                st.session_state[key_data] = df_nuevo
                st.success(f"✅ REGISTRO DEL DÍA {in_fecha.strftime('%d/%m/%Y')} GUARDADO CORRECTAMENTE.")

            # Botón de Salida al Dashboard
            st.markdown("---")
            col_msg, col_btn = st.columns([3, 1])
            col_msg.info("Base de datos actualizada.")
            if col_btn.button("👉 Ir al DASHBOARD"):
                st.session_state.navegacion_radio = "MÓDULO 2: DASHBOARD (Reporte)"
                cambiar_pagina("MÓDULO 2: DASHBOARD (Reporte)")
                st.rerun()

# ==============================================================================
# MÓDULO 2: DASHBOARD (TABLA DETALLADA)
# ==============================================================================
elif modulo == "MÓDULO 2: DASHBOARD (Reporte)":
    st.markdown(f'<div class="main-header">Módulo 2: Dashboard de Desempeño</div>', unsafe_allow_html=True)
    dibujar_ficha(ficha)
    st.markdown(f"**Fecha de corte:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    key_data = 'data_zona1' if contrato_seleccionado == "ZONA 1 - SECTOR CAMARONERO" else 'data_zona2'
    df_show = st.session_state[key_data].copy()

    # Limpiar el registro inicial "cero" para la visualización, si hay más datos
    if len(df_show) > 1:
        df_final = df_show.iloc[1:].reset_index(drop=True)
    else:
        df_final = df_show # Mostrar inicio si está vacío

    # 1. TABLA DETALLADA (REQUERIMIENTO PRINCIPAL)
    st.markdown("### 2. Tabla de Avance y Saldos (Tiempo Real)")
    
    # Formateo para que se vea bonita
    columnas_mostrar = ['Fecha', 'Día N', 'Físico Diario (%)', 'Inversión Diaria ($)', 'Físico Acum (%)', 'Financiero Acum ($)', 'Saldo ($)']
    
    # Crear un dataframe estilizado
    st.dataframe(
        df_final[columnas_mostrar].style.format({
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

    # GRÁFICOS
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("3. Curva S (Acumulada)")
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=df_final['Fecha'], y=df_final['Físico Acum (%)'], fill='tozeroy', name='Físico Real'))
        st.plotly_chart(fig3, use_container_width=True)
        
        st.subheader("7. Pagos Mensuales ($)")
        fig7 = px.bar(df_final, x='Fecha', y='Inversión Diaria ($)', title="Planillado por Registro")
        st.plotly_chart(fig7, use_container_width=True)

    with c2:
        st.subheader("6. Correlación Avance vs Inversión")
        fig6 = go.Figure()
        fig6.add_trace(go.Scatter(x=df_final['Fecha'], y=df_final['Físico Acum (%)'], name='% Avance'))
        fig6.add_trace(go.Scatter(x=df_final['Fecha'], y=df_final['Financiero Acum ($)'], name='$ Inversión', yaxis='y2', line=dict(dash='dot')))
        fig6.update_layout(yaxis2=dict(overlaying='y', side='right', title="Monto USD"))
        st.plotly_chart(fig6, use_container_width=True)
