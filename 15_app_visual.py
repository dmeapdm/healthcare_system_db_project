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


# --- MENÚ LATERAL DE ROUTING (Añadimos tu nuevo Paso 2 de forma independiente) ---
st.sidebar.markdown("## 🏥 Gestión Biomédica (R&D Log)")
st.sidebar.write("---")
opcion = st.sidebar.selectbox("Módulos del Sistema:", [
    "📊 Inventario (Estándar OMS)",
    "🏭 Registro de Proveedores",
    "📝 Registro de Equipos Nuevos",
    "👨‍🔧 Historial de Reparaciones (Taller)",
    "📝 Nueva Orden de Trabajo" # <-- NUEVA POSTA OPERATIVA DE HOY
    "📝 Nueva Orden de Trabajo",
    "📦 Almacén y Control de Stock"
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



# =========================================================================
# 📝 MÓDULO 5: NUEVA ORDEN DE TRABAJO CON AUDITORÍA TRANSACCIONAL DE STOCK
# =========================================================================
elif opcion == "📝 Nueva Orden de Trabajo":
    st.title("📝 Apertura y Cierre de Orden de Trabajo")
    st.markdown("#### *Registro técnico con asignación y movimientos automatizados de stock.*")
    st.write("---")
    
    st.subheader("🔍 Identificación del Activo")
    serie_orden = st.text_input("🔌 Número de Serie del Equipo:", placeholder="Ej: SN-MIND-9982...").strip()
    
    id_equipment_encontrado = None
    servicio_equipo = "Desconocido"
    if serie_orden:
        try:
            conexion = conectar_base_datos()
            mensajero = conexion.cursor(dictionary=True)
            mensajero.execute("SELECT id_equipment, type_device, brand, model, location FROM equipment WHERE serial_number_factory = %s;", (serie_orden,))
            activo = mensajero.fetchone()
            mensajero.close()
            conexion.close()
            if activo:
                id_equipment_encontrado = activo['id_equipment']
                servicio_equipo = activo['location']
                st.success(f"✅ **Equipo Vinculado:** {activo['type_device']} | {activo['brand']} {activo['model']} (Servicio: {servicio_equipo} | ID QR: {id_equipment_encontrado})")
            else: st.error("❌ El Número de Serie no existe en el inventario.")
        except Exception as e: st.error(f"❌ Error: {e}")
            
    st.write("---")
    st.subheader("📋 Datos del Reporte")
    c_maint, c_tec = st.columns(2)
    with c_maint: tipo_maint = st.selectbox("⚙️ Tipo:", ["corrective", "preventive"])
    with c_tec: tecnico_firmante = st.text_input("👤 Técnico Responsable (Tu Nombre):").strip()
        
    falla_reportada = st.text_area("🚨 Falla Reportada / Síntomas:")
    trabajo_realizado = st.text_area("✅ Trabajo Técnico Ejecutado:")
    
    st.write("---")
    st.subheader("📦 Consumo de Repuestos y Accesorios Clínicos")
    
    insumos_seleccionados = []
    cantidades_insumos = {}
    mapa_ids_repuestos = {}
    
    try:
        conexion = conectar_base_datos()
        # Traemos los Grupos y Categorías orgánicas de tu nueva tabla inputs
        df_tipos_inv = pd.read_sql("SELECT DISTINCT input_type FROM inputs WHERE is_active = TRUE;", conexion)
        df_cats_inv = pd.read_sql("SELECT DISTINCT input_category FROM inputs WHERE is_active = TRUE;", conexion)
        conexion.close()
        
        c_f1, c_f2 = st.columns(2)
        with c_f1: filtro_t = st.selectbox("🎯 Filtrar por Tipo de Almacén:", ["-- Todos --"] + list(df_tipos_inv['input_type'].values))
        with c_f2: filtro_c = st.selectbox("📁 Filtrar por Categoría Clínica:", ["-- Todas --"] + list(df_cats_inv['input_category'].values))
            
        query_parts = "SELECT id_inputs, internal_code, brand, model_ref, name_input, stock, unit_of_measure FROM inputs WHERE is_active = TRUE"
        params_parts = []
        if filtro_t != "-- Todos --": query_parts += " AND input_type = %s"; params_parts.append(filtro_t)
        if filtro_c != "-- Todas --": query_parts += " AND input_category = %s"; params_parts.append(filtro_c)
            
        conexion = conectar_base_datos()
        df_parts = pd.read_sql(query_parts, conexion, params=params_parts)
        conexion.close()
        
        opciones_repuestos = []
        for idx, fila in df_parts.iterrows():
            label = f"{fila['internal_code']} | {fila['brand']} {fila['model_ref']} | {fila['name_input']} ({fila['stock']} {fila['unit_of_measure']} disp.)"
            opciones_repuestos.append(label)
            mapa_ids_repuestos[label] = (fila['id_inputs'], fila['stock'], fila['name_input'])
            
        insumos_seleccionados = st.multiselect("🔍 Selecciona las partes utilizadas (puedes elegir varias):", opciones_repuestos)
        
        if insumos_seleccionados:
            st.write("🔢 **Especificar las cantidades utilizadas:**")
            columnas_cantidades = st.columns(len(insumos_seleccionados))
            for i, item in enumerate(insumos_seleccionados):
                with columnas_cantidades[i]:
                    _, max_disp, nom_ins_c = mapa_ids_repuestos[item]
                    cantidades_insumos[item] = st.number_input(f"{nom_ins_c[:20]}... :", min_value=1, max_value=max_disp if max_disp > 0 else 1, value=1, key=f"cant_wo_{i}")
    except Exception as e: st.error(f"❌ Error al mapear almacén: {e}")
        
    st.write("---")
    if st.button("🚀 Registrar Orden y Generar Movimientos de Stock", use_container_width=True):
        if id_equipment_encontrado is None: st.error("🚫 Operación bloqueada: Se necesita un Número de Serie válido.")
        elif tecnico_firmante and falla_reportada and trabajo_realizado:
            try:
                conexion = conectar_base_datos()
                mensajero = conexion.cursor()
                
                # 1. Insertamos la orden de trabajo principal
                query_insert_order = "INSERT INTO work_order (id_equipment, date_work_start, date_work_finish, type_maintenance, description_fault, description_work_done, technical_responsible) VALUES (%s, NOW(), NOW(), %s, %s, %s, %s);"
                mensajero.execute(query_insert_order, (id_equipment_encontrado, tipo_maint, falla_reportada, trabajo_realizado, tecnico_firmante))
                id_wo = mensajero.lastrowid
                
                # 2. Bucle transaccional: Actualiza stock e inserta en tu nueva tabla de movimientos
                for item in insumos_seleccionados:
                    id_insumo, _, _ = mapa_ids_repuestos[item]
                    cantidad_usada = cantidades_insumos[item]
                    
                    # Enlace clásico N a N
                    mensajero.execute("INSERT INTO work_order_inputs (id_work_order, id_inputs, quantity_used) VALUES (%s, %s, %s);", (id_wo, id_insumo, cantidad_usada))
                    # Descuento físico en inputs
                    mensajero.execute("UPDATE inputs SET stock = stock - %s WHERE id_inputs = %s;", (cantidad_usada, id_insumo))
                    
                    # 💡 NUEVO: Tu auditoría transaccional en stock_movements
                    query_mov = """
                    INSERT INTO stock_movements (id_inputs, id_work_order, movement_type, quantity, destination_service, requested_by, dispatched_by, notes) 
                    VALUES (%s, %s, 'salida_orden', %s, %s, %s, %s, %s);
                    """
                    notas_mov = f"Consumido de forma automática en reparación bajo Orden de Trabajo N° {id_wo}."
                    mensajero.execute(query_mov, (id_insumo, id_wo, cantidad_usada, servicio_equipo, tecnico_firmante, tecnico_firmante, notas_mov))
                    
                conexion.commit()
                mensajero.close()
                conexion.close()
                st.success(f"🎉 ¡Orden N° {id_wo} guardada! Movimientos de stock auditados en tu nueva tabla relacional.")
                st.balloons()
            except Exception as e: st.error(f"❌ Error transaccional MySQL: {e}")
        else: st.warning("⚠️ Completa los campos obligatorios.")

# =========================================================================
# 📦 MÓDULO 6: ALMACÉN CON DESCUENTO DIRECTO Y BITÁCORA DE MOVIMIENTOS
# =========================================================================
elif opcion == "📦 Almacén y Control de Stock":
    st.title("📦 Almacén Unificado de Electromedicina")
    st.write("---")
    
    pestana_ver, pestana_egreso, pestana_kardex = st.tabs(["📋 Ver Stock Actual", "📉 Salida Directa (Sin Orden)", "📜 Bitácora de Movimientos (Kardex)"])
    
    with pestana_ver:
        st.subheader("📋 Estado Organizado del Almacén")
        try:
            conexion = conectar_base_datos()
            query_master_stock = """
            SELECT 
                i.id_inputs AS 'ID', i.internal_code AS 'Código', i.input_type AS 'Grupo', 
                i.input_category AS 'Categoría', i.brand AS 'Marca', i.model_ref AS 'Modelo/REF', 
                i.name_input AS 'Descripción', i.stock AS 'Cant.', i.unit_of_measure AS 'Unidad', 
                i.min_stock_alert AS 'Mínimo', i.unit_price AS 'Precio U.', s.name_supplier AS 'Proveedor'
            FROM inputs i
            LEFT JOIN supplier s ON i.id_supplier = s.id_supplier
            WHERE i.is_active = TRUE;
            """
            df_stock = pd.read_sql(query_master_stock, conexion)
            conexion.close()
            st.dataframe(df_stock, use_container_width=True)
            
            criticos = df_stock[df_stock['Cant.'] <= df_stock['Mínimo']]
            if not criticos.empty:
                st.error(f"🚨 **Alerta Crítica de Almacén:** ¡Hay {len(criticos)} artículos en nivel de reposición obligatoria!")
                st.write(criticos[['Código', 'Descripción', 'Cant.']])
        except Exception as e: st.error(f"❌ Error: {e}")
            
    with pestana_egreso:
        st.subheader("📉 Egreso Directo de Almacén (Para UCI / Guardia / Emergencias)")
        st.caption("Usa esta pestaña para despachar un insumo médico de inmediato sin asociarlo a ninguna orden de trabajo.")
        
        try:
            conexion = conectar_base_datos()
            df_eg_combo = pd.read_sql("SELECT id_inputs, internal_code, name_input, stock, unit_of_measure FROM inputs WHERE is_active = TRUE;", conexion)
            conexion.close()
            
            lista_egresos = []
            mapa_egresos = {}
            for idx, fila in df_eg_combo.iterrows():
                lbl = f"{fila['internal_code']} | {fila['name_input']} ({fila['stock']} {fila['unit_of_measure']} disp.)"
                lista_egresos.append(lbl)
                mapa_egresos[lbl] = (fila['id_inputs'], fila['stock'], fila['name_input'])
                
            item_egreso = st.selectbox("📦 Selecciona el insumo clínico a despachar:", lista_egresos)

            c_eg1, c_eg2 = st.columns(2)
            with c_eg1: 
                cant_egreso = st.number_input("🔢 Cantidad a Retirar:", min_value=1, step=1)
            with c_eg2: 
                servicio_destino = st.selectbox("📍 Servicio Destino:", ["UCI", "Neonatología", "Guardia", "Quirófano", "Piso Internación"])

            c_eg3, c_eg4 = st.columns(2)
            with c_eg3: 
                solicita = st.text_input("👤 Solicitado por (Ej. Enfermera Jefa):").strip()
            with c_eg4: 
                entrega = st.text_input("👤 Entregado por (Técnico de Electromedicina):").strip()
            notas_egreso = st.text_input("📝 Notas o Justificación:", placeholder="Ej: Reposición de emergencia por rotura de sensor anterior...")
            if st.button("📉 Confirmar Despacho Directo e Impactar Auditoría", use_container_width=True):
                id_ins, st_disp, nom_ins = mapa_egresos[item_egreso]
                if solicita and entrega:
                    if st_disp >= cant_egreso:
                        conexion = conectar_base_datos()
                        mensajero = conexion.cursor()
                        # 1. Descontamos el stock de la tabla maestra
                        mensajero.execute("UPDATE inputs SET stock = stock - %s WHERE id_inputs = %s;", (cant_egreso, id_ins))
                        # 2. 💡 NUEVO: Registramos la auditoría transparente en stock_movements con id_work_order = NULL
                        query_mov_directo = """INSERT INTO stock_movements (id_inputs, id_work_order, movement_type, quantity, destination_service, requested_by, dispatched_by, notes)VALUES (%s, NULL, 'salida_directa', %s, %s, %s, %s, %s);"""
                        mensajero.execute(query_mov_directo, (id_ins, cant_egreso, servicio_destino, solicita, entrega, notas_egreso))
                        conexion.commit()
                        mensajero.close()
                        conexion.close()
                        st.success(f"✅ ¡Despacho exitoso! Se descontaron {cant_egreso} unidades de '{nom_ins}' destinadas a {servicio_destino}.")
                        st.balloons()
                    else:
                        st.error("🚫 Error: Cantidad insuficiente en stock.")
                else:
                    st.warning("⚠️ Los campos de personal (quién solicita y quién entrega) son obligatorios.")
        except Exception as e:
                st.error(f"❌ Error operativo: {e}")
# -------------------------------------------------------------------------# 
# 📜 PESTAÑA 3: LA BITÁCORA KARDEX EN VIVO (MUESTRA TU NUEVA TABLA)#
# -------------------------------------------------------------------------
    with pestana_kardex:
        st.subheader("📜 Libro de Actas e Historial Logístico (Kardex)")
        st.caption("Bitácora inmutable de auditoría. Cada movimiento de stock, compra o ajuste se registra aquí cronológicamente.")
        try:
            conexion = conectar_base_datos()
            query_kardex = """
            SELECT
                sm.id_movement AS 'N° Ref',
                i.internal_code AS 'Código Insumo',
                i.name_input AS 'Descripción',
                sm.movement_type AS 'Tipo Movimiento',
                sm.quantity AS 'Cantidad',
                sm.destination_service AS 'Destino/Servicio',
                sm.requested_by AS 'Solicitante',
                sm.dispatched_by AS 'Despachante',
                sm.movement_date AS 'Fecha/Hora',
                sm.notes AS 'Observaciones'
            FROM stock_movements sm
            JOIN inputs i ON sm.id_inputs = i.id_inputs
            ORDER BY sm.movement_date DESC;
            """
            df_kardex = pd.read_sql(query_kardex, conexion)
            conexion.close()
            st.dataframe(df_kardex, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Error al leer la bitácora: {e}")