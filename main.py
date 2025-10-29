from fastapi import FastAPI, HTTPException, Request
from database import get_db_connection
from dotenv import load_dotenv
import os
import psycopg2
from pydantic import BaseModel

# Cargar variables del entorno (.env)
load_dotenv()

app = FastAPI(title="FastAPI + PostgreSQL Local", version="1.1")

class Student(BaseModel):
    name: str
    age: int


# -------------------------------
# Endpoints
# -------------------------------

@app.get("/")
def read_root():
    mensaje = os.getenv("HOLA_MUNDO")
    print(f"✅ [GET /] Mensaje desde .env: {mensaje}")
    return {"Hello": mensaje}


@app.get("/students")
def read_students():
    print("📥 [GET /students] Solicitando lista de estudiantes...")
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()

        print(f"✅ [GET /students] Se obtuvieron {len(students)} registros.")
        for s in students:
            print(f"   → ID: {s[0]}, Nombre: {s[1]}, Edad: {s[2]}")

        cursor.close()
        db.close()
        return {"students": students}
    except psycopg2.Error as e:
        print("❌ [GET /students] Error al consultar la base de datos:", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/students")
async def add_student(student: Student):
    print("📤 [POST /students] Recibiendo datos...")

    try:
        print(f"🧩 [POST /students] Datos recibidos → Nombre: {student.name}, Edad: {student.age}")

        db = get_db_connection()
        print("✅ [POST /students] Conexión abierta correctamente.")
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO students (name, age) VALUES (%s, %s) RETURNING id;",
            (student.name, student.age)
        )
        student_id = cursor.fetchone()[0]
        db.commit()
        cursor.close()
        db.close()

        print(f"✅ [POST /students] Estudiante insertado con ID {student_id}")
        return {"id": student_id, "message": "Student added successfully"}

    except psycopg2.Error as e:
        print("❌ [POST /students] Error en base de datos:")
        print(f"   → Código: {e.pgcode}")
        print(f"   → Mensaje: {e.pgerror}\n")
        raise HTTPException(status_code=500, detail=str(e))

