import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(layout="wide", page_title="SISTEMA DE GESTIÓN RDO & DASHBOARD", page_icon="⚡")

# --- ESTILOS VISUALES (Tabla y Etiquetas Numeradas) ---
st.markdown("""
<style>
    .main-header {font-size: 24px; font-weight: bold; color: #1E3A8A; margin-bottom: 10px;}
    
    /* Estilos para las etiquetas de los inputs (Números Rojos) */
    .stTextInput label, .stDateInput label, .stSelectbox label, .stTextArea label, .stNumberInput label {
        font-weight: bold !important;
        color: #b91c1c !important; 
        font-size: 15px !important;
    }

    /* Estilo para la Tabla Ficha Técnica */
    .ficha-tecnica {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
        font-family: Arial, sans-serif;
        font-size: 14px;
        border: 1px solid #ddd;
    }
    .ficha-tecnica th {
        background-color: #1E3A8A;
        color: white;
        padding: 8px;
        text-align: left;
        border: 1px solid #ddd;
    }
    .ficha-tecnica td {
        padding: 8px;
        border: 1px solid #ddd;
        background-color: #f9f9f9;
        color: #333;
    }
    .ficha-tecnica tr:nth-child(even) td {
        background-color: #f2f2f2;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/e4/Logotipo_de_CNEL.svg", width=150)
st.sidebar.title("Configuración")

# SELECTOR DE CONTRATO (Clave para cambiar los datos)
contrato_seleccionado = st.sidebar.selectbox(
    "Seleccione el Contrato/Zona:",
    ["ZONA 1 - SECTOR CAMARONERO", "ZONA 2 - SECTOR CAMARONERO"]
)

st.sidebar.markdown("---")
modulo = st.sidebar.radio("Navegación:", ["MÓDULO 1: RDO (Lista de 19 Puntos)", "MÓDULO 2: DASHBOARD (Lista de 8 Puntos)"])
st.sidebar.info(f"**Oferente:** Consorcio Fiscalred\n**Proceso:** Fiscalización Redes Eléctricas")

# --- FUNCIÓN PARA DATOS ESTÁTICOS (FICHA TÉCNICA) ---
# ¡AQUÍ ES DONDE DEBES PONER TUS DATOS REALES!
def obtener_ficha_tecnica(zona):
    if zona == "ZONA 1 - SECTOR CAMARONERO":
        return {
            "Entidad": "EMPRESA ELÉCTRICA PÚBLICA ESTRATÉGICA CORPORACIÓN NACIONAL DE ELECTRICIDAD CNEL EP - UNIDAD DE NEGOCIO EL ORO",
            "Categoría": "CONSTRUCCION DE REDES DE DISTRIBUCIONn",
            "Objeto": "EOR Construccion de redes electricas para proyectos PER sector camaronero zona 1 CAF GD",
            "Código": "COTO-CNELEP-2025-43",
            "Plazo": "150 Días Calendario",
            "Contratista": "CONSORCIO CAF ARENILLAS", # <--- PON AQUÍ EL REAL
            "Rep_Legal": "OSCAR LUIS YANANGOMEZ SUQUILANDA (Procurador Común)",                       # <--- PON AQUÍ EL REAL
            "Monto": "$ 399.743,03415",
            "Link": "https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/PC/informacionProcesoContratacion2.cpe?idSoliCompra=Mlped7h-x8tM2Mi5JzAbNVHBoqrlPkyFh2Yoxj85zQc,"
        }
    else:
        return {
            "Entidad": "EMPRESA ELÉCTRICA PÚBLICA ESTRATÉGICA CORPORACIÓN NACIONAL DE ELECTRICIDAD CNEL EP - UNIDAD DE NEGOCIO EL ORO",
            "Categoría": "CONSTRUCCION DE REDES DE DISTRIBUCION",
            "Objeto": "EOR Construccion de redes electricas para proyectos PER sector camaronero zona 2 CAF GD",
            "Código": "COTO-CNELEP-2025-44",
            "Plazo": "150 Días Calendario",
            "Contratista": "CONSORCIO REDES HUNTER",             # <--- PON AQUÍ EL REAL
            "Rep_Legal": "Cristhian Manuel Romero Freire (Procurador Común)",                      # <--- PON AQUÍ EL REAL
            "Monto": "$499.654,23906",
            "Link": "https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/PC/informacionProcesoContratacion2.cpe?idSoliCompra=VJCoFonyH1vOnVROGwOunGmr6qD3pTr-znOrgilqON0,"
        }

ficha = obtener_ficha_tecnica(contrato_seleccionado)

# --- FUNCIÓN PARA GRÁFICOS (SIMULACIÓN) ---
def obtener_datos_graficos(zona):
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

df_data, monto_obra = obtener_datos_graficos(contrato_seleccionado)

# --- VISUALIZACIÓN DE LA FICHA TÉCNICA (HTML) ---
# Esta función dibuja la tablita bonita arriba de todo
def dibujar_ficha(datos):
    html_table = f"""
    <table class="ficha-tecnica">
        <tr>
            <th colspan="4" style="text-align:center;">FICHA TÉCNICA DEL PROYECTO (CONTRATO DE OBRA)</th>
        </tr>
        <tr>
            <td><strong>Entidad:</strong></td>
            <td>{datos['Entidad']}</td>
            <td><strong>Categoría:</strong></td>
            <td>{datos['Categoría']}</td>
        </tr>
        <tr>
            <td><strong>Objeto de Proceso:</strong></td>
            <td colspan="3">{datos['Objeto']}</td>
        </tr>
        <tr>
            <td><strong>Código:</strong></td>
            <td>{datos['Código']}</td>
            <td><strong>Plazo de Entrega:</strong></td>
            <td>{datos['Plazo']}</td>
        </tr>
        <tr>
            <td><strong>Contratista Constructor:</strong></td>
            <td>{datos['Contratista']}</td>
            <td><strong>Representante Legal:</strong></td>
            <td>{datos['Rep_Legal']}</td>
        </tr>
        <tr>
            <td><strong>Monto Contratado USD:</strong></td>
            <td>{datos['Monto']}</td>
            <td><strong>Link Proceso:</strong></td>
            <td><a href="{datos['Link']}" target="_blank">Ver en SERCOP</a></td>
        </tr>
    </table>
    """
    st.markdown(html_table, unsafe_allow_html=True)

# ==============================================================================
# MÓDULO 1: RDO WEB (19 PUNTOS)
# ==============================================================================
if modulo == "MÓDULO 1: RDO (Lista de 19 Puntos)":
    st.markdown(f'<div class="main-header">Módulo 1: Registro Diario de Obra (RDO)</div>', unsafe_allow_html=True)
    
    # 1. MOSTRAR LA TABLA ESTÁTICA AQUÍ
    dibujar_ficha(ficha)

    st.warning("Formulario de Campo - Numeración conforme a TDR Pág. 28")

    with st.form("rdo_form"):
        # A. Datos Generales
        st.markdown("### A. Datos Generales")
        c1, c2 = st.columns(2)
        c1.date_input("1. Fechas de Ejecución", date.today())
        c2.text_input("4. Día de ejecución", "Día 15 - Jornada Ordinaria")
        
        c3, c4 = st.columns(2)
        c3.text_input("2. Datos Económicos del Contrato", "$ 67,490.10 (Fiscalización)")
        c4.text_input("3. Dato Económico total de los Proyectos", f"{ficha['Monto']} (Obra Civil/Eléctrica)")

        # B. Condiciones de Campo
        st.markdown("### B. Condiciones de Campo")
        col_clima, col_inc = st.columns(2)
        col_clima.selectbox("5. Condiciones climáticas", ["Soleado", "Nublado", "Lluvia Ligera", "Tormenta"])
        col_inc.selectbox("19. Registro de Incidentes o accidentes", ["Sin Novedades", "Incidente Leve", "Accidente Grave"])

        # C. Control de Avance
        st.markdown("### C. Control de Avance y Desempeño")
        st.info("**6. Progreso General del Contrato de Obra:**")
        
        m1, m2, m3 = st.columns(3)
        val_fis = df_data['Físico Real (%)'].iloc[5]
        m1.metric("6.i. % de Avance", f"{val_fis}%")
        m2.metric("6.i. $ de Avance", f"$ {(val_fis/100)*monto_obra:,.2f}")
        m3.metric("6.i. Avance Avaluado", f"$ {(val_fis/100)*monto_obra:,.2f}")
        
        st.text_input("6.ii. Avance prorrateado de los proyectos por Hito", "Hito #1: 100% | Hito #2: 45%")

        st.text_input("7. Indicadores de Desempeño y estimaciones", "CPI: 1.05 | SPI: 0.98 | Estimado al concluir: En presupuesto")
        
        cc1, cc2 = st.columns(2)
        cc1.selectbox("14. Control mediante Tabla de cantidades y Reporte de Avance diario", ["SI - Verificado", "NO"])
        cc2.text_input("15. Porcentaje total de los proyectos", f"{val_fis}% (Ponderado Global)")

        # Gráfico Punto 8
        st.markdown("**8. Curva de Avance – Valor Ganado – Simbología**")
        fig_rdo = go.Figure()
        fig_rdo.add_trace(go.Scatter(x=df_data['Mes'], y=df_data['Programado (%)'], name='Línea Base (PV)', line=dict(dash='dash')))
        fig_rdo.add_trace(go.Scatter(x=df_data['Mes'], y=df_data['Físico Real (%)'], name='Valor Ganado (EV)', fill='tozeroy'))
        fig_rdo.update_layout(height=300,
