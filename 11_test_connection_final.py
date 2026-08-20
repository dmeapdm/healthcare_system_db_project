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
    ( YEAR(CURDATE()) - year_manufactured ) AS 'Años de Antigüedad'
FROM equipment;
"""

mensajero.execute(consulta_sql)

# El mensajero trae los datos y los imprimimos fila por fila
resultados = mensajero.fetchall()
for fila in resultados:
    print(fila)

# 4. CERRAR LA PUERTA (Por seguridad y memoria)
mensajero.close()
conexion.close()
