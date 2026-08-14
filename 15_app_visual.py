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
    "📝 Registro de Equipos Nuevos",
    "👨‍🔧 Historial de Reparaciones (Taller)"
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


# =========================================================================
# 👨‍🔧 MÓDULO 4: HISTORIAL CLÍNICO CON BUSCADOR INTELIGENTE ESCALABLE (UPDATED)
# =========================================================================
elif opcion == "👨‍🔧 Historial de Reparaciones (Taller)":
    st.title("👨‍🔧 Historial Clínico de Equipamiento Médico")
    st.markdown("#### *Trazabilidad de mantenimiento preventivo/correctivo y auditoría de tiempo muerto.*")
    st.write("---")
    
    st.subheader("🔍 Panel de Búsqueda Avanzada e Historial por Activo")
    
    # 1. Creamos una fila de 3 columnas para los filtros escalables en la interfaz
    col_txt, col_tipo, col_ubica = st.columns([2, 1, 1])
    
    with col_txt:
        # Buscador por texto libre (Acepta Serie, Marca o Modelo)
        busqueda_texto = st.text_input("📝 Buscar por N° de Serie, Marca o Modelo:", placeholder="Ej: SN-MIND o Mindray...")
        
    try:
        # Traemos de forma única los tipos y ubicaciones que existen hoy cargados en MySQL
        conexion = conectar_base_datos()
        
        df_tipos = pd.read_sql("SELECT DISTINCT type_device FROM equipment;", conexion)
        df_ubicas = pd.read_sql("SELECT DISTINCT location FROM equipment;", conexion)
        conexion.close()
        
        # Armamos las listas de filtros agregando la opción universal "Todos"
        lista_tipos = ["-- Todos los Dispositivos --"] + list(df_tipos['type_device'].values)
        lista_ubicas = ["-- Todas las Ubicaciones --"] + list(df_ubicas['location'].values)
        
        with col_tipo:
            filtro_tipo = st.selectbox("⚙️ Filtrar por Tipo:", lista_tipos)
        with col_ubica:
            filtro_ubica = st.selectbox("📍 Filtrar por Servicio/Ubicación:", lista_ubicas)
            
        # =========================================================================
        # CONSTRUCCIÓN DE LA QUERY DINÁMICA CON PATRÓN 'LIKE'
        # =========================================================================
        # Iniciamos la consulta base que traerá los equipos que coincidan con los filtros
        query_busqueda = "SELECT id_equipment, type_device, brand, model, serial_number_factory, location FROM equipment WHERE 1=1"
        parametros = []
        
        # Si el usuario escribió algo en la barra de búsqueda, aplicamos el operador LIKE de MySQL
        if busqueda_texto:
            query_busqueda += " AND (serial_number_factory LIKE %s OR brand LIKE %s OR model LIKE %s)"
            termino_busqueda = f"%{busqueda_texto}%"
            parametros.extend([termino_busqueda, termino_busqueda, termino_busqueda])
            
        # Filtros directos por desplegable
        if filtro_tipo != "-- Todos los Dispositivos --":
            query_busqueda += " AND type_device = %s"
            parametros.append(filtro_tipo)
            
        if filtro_ubica != "-- Todas las Ubicaciones --":
            query_busqueda += " AND location = %s"
            parametros.append(filtro_ubica)
            
        # Ejecutamos la búsqueda de los equipos filtrados
        conexion = conectar_base_datos()
        mensajero = conexion.cursor(dictionary=True)
        mensajero.execute(query_busqueda, tuple(parametros))
        equipos_encontrados = mensajero.fetchall()
        mensajero.close()
        conexion.close()
        
        
        # 2. Si la búsqueda arrojó resultados, los procesamos de forma limpia
        if equipos_encontrados:
            st.write("---")
            st.markdown(f"#### 📋 Resultados Encontrados ({len(equipos_encontrados)} activos)")
            
            # Mapeamos los resultados para que el técnico elija el equipo exacto de la lista ya reducida
            opciones_filtradas = {}
            for eq in equipos_encontrados:
                label = f"ID: {eq['id_equipment']} | {eq['type_device']} - {eq['brand']} {eq['model']} (Serie: {eq['serial_number_factory']}) | Ubicación: {eq['location']}"
                opciones_filtradas[label] = eq['id_equipment']
                
            seleccion_final = st.selectbox("👇 Selecciona el equipo exacto para desplegar su Hoja de Vida:", list(opciones_filtradas.keys()))
            
            if seleccion_final:
                id_eq_final = opciones_filtradas[seleccion_final]
                
                # Desplegamos las Órdenes de Trabajo del equipo seleccionado con el reloj de tiempo muerto
                conexion = conectar_base_datos()
                query_historial = f"""
                SELECT 
                    w.id_work_order AS 'N° Orden',
                    w.type_maintenance AS 'Tipo',
                    w.date_work_start AS 'Fecha Inicio',
                    w.date_work_finish AS 'Fecha Fin',
                    -- Calculamos el tiempo muerto en horas con un decimal 
                    TIMESTAMPDIFF(MINUTE, w.date_work_start, w.date_work_finish) AS 'Minutos_Totales',
                    -- TIMESTAMPDIFF(MINUTE, w.date_work_start, w.date_work_finish) AS 'erTiempo Muto (Horas)',
                    w.description_fault AS 'Falla Reportada',
                    w.description_work_done AS 'Tarea Ejecutada',
                    w.technical_responsible AS 'Técnico'
                FROM work_order w
                WHERE w.id_equipment = {id_eq_final}
                ORDER BY w.date_work_start DESC;
                """
                df_historial = pd.read_sql(query_historial, conexion)
                conexion.close()

                             
                
                # =========================================================================
                # CORRECCIÓN DE MÉTRICAS Y RENDERIZADO VISUAL (CON CIERRE TRY/EXCEPT)
                # =========================================================================
                st.write("---")
                st.subheader(f"📊 Historial Clínico de Reparaciones (ID QR: {id_eq_final})")
                
                if not df_historial.empty:
                    # 1. Sumamos todos los minutos acumulados en el historial clínico usando la nueva columna
                    total_minutos_acumulados = df_historial['Minutos_Totales'].sum()
                    global_horas = total_minutos_acumulados // 60
                    global_minutos = total_minutos_acumulados % 60
                    
                    # Dibujamos el indicador grande arriba en formato humano
                    st.metric(label="🚨 Tiempo Muerto Total Acumulado en el Activo", value=f"{global_horas} hs {global_minutos} min")
                    
                    st.markdown("#### ⏳ Línea de Tiempo de Intervenciones Técnicas")
                    st.caption("Haz clic en cualquier orden de trabajo para desplegar el reporte técnico completo sin scroll.")
                    
                    # 2. Renderizamos cada fila como un bloque desplegable vertical (Estilo Acordeón)
                    for idx, fila in df_historial.iterrows():
                        # Procesamos de forma segura los minutos que viajan de la base de datos
                        minutos_puros = int(fila['Minutos_Totales']) if fila['Minutos_Totales'] else 0
                        
                        # División matemática exacta para separar horas y minutos residuales
                        horas_enteras = minutos_puros // 60
                        minutos_sobrantes = minutos_puros % 60
                        tiempo_formateado = f"{horas_enteras} hs {minutos_sobrantes} min"
                        
                        titulo_orden = f"🛠️ Orden N° {fila['N° Orden']} | Tipo: {fila['Tipo']} | Fecha: {fila['Fecha Inicio']}"
                        
                        with st.expander(titulo_orden):
                            c1, c2, c3 = st.columns(3)
                            with c1:
                                st.markdown(f"**📅 Fecha Finalización:** {fila['Fecha Fin'] if fila['Fecha Fin'] else '⚠️ En Proceso'}")
                            with c2:
                                # Mostramos el tiempo traducido a formato humano
                                st.markdown(f"**⏳ Horas Fuera de Servicio:** `{tiempo_formateado}`")
                            with c3:
                                st.markdown(f"**👨‍🔧 Técnico Responsable:** {fila['Técnico']}")
                            
                            st.write("---")
                            st.markdown("**🚨 Falla Reportada por el Servicio:**")
                            st.info(fila['Falla Reportada'])
                            
                            st.markdown("**✅ Tarea Técnica Ejecutada / Repuestos:**")
                            st.success(fila['Tarea Ejecutada'])
                else:
                    st.info("ℹ️ Este activo biomédico no registra ninguna intervención técnica en el historial (Hoja de vida limpia).")
                    
  
    except Exception as e:
        st.error(f"❌ Error al consultar la base de datos de historial: {e}")