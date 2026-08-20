# CÓDIGO DEFECTUOSO ENTREGADO POR LA EMPRESA
import psycopg2 #conectar a la base de datos
import logging #para los logs
import os #secretos
import json

# 1. Configurar logging industrial
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def guardar_datos(id_sensor: str, temperatura: float) -> None:
    
    try:
        # Conexión básica
        conexion = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conexion.cursor()
        
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS lecturas (
                    id SERIAL PRIMARY KEY,
                    sensor_id VARCHAR(50) NOT NULL,
                    grados REAL NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

        # SOLUCIÓN 2: Consulta parametrizada con marcadores %s (segura contra inyecciones)
        query = "INSERT INTO lecturas (sensor_id, grados) VALUES (%s, %s);"
        parametros = (id_sensor, temperatura)
            
        cursor.execute(query, parametros)
        conexion.commit()

        # SOLUCIÓN 3: Logging formal en lugar de print()
        logger.info(f"Dato guardado correctamente: Sensor={id_sensor}, Temp={temperatura}°C")

        cursor.close()
        conexion.close()
    except psycopg2.Error as e:
        logger.error(f"Error de base de datos PostgreSQL: {e}")
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        
if __name__ == "__main__":
    try:
        with open("datos.json", "r") as archivo:
            lista_lecturas = json.load(archivo)
            
        for lectura in lista_lecturas:
            guardar_datos(lectura["id_sensor"], lectura["temperatura"])
            
    except FileNotFoundError:
        logger.error("No se encontró el archivo datos.json")
    