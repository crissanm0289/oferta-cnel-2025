import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(layout="wide", page_title="SISTEMA DE GESTIÓN RDO & DASHBOARD", page_icon="⚡")

# --- GESTIÓN DE MEMORIA (SESSION STATE) ---
# Inicializamos el DataFrame con columnas para valores DIARIOS y ACUMULADOS
if 'data_zona1' not in st.session_state:
    st.session_state['data_zona1'] = pd.DataFrame({
        'Fecha': [date(2025, 1, 1)],
        'Día N': ['Inicio'],
        'Físico Acum (%)': [0.0],
        'Financiero Acum ($)': [0.0],
        'Físico Diario (%)': [0.0],       # Calculado: Hoy - Ayer
        'Inversión Diaria ($)': [0.0],    # Calculado: Hoy - Ayer
        'Saldo ($)': [0.0],               # Calculado: Total - Acumulado
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

    /* Estilo Ficha Técnica */
    .ficha-tecnica {
        width: 100%; border-collapse: collapse; margin-bottom: 20px;
        font-family: Arial, sans-serif; font-size: 13px; border: 1px solid #ddd;
    }
    .ficha-tecnica th {background-color: #1E3A8A; color: white; padding: 6px; text-align: left; border: 1px solid #ddd;}
    .ficha-tecnica td {padding: 6px; border: 1px solid #ddd; background-color: #f9f9f9; color: #333;}
    
    /* Caja de Error */
    .error-box {
        padding: 10px; background-color: #f8d7da; color: #721c24; 
        border: 1px solid #f5c6cb; border-radius: 5px; margin-bottom: 10px;
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
    ["MÓDULO 1: RDO (Lista de 19 Puntos)", "MÓDULO 2: DASHBOARD (Lista de 8 Puntos)"],
    index=0 if st.session_state.pagina_actual == "MÓDULO 1: RDO (Lista de 19 Puntos)" else 1,
    key="navegacion_radio",
    on_change=lambda: cambiar_pagina(st.session_state.navegacion_radio)
)

st.sidebar.info(f"**Oferente:** Consorcio FiscalRed\n**Usuario:** Ing. Cristhian San Martin")

# --- FICHA TÉCNICA (DATOS REALES) ---
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
# MÓDULO 1: RDO WEB (INGRESO CON VALIDACIÓN Y EDICIÓN)
# ==============================================================================
if modulo == "MÓDULO 1: RDO (Lista de 19 Puntos)":
    st.markdown(f'<div class="main-header">Módulo 1: Registro Diario de Obra (RDO)</div>', unsafe_allow_html=True)
    dibujar_ficha(ficha)
    st.warning("Formulario de Campo - Numeración conforme a TDR Pág. 28")

    # --- LÓGICA DE EDICIÓN (CANDADO) ---
    key_data = 'data_zona1' if contrato_seleccionado == "ZONA 1 - SECTOR CAMARONERO" else 'data_zona2'
    df_actual = st.session_state[key_data]

    # Checkbox para habilitar edición histórica
    modo_edicion = st.checkbox("🔓 Modificar Registro Anterior (Corrección de Historial)")

    # Valores por defecto (Vacíos para nuevo registro)
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
        "firma": ""
    }
    indice_a_editar = -1

    if modo_edicion:
        st.info("⚠️ MODO EDICIÓN: Seleccione el día que desea corregir. Los cambios sobreescribirán el registro.")
        opciones = df_actual.iloc[1:]['Fecha'].astype(str) + " - " + df_actual.iloc[1:]['Día N']
        if not opciones.empty:
            seleccion = st.selectbox("Seleccione Registro:", opciones)
            # Buscar datos
            indice_a_editar = df_actual[df_actual['Fecha'].astype(str) + " - " + df_actual['Día N'] == seleccion].index[0]
            fila = df_actual.loc[indice_a_editar]
            
            # Cargar datos al formulario
            defaults["fecha"] = fila['Fecha']
            defaults["dia_n"] = fila['Día N']
            defaults["pct_acum"] = float(fila['Físico Acum (%)'])
            defaults["monto_acum"]
