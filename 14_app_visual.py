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

# Configuración estructural de la interfaz en tu ThinkPad
st.set_page_config(page_title="CMMS - Estándar OMS", page_icon="🏥", layout="wide")

# Conector seguro usando el proxy local 'tecnico_biomedica' libre de bloqueos de Linux
def conectar_base_datos():
    return mysql.connector.connect(
        host="localhost",
        user="tecnico_biomedica",
        password="biomedica123",
        database="healthcare_system_db"
    )

# --- MENÚ LATERAL DE ROUTING (Añadimos tu nuevo Paso 2 de forma independiente) ---
st.sidebar.markdown("## 🏥 Gestión Biomédica (R&D Log)")
st.sidebar.write("---")
opcion = st.sidebar.selectbox("Módulos del Sistema:", [
    "📊 Inventario (Estándar OMS)",
    "🏭 Registro de Proveedores",
    "📝 Registro de Equipos Nuevos"
])

# =========================================================================
# 📊 MÓDULO 1: VER INVENTARIO CON CAMPOS DE LA OMS
# =========================================================================
if opcion == "📊 Inventario (Estándar OMS)":
    st.title("⚙️ Control de Activos y Ciclo de Vida")
    st.markdown("#### *Campos analíticos sincronizados bajo las normativas de la OMS.*")
    st.write("---")
    
    try:
        conexion = conectar_base_datos()
        # Modificamos la query para traer los nuevos campos de energía y auditoría
        query_oms = """
        SELECT 
            id_equipment AS 'ID QR',
            brand AS 'Fabricante',
            model AS 'Modelo',
            serial_number_factory AS 'N° de Serie',
            power_requirements AS 'Energía (OMS)',
            year_manufactured AS 'Año Fab.',
            ( YEAR(CURDATE()) - year_manufactured ) AS 'Años de Antigüedad',
            state AS 'Estado',
            location AS 'Servicio',
            id_supplier AS 'ID Proveedor',
            date_inventory_updated AS 'Última Actualización'
        FROM equipment;
        """
        df = pd.read_sql(query_oms, conexion)
        conexion.close()
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error en el servidor: {e}")

# =========================================================================
# 🏭 MÓDULO 2: ALTA INDEPENDIENTE DE PROVEEDORES (CORREGIDO CON TU ESQUEMA)
# =========================================================================
elif opcion == "🏭 Registro de Proveedores":
    st.title("🏭 Agenda de Soporte Técnico y Fabricantes")
    st.markdown("#### *Registro independiente de empresas comerciales y servicios técnicos.*")
    st.write("---")
    
    st.subheader("📋 Datos de Contacto de la Empresa")
    col1, col2 = st.columns(2)
    with col1:
        nombre_prov = st.text_input("🏢 Nombre Comercial de la Empresa (Ej: MEDITEA):").strip()
        email_prov = st.text_input("📧 Correo General de la Empresa:")
    with col2:
        phone_prov = st.text_input("📞 Teléfono Comercial / Oficina:")
    
    st.write("---")
    st.subheader("👨‍🔧 Datos Especializados de Soporte Técnico (Electromedicina)")
    col3, col4 = st.columns(2)
    with col3:
        responsable = st.text_input("👤 Nombre del Ingeniero / Técnico de Aplicaciones:")
        # 🛠️ TU TAREA: Crea el casillero de Streamlit para el email de soporte técnico
        email_soporte = st.text_input("📬 Correo Directo de Soporte Técnico:")
    with col4:
        # 🛠️ TU TAREA: Crea el casillero de Streamlit para el teléfono de soporte técnico
        phone_soporte = st.text_input("📱 Teléfono Celular de Guardia de Soporte:")

    if st.button("💾 Guardar Proveedor en la Agenda", use_container_width=True):
        if nombre_prov and email_prov:
            try:
                conexion = conectar_base_datos()
                mensajero = conexion.cursor()
                
                # 🛠️ TU TAREA: Agrega las columnas faltantes en la consulta SQL
                query_prov = """
                INSERT INTO supplier (
                    name_supplier, 
                    email, 
                    phone, 
                    technical_support, 
                    phone_technical_support, 
                    email_technical_support
                ) 
                VALUES (%s, %s, %s, %s, %s, %s);
                """
                
                # Empaquetamos las 6 variables en el orden exacto de las columnas de MySQL
                datos_proveedor = (
                    nombre_prov, 
                    email_prov, 
                    phone_prov, 
                    responsable, 
                    phone_soporte, 
                    email_soporte
                )
                
                mensajero.execute(query_prov, datos_proveedor)
                conexion.commit()
                mensajero.close()
                conexion.close()
                
                st.success(f"🎉 Empresa '{nombre_prov}' y su equipo de soporte registrados exitosamente en la agenda.")
            except Exception as e:
                st.error(f"❌ Error crítico al intentar inyectar en MySQL: {e}")
        else:
            st.warning("⚠️ El Nombre de la empresa y el Email general son obligatorios para abrir la ficha de proveedor.")


# =========================================================================
# 📝 MÓDULO 3: TU PASO 1 - ALTA DINÁMICA DE EQUIPOS (OPCIONAL/NULL)
# =========================================================================
elif opcion == "📝 Registro de Equipos Nuevos":
    st.title("📝 Data Entry - Registro de Nuevos Activos")
    st.write("---")
    
    try:
        # TRUCO DINÁMICO: Traemos los proveedores vivos de MySQL para armar la lista web
        conexion = conectar_base_datos()
        query_combo = "SELECT id_supplier, name_supplier FROM supplier;"
        df_prov = pd.read_sql(query_combo, conexion)
        conexion.close()
        
        # Estructuramos la lista para mostrar "ID - Nombre" y agregamos tu opción comodín NULL
        lista_proveedores = ["❌ Sin proveedor asignado por el momento"]
        for idx, fila in df_prov.iterrows():
            lista_proveedores.append(f"{fila['id_supplier']} - {fila['name_supplier']}")
            
    except Exception:
        lista_proveedores = ["❌ Sin proveedor asignado por el momento"]

    col1, col2 = st.columns(2)
    with col1:
        serie = st.text_input("🔌 Número de Serie de Fábrica:").strip()
        tipo = st.text_input("⚙️ Tipo de Dispositivo:")
        categoria = st.text_input("📁 Categoría (Ej: Kinesiología):")
        marca = st.text_input("🏭 Marca del Fabricante:")
    with col2:
        modelo = st.text_input("📦 Modelo:")
        anio = st.number_input("📅 Año de Fabricación:", min_value=1980, max_value=2026, value=2026, step=1)
        ubicacion = st.text_input("📍 Ubicación / Servicio:")
        energia = st.text_input("⚡ Requerimientos de Energía (OMS):", value="220V / Batería interna")
        
        # TU PASO 1 EN PANTALLA: El menú desplegable dinámico
        prov_seleccionado = st.selectbox("🏭 Asignar Proveedor de Soporte Técnico:", lista_proveedores)

    if st.button("🚀 Guardar Equipo en el Inventario", use_container_width=True):
        if serie and tipo and categoria:
            try:
                # TRADUCCIÓN AUTOMÁTICA: Si elige el comodín, mandamos None (NULL en SQL)
                if prov_seleccionado == "❌ Sin proveedor asignado por el momento":
                    id_final_proveedor = None
                else:
                    # Cortamos el texto para quedarnos solo con el número de ID
                    id_final_proveedor = int(prov_seleccionado.split(" - ")[0])
                
                conexion = conectar_base_datos()
                mensajero = conexion.cursor()
                
                # Plantilla SQL actualizada con el nuevo campo de energía de la OMS
                query_insertar = """
                INSERT INTO equipment (
                    serial_number_factory, type_device, category, brand, model, 
                    year_manufactured, state, location, id_supplier, power_requirements
                ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                datos_equipo = (serie, tipo, categoria, marca, modelo, int(anio), 'OK', ubicacion, id_final_proveedor, energia)
                
                mensajero.execute(query_insertar, datos_equipo)
                conexion.commit()
                mensajero.close()
                conexion.close()
                
                st.success(f"🎉 ¡Equipo registrado exitosamente!")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Error en MySQL: {e}")
