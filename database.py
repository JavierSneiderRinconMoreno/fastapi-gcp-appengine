import os
import psycopg2
from dotenv import load_dotenv

# Cargar variables desde .env (solo en local)
load_dotenv()

def get_db_connection():
    """Crea una conexión a PostgreSQL, detectando si está en local o GCP."""

    environment = os.getenv("ENVIRONMENT", "local")

    print(f"🌍 [database.py] Entorno actual: {environment}")

    # Datos comunes
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    if environment == "gcp":
        # --- MODO CLOUD SQL (App Engine) ---
        db_socket_dir = os.getenv("DB_SOCKET_DIR")
        cloud_sql_connection = f"{db_socket_dir}"

        print("☁️ [database.py] Conectando a Cloud SQL mediante Unix socket...")
        print(f"   → Socket: {cloud_sql_connection}")
        print(f"   → Base de datos: {db_name}")
        print(f"   → Usuario: {db_user}")

        connection = psycopg2.connect(
            user=db_user,
            password=db_pass,
            dbname=db_name,
            host=cloud_sql_connection
        )

    else:
        # --- MODO LOCAL ---
        db_host = os.getenv("DB_HOST", "127.0.0.1")
        db_port = os.getenv("DB_PORT", "5432")

        print("💻 [database.py] Conectando a PostgreSQL local...")
        print(f"   → Host: {db_host}")
        print(f"   → Puerto: {db_port}")
        print(f"   → Base de datos: {db_name}")
        print(f"   → Usuario: {db_user}")
        print(f"   → Contraseña: {db_pass[:2]}*** (oculta por seguridad)")

        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_pass,
            database=db_name
        )

    print("✅ [database.py] Conexión establecida correctamente.\n")
    return connection



'''   USO DE SOLO FORMA LOCAL 
import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor


load_dotenv()
# Configuración de Cloud SQL
# DB_HOST = os.getenv("DB_HOST", "")
# DB_NAME = os.getenv("DB_NAME", "")
# DB_USER = os.getenv("DB_USER", "")
# DB_PASSWORD = os.getenv("DB_PASSWORD", "")

def get_db_connection():
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    try:
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=5432
        )
        print("✅ [database.py] Conexión creada correctamente.\n")
        return connection
    except Exception as e:
        print("❌ [database.py] Error al conectar con la base de datos:")
        print(f"   → Tipo: {type(e).__name__}")
        print(f"   → Mensaje: {e}\n")
        raise

        '''   
