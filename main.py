import psycopg2
from psycopg2 import errors

BASE_DE_DATOS = {
    "host": "localhost",
    "database": "tarea1",
    "user": "postgres",
    "password": "admin",
    "port": "5432"
}

def conectar():
    try:
        conexion = psycopg2.connect(**BASE_DE_DATOS)
        return conexion
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:")
        print(e)
        return None

def crear_tabla():
    conexion = conectar()
    if conexion is None: return
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alumno (
                id SERIAL PRIMARY KEY,
                carnet VARCHAR(15) UNIQUE NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                carrera VARCHAR(150),
                email VARCHAR(150),
                telefono VARCHAR(20),
                fecha_registro DATE DEFAULT CURRENT_DATE
            );
        """)
        conexion.commit()
        cursor.close()
        conexion.close()
    except psycopg2.Error as e:
        print("Error al crear la tabla:")
        print(e)

def agregar():
    print("\nAGREGAR")
    carnet = input("Carnet: ").strip()
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    carrera = input("Carrera: ").strip()
    email = input("Email: ").strip()
    telefono = input("Teléfono: ").strip()

    if carnet == "" or nombre == "" or apellido == "":
        print("Carnet, nombre y apellido son obligatorios")
        return
    conexion = conectar()
    if conexion is None: return
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO alumno 
            (carnet, nombre, apellido, carrera, email, telefono)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (carnet, nombre, apellido, carrera, email, telefono))
        conexion.commit()
        cursor.close()
        conexion.close()
        print("ALUMNO AGREGADO")

    except errors.UniqueViolation:
        conexion.rollback()
        print("Error ya existe un alumno con ese carnet")
        conexion.close()

    except psycopg2.Error as e:
        conexion.rollback()
        print("Error al agregar alumno:")
        print(e)
        conexion.close()

def modificar():
    print("\nMODIFICAR")
    carnet = input("Ingrese el carnet: ").strip()
    conexion = conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, carnet, nombre, apellido, carrera, email, telefono
            FROM alumno
            WHERE carnet = %s;
        """, (carnet,))
        alumno = cursor.fetchone()
        if alumno is None:
            print("No se encontró dato.")
            cursor.close()
            conexion.close()
            return

        print("\nAlumno encontrado:")
        print(f"Carnet: {alumno[1]}")
        print(f"Nombre actual: {alumno[2]}")
        print(f"Apellido actual: {alumno[3]}")
        print(f"Carrera actual: {alumno[4]}")
        print(f"Email actual: {alumno[5]}")
        print(f"Teléfono actual: {alumno[6]}")
        print("\nDejar vacío si no se va a cambiar")

        nuevo_nombre = input("Nuevo nombre: ").strip()
        nuevo_apellido = input("Nuevo apellido: ").strip()
        nueva_carrera = input("Nueva carrera: ").strip()
        nuevo_email = input("Nuevo email: ").strip()
        nuevo_telefono = input("Nuevo teléfono: ").strip()

        nombre = nuevo_nombre if nuevo_nombre else alumno[2]
        apellido = nuevo_apellido if nuevo_apellido else alumno[3]
        carrera = nueva_carrera if nueva_carrera else alumno[4]
        email = nuevo_email if nuevo_email else alumno[5]
        telefono = nuevo_telefono if nuevo_telefono else alumno[6]

        cursor.execute("""
            UPDATE alumno
            SET nombre = %s,
                apellido = %s,
                carrera = %s,
                email = %s,
                telefono = %s
            WHERE carnet = %s;
        """, (nombre, apellido, carrera, email, telefono, carnet))

        conexion.commit()
        cursor.close()
        conexion.close()
        print("ALUMNO MODIFICADO")

    except psycopg2.Error as e:
        conexion.rollback()
        print("Error al modificar alumno:")
        print(e)
        conexion.close()

def listar():
    print("\nLISTADO")
    conexion = conectar()
    if conexion is None: return
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, carnet, nombre, apellido, carrera, email, telefono, fecha_registro
            FROM alumno
            ORDER BY id;
        """)
        alumnos = cursor.fetchall()
        if len(alumnos) == 0:
            print("\nNo hay alumnos registrados.")
        else:
            for alumno in alumnos:
                print(
                    f"\nID: {alumno[0]}\n"
                    f"Carnet: {alumno[1]}\n"
                    f"Nombre: {alumno[2]}\n"
                    f"Apellido: {alumno[3]}\n"
                    f"Carrera: {alumno[4]}\n"
                    f"Email: {alumno[5]}\n"
                    f"Teléfono: {alumno[6]}\n"
                    f"Fecha registro: {alumno[7]}\n"
                    f"--------------------------------------------------"
                )
        cursor.close()
        conexion.close()

    except psycopg2.Error as e:
        print("Error al listar alumnos:")
        print(e)
        conexion.close()

def eliminar():
    print("\nELIMINAR")
    carnet = input("Ingrese el carnet: ").strip()
    conexion = conectar()
    if conexion is None: return
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT carnet, nombre, apellido
            FROM alumno
            WHERE carnet = %s;
        """, (carnet,))
        alumno = cursor.fetchone()
        if alumno is None:
            print("No se encontró dato.")
            cursor.close()
            conexion.close()
            return

        print(f"Alumno encontrado: {alumno[1]} {alumno[2]} - Carnet: {alumno[0]}")
        confirmar = input("¿Seguro que deseas eliminarlo? (s/n): ").lower().strip()

        if confirmar == "s":
            cursor.execute("""
                DELETE FROM alumno
                WHERE carnet = %s;
            """, (carnet,))
            conexion.commit()
            print("Alumno eliminado")
        else:
            print("Cancelado")
        cursor.close()
        conexion.close()

    except psycopg2.Error as e:
        conexion.rollback()
        print("Error:")
        print(e)
        conexion.close()

def menu():
    while True:
        print("\nMENÚ")
        print("------------------------------------")
        print("1. Agregar alumno")
        print("2. Modificar datos de un alumno")
        print("3. Listar todos los alumnos")
        print("4. Eliminar alumno")
        print("5. Salir")
        print("------------------------------------")

        opcion = input("Escriba el número de la opción: ").strip()
        if opcion == "1": agregar()
        elif opcion == "2": modificar()
        elif opcion == "3": listar()
        elif opcion == "4": eliminar()
        elif opcion == "5":
            print("Saliendo ")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    crear_tabla()
    menu()
