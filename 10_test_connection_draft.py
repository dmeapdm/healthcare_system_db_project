import mysql.connector

# 1. ABRIR LA PUERTA (Conexión)
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="...", # <-- COLOCA AQUÍ TU CONTRASEÑA DE WORKBENCH
    database="healthcare_system_db"
)

# 2. EL MENSAJERO (Cursor)
mensajero = conexion.cursor()

# 3. EJECUTAR LA ORDEN
# Coloca adentro de las triples comillas tu consulta de antigüedad de los equipos:
consulta_sql = """
SELECT 
    id_equipment AS 'ID',
    brand AS 'Marca',
    model AS 'Modelo',
    year_manufactured AS 'Año Fab',
    ( YEAR(CURDATE()) - ... ) AS 'Años de Antigüedad'
FROM ...;
"""

mensajero.execute(consulta_sql)

# El mensajero trae los datos y los imprimimos fila por fila
resultados = mensajero.fetchall()
for fila in resultados:
    print(fila)

# 4. CERRAR LA PUERTA (Por seguridad y memoria)
mensajero.close()
conexion.close()
