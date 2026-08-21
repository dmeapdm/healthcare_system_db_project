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
# 📝 MÓDULO 5: NUEVA ORDEN DE TRABAJO CON SELECCIÓN POR CÓDIGO (ANTI-SCROLL)
# =========================================================================
elif opcion == "📝 Nueva Orden de Trabajo":
    st.title("📝 Apertura y Cierre de Orden de Trabajo")
    st.markdown("#### *Registro técnico con asignación por código de barra/interno y auditoría de stock.*")
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
    
    # --- TU MEJORA: AGREGAR INSUMOS DIRECTO POR CÓDIGO INTERNO ---
    st.write("---")
    st.subheader("📦 Consumo de Repuestos e Insumos Clínicos")
    st.caption("Digita el código interno del repuesto que tienes en la mano (ej: 6690 o 12071) para verificar stock y agregarlo al reporte.")
    
    # Usamos la memoria de Streamlit st.session_state para simular el botón "+" dinámico
    if "lista_codigos_wo" not in st.session_state:
        st.session_state.lista_codigos_wo = []
        
    col_cod, col_btn_add = st.columns([3, 1])
    with col_cod:
        codigo_tipeado = st.text_input("🔑 Digita el Código Interno del Repuesto:", key="input_cod_wo", placeholder="Ej: 6690...").strip()
    with col_btn_add:
        st.write("##") # Espacio estético
        if st.button("➕ Adherir Repuesto", use_container_width=True):
            if codigo_tipeado and codigo_tipeado not in st.session_state.lista_codigos_wo:
                st.session_state.lista_codigos_wo.append(codigo_tipeado)
                
    # Procesamos y descontamos los insumos adheridos dinámicamente
    id_insumos_finales = {}
    if st.session_state.lista_codigos_wo:
        st.write("📋 **Lista de Repuestos Adheridos a la Orden de Trabajo:**")
        for codigo in st.session_state.lista_codigos_wo:
            try:
                conexion = conectar_base_datos()
                cursor_chk = conexion.cursor(dictionary=True)
                cursor_chk.execute("SELECT id_inputs, name_input, stock, unit_of_measure FROM inputs WHERE internal_code = %s AND is_active = TRUE;", (codigo,))
                ins_data = cursor_chk.fetchone()
                cursor_chk.close()
                conexion.close()
                
                if ins_data:
                    c_lbl, c_cant, c_del = st.columns([3, 1, 1])
                    with c_lbl:
                        st.info(f"📦 **{codigo}** | {ins_data['name_input']} (Disponibles: {ins_data['stock']} {ins_data['unit_of_measure']})")
                    with c_cant:
                        # Casillero numérico individual limitado por el stock físico real
                        id_insumos_finales[ins_data['id_inputs']] = st.number_input(f"Cantidad:", min_value=1, max_value=ins_data['stock'] if ins_data['stock'] > 0 else 1, value=1, key=f"cant_wo_{codigo}")
                    with c_del:
                        st.write("##")
                        if st.button("🗑️ Quitar", key=f"del_wo_{codigo}"):
                            st.session_state.lista_codigos_wo.remove(codigo)
                            st.rerun()
                else:
                    st.warning(f"⚠️ El código '{codigo}' no corresponde a ningún artículo activo en el almacén.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
                
    st.write("---")
    if st.button("🚀 Registrar Orden y Descontar Almacén", use_container_width=True):
        if id_equipment_encontrado is None: st.error("🚫 Operación bloqueada: Se necesita un Número de Serie de equipo válido.")
        elif not id_insumos_finales: st.error("🚫 Operación bloqueada: Debes adherir al menos un repuesto por código.")
        elif tecnico_firmante and falla_reportada and trabajo_realizado:
            try:
                conexion = conectar_base_datos()
                mensajero = conexion.cursor()
                
                query_insert_order = "INSERT INTO work_order (id_equipment, date_work_start, date_work_finish, type_maintenance, description_fault, description_work_done, technical_responsible) VALUES (%s, NOW(), NOW(), %s, %s, %s, %s);"
                mensajero.execute(query_insert_order, (id_equipment_encontrado, tipo_maint, falla_reportada, trabajo_realizado, tecnico_firmante))
                id_wo = mensajero.lastrowid
                
                # Bucle transaccional sobre tus repuestos adheridos
                for id_ins, cant_usada in id_insumos_finales.items():
                    mensajero.execute("INSERT INTO work_order_inputs (id_work_order, id_inputs, quantity_used) VALUES (%s, %s, %s);", (id_wo, id_ins, cant_usada))
                    mensajero.execute("UPDATE inputs SET stock = stock - %s WHERE id_inputs = %s;", (cant_usada, id_ins))
                    
                    query_mov = """
                    INSERT INTO stock_movements (id_inputs, id_work_order, movement_type, quantity, destination_service, requested_by, dispatched_by, notes) 
                    VALUES (%s, %s, 'salida_orden', %s, %s, %s, %s, %s);
                    """
                    notas_mov = f"Consumido de forma automática en reparación bajo Orden de Trabajo N° {id_wo}."
                    mensajero.execute(query_mov, (id_ins, id_wo, cant_usada, servicio_equipo, tecnico_firmante, tecnico_firmante, notas_mov))
                    
                conexion.commit()
                mensajero.close()
                conexion.close()
                
                st.session_state.lista_codigos_wo = [] # Limpiamos la lista para la próxima orden
                st.success(f"🎉 ¡Orden N° {id_wo} guardada exitosamente con descuento transaccional!")
                st.balloons()
                st.rerun()
            except Exception as e: st.error(f"❌ Error transaccional MySQL: {e}")
        else: st.warning("⚠️ Completa los campos obligatorios del reporte técnico.")


# =========================================================================
# 📦 MÓDULO 6: ALMACÉN CON BUSCADOR DE UBICACIÓN INTEGRADO Y KARDEX
# =========================================================================
elif opcion == "📦 Almacén y Control de Stock":
    st.title("📦 Almacén Unificado de Electromedicina")
    st.write("---")
    
    pestana_ver, pestana_egreso, pestana_kardex = st.tabs(["📋 Ver y Buscar Ubicación", "📉 Salida Directa (Por Código)", "📜 Bitácora de Movimientos (Kardex)"])
    
    # -------------------------------------------------------------------------
    # PESTAÑA 1: TU REQUERIMIENTO - LOCALIZADOR RÁPIDO DE ESTANTES Y CAJONES
    # -------------------------------------------------------------------------
    with pestana_ver:
        st.subheader("🔍 Localizador de Repuestos y Consulta de Stock")
        txt_buscar_almacen = st.text_input("🔎 Escribe el nombre o marca del repuesto para saber DÓNDE está guardado:", placeholder="Ej: manguito, Nellcor, estaño...").strip()
        
        try:
            conexion = conectar_base_datos()
            query_master_stock = """
            SELECT 
                i.id_inputs AS 'ID', i.internal_code AS 'Código', i.input_type AS 'Grupo', 
                i.input_category AS 'Categoría', i.brand AS 'Marca', i.model_ref AS 'Modelo/REF', 
                i.name_input AS 'Descripción', i.cabinet_space AS 'Mueble/Estante', i.drawer_location AS 'Cajón/Ubicación',
                i.stock AS 'Cant.', i.unit_of_measure AS 'Unidad', i.min_stock_alert AS 'Mínimo'
            FROM inputs i
            WHERE i.is_active = TRUE
            """
            if txt_buscar_almacen:
                query_master_stock += f" AND (i.name_input LIKE '%{txt_buscar_almacen}%' OR i.brand LIKE '%{txt_buscar_almacen}%' OR i.internal_code LIKE '%{txt_buscar_almacen}%')"
                
            query_master_stock += " ORDER BY i.internal_code ASC;"
            df_stock = pd.read_sql(query_master_stock, conexion)
            conexion.close()
            
            # Si el usuario buscó algo específico, le dibujamos tarjetas estéticas en pantalla
            if txt_buscar_almacen and not df_stock.empty:
                st.markdown("### 📍 Coincidencias de Ubicación en el Taller:")
                for idx, fila in df_stock.iterrows():
                    with st.chat_message("assistant", avatar="📦"):
                        st.markdown(
                            f"**📌 ARTÍCULO:** `{fila['Código']}` - **{fila['Descripción']}** ({fila['Marca']} {fila['Modelo/REF']})  \n"
                            f"**🗺️ LOCALIZACIÓN FÍSICA:** En **{fila['Mueble/Estante']}** ──► En el **{fila['Cajón/Ubicación']}**  \n"
                            f"**📊 DISPONIBILIDAD:** `{fila['Cant.']} {fila['Unidad']}` en almacén."
                        )
                st.write("---")
                
            st.markdown("#### 📋 Inventario General Completo")
            st.dataframe(df_stock, use_container_width=True)
            
            criticos = df_stock[df_stock['Cant.'] <= df_stock['Mínimo']]
            if not criticos.empty:
                st.error(f"🚨 **Alerta Crítica de Almacén:** ¡Hay {len(criticos)} artículos en nivel de reposición obligatoria!")
        except Exception as e: st.error(f"❌ Error: {e}")
            
    # -------------------------------------------------------------------------
    # PESTAÑA 2: EGRESO RÁPIDO DIGITAL POR CÓDIGO (SIN SCROLL INFINITO)
    # -------------------------------------------------------------------------
    with pestana_egreso:
        st.subheader("📉 Egreso Directo de Almacén (UCI / Guardia / Emergencias)")
        st.caption("Digita el código del insumo que retiraste físicamente del estante para registrar la salida sin orden.")
        
        codigo_eg_directo = st.text_input("🔑 Ingresa el Código Interno del Artículo a despachar:", placeholder="Ej: 6690...").strip()
        
        if codigo_eg_directo:
            try:
                conexion = conectar_base_datos()
                cursor_eg = conexion.cursor(dictionary=True)
                cursor_eg.execute("SELECT id_inputs, name_input, stock, unit_of_measure FROM inputs WHERE internal_code = %s AND is_active = TRUE;", (codigo_eg_directo,))
                item_eg = cursor_eg.fetchone()
                cursor_eg.close()
                conexion.close()
                
                if item_eg:
                    st.success(f"✅ **Artículo Identificado:** {item_eg['name_input']} (Disponibles: {item_eg['stock']} {item_eg['unit_of_measure']})")
                    
                    c_eg1, c_eg2 = st.columns(2)
                    with c_eg1: cant_egreso = st.number_input("🔢 Cantidad a Retirar:", min_value=1, max_value=item_eg['stock'] if item_eg['stock'] > 0 else 1, step=1)
                    with c_eg2: servicio_destino = st.selectbox("📍 Servicio Destino:", ["UCI", "Neonatología", "Guardia", "Quirófano", "Piso Internación"])
                    
                    c_eg3, c_eg4 = st.columns(2)
                    with c_eg3: solicita = st.text_input("👤 Solicitado por:").strip()
                    with c_eg4: entrega = st.text_input("👤 Entregado por (Tú):").strip()
                    
                    notas_egreso = st.text_input("📝 Observaciones:")
                    
                    if st.button("📉 Confirmar Despacho Directo", use_container_width=True):
                        if solicita and entrega:
                            conexion = conectar_base_datos()
                            mensajero = conexion.cursor()
                            mensajero.execute("UPDATE inputs SET stock = stock - %s WHERE id_inputs = %s;", (cant_egreso, item_eg['id_inputs']))
                            
                            query_mov_directo = """
                            INSERT INTO stock_movements (id_inputs, id_work_order, movement_type, quantity, destination_service, requested_by, dispatched_by, notes)
                            VALUES (%s, NULL, 'salida_directa', %s, %s, %s, %s, %s);
                            """
                            mensajero.execute(query_mov_directo, (item_eg['id_inputs'], cant_egreso, servicio_destino, solicita, entrega, notas_egreso))
                            conexion.commit()
                            mensajero.close()
                            conexion.close()
                            st.success(f"✅ Despacho exitoso y auditado en la bitácora Kardex.")
                            st.balloons()
                            st.rerun()
                        else: st.warning("⚠️ Los campos de personal son obligatorios.")
                else:
                    st.error("❌ El código ingresado no coincide con ningún artículo en stock.")
            except Exception as e: st.error(f"❌ Error: {e}")

    # -------------------------------------------------------------------------
    # PESTAÑA 3: LA BITÁCORA KARDEX EN VIVO
    # -------------------------------------------------------------------------
    with pestana_kardex:
        st.subheader("📜 Libro de Actas e Historial Logístico (Kardex)")
        try:
            conexion = conectar_base_datos()
            query_kardex = """
            SELECT 
                sm.id_movement AS 'N° Ref', i.internal_code AS 'Código Insumo', i.name_input AS 'Descripción',
                sm.movement_type AS 'Tipo Movimiento', sm.quantity AS 'Cantidad', sm.destination_service AS 'Destino/Servicio',
                sm.requested_by AS 'Solicitante', sm.dispatched_by AS 'Despachante', sm.movement_date AS 'Fecha/Hora', sm.notes AS 'Observaciones'
            FROM stock_movements sm
            JOIN inputs i ON sm.id_inputs = i.id_inputs
            ORDER BY sm.movement_date DESC;
            """
            df_kardex = pd.read_sql(query_kardex, conexion)
            conexion.close()
            st.dataframe(df_kardex, use_container_width=True)
        except Exception as e: st.error(f"❌ Error al leer la bitácora: {e}")
