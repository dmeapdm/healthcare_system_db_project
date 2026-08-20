"""
🏥 SYSTEM: CMMS BIOMEDICAL WORKSPACE (GUIs MODULE)
👨‍💻 DEVELOPER: Electromedicina - Hospital Heller
🛠️ DESIGN PATTERN: Modular Interface with Secure Local Pipelines

STORYTELLING AND CONTEXT:
This application is designed to be the central brain of Biomedical Engineering.
It solves two real-world hospital problems:
1. Network Instability: It runs lightweight memory frames (Pandas) to render fast even on slow Wi-Fi.
2. Kernel Security Lockout: It drops the restrictive Linux 'root' profile and routes all traffic
   through a dedicated local application pipeline ('tecnico_biomedica') to bypass auth_socket blocks.
"""


import streamlit as st
import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()  # carga las variables del archivo .env

def conectar_base_datos():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )






# =========================================================================
# 🏗️ STAGE 1: WEB INFRASTRUCTURE AND VIEWPORT CONFIGURATION
# =========================================================================
# We override standard layout constraints. We need a 'wide' frame to comfortable
# visualize wide data matrices, metric counters, and timelines on our ThinkPad laptop.
st.set_page_config(
    page_title="CMMS Electromedicina - Hospital Heller", 
    page_icon="🏥",
    layout="wide"
)

# =========================================================================
# 🔌 STAGE 2: SECURE DATABASE CONNECTOR PIPELINE
# =========================================================================
def conectar_base_datos():
    """
    Establishes the communication bridge with the local MySQL server.
    CRITICAL SECURITY ARCHITECTURE: We use 'tecnico_biomedica' account.
    This bypasses Ubuntu's root auth_socket guard, allowing frictionless 
    TCP/IP internal piping.
    """
    return mysql.connector.connect(
           host=os.getenv("DB_HOST"),
           user=os.getenv("DB_USER"),
           password=os.getenv("DB_PASSWORD"),
           database=os.getenv("DB_NAME")
       )
   
# =========================================================================
# 🎛️ STAGE 3: INTERACTIVE NAVIGATION SIDEBAR (UX LAYER)
# =========================================================================
# The sidebar acts as the central router. It separates everyday diagnostic tasks 
# (QR/Inventory scans) from heavy data-entry operations (Notebook operations).
st.sidebar.markdown("## 🏥 Sistema de Gestión Biomédica")
st.sidebar.write("---")
st.sidebar.markdown("### 🗺️ Navegación Principal")

opcion = st.sidebar.selectbox(
    "Selecciona la acción a ejecutar:", 
    [
        "📊 Inventario y Antigüedad",
        "📝 Registro de Equipos Nuevos"
    ]
)

st.sidebar.write("---")
st.sidebar.caption("💻 Taller de Electromedicina | Entorno Local Activo")

# =========================================================================
# 📊 MODULE 1: REAL-TIME INVENTORY AND DYNAMIC LIFESPAN METRICS
# =========================================================================
if opcion == "📊 Inventario y Antigüedad":
    st.title("⚙️ Control de Activos y Años de Antigüedad")
    st.markdown("#### *Monitoreo clínico de ciclo de vida de equipamiento médico.*")
    st.write("---")
    
    try:
        # Step 1: Open the channel with the secure database pipeline
        conexion = conectar_base_datos()
        
        # LOGIC PATTERN: The calculation is automated at the core level (MySQL).
        # We don't hardcode years. YEAR(CURDATE()) guarantees the system stays
        # alive and mathematically correct as years pass without manual updates.
        query_antiguedad = """
        SELECT 
            id_equipment AS 'ID QR',
            brand AS 'Marca',
            model AS 'Modelo',
            serial_number_factory AS 'N° de Serie',
            year_manufactured AS 'Año Fab.',
            ( YEAR(CURDATE()) - year_manufactured ) AS 'Años de Antigüedad',
            state AS 'Estado Operativo',
            location AS 'Ubicación Servicio'
        FROM equipment;
        """
        
        # Step 2: Extract data chunks via Pandas and cache them into an interactive Frame
        df = pd.read_sql(query_antiguedad, conexion)
        
        # Step 3: Close connection immediately to conserve memory and shield against data leakage
        conexion.close()
        
        # Step 4: Render data grid. Streamlit injects live filters and sorting automatically.
        st.subheader("📋 Grilla de Activos en Servicio")
        st.dataframe(df, use_container_width=True)
        
        # Visual statistics indicators (Preparation for upcoming dashboard layer)
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Total de Equipos Monitoreados", value=len(df))
        with col2:
            st.caption("💡 *Tip Técnico:* Puedes ordenar por antigüedad haciendo clic en la cabecera de la columna.")
        
    except Exception as e:
        # Safe failure mode: If the Wi-Fi or server stumbles, the UI displays a clean alert
        st.error(f"❌ Error crítico de comunicación con el motor de base de datos: {e}")

# =========================================================================
# 📝 MODULE 2: DATA ENTRY SYSTEM FOR ACTIVE INVENTORY (WORK IN PROGRESS)
# =========================================================================
elif opcion == "📝 Registro de Equipos Nuevos":
    st.title("📝 Data Entry - Registro de Nuevos Activos")
    st.markdown("#### *Alta patrimonial de dispositivos biomédicos en el servidor local.*")
    st.write("---")
    
    st.info(
        "💡 **Próximo Paso en Electromedicina:** Aquí diseñaremos los campos de texto estructurados "
        "(`st.text_input`) para capturar variables físicas (Marca, Modelo, Serie) y mandarlos directos "
        "a MySQL con un botón, eliminando la necesidad de volver a tipear scripts en el taller."
    )
