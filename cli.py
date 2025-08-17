from contextlib import contextmanager
from tabulate import tabulate
from .db import SessionLocal
from . import crud

@contextmanager
def session_scope():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def menu():
    print("\n=== Biblioteca Personal (MariaDB + SQLAlchemy) ===")
    print("1. Agregar nuevo libro")
    print("2. Actualizar información de un libro")
    print("3. Eliminar libro existente")
    print("4. Ver listado de libros")
    print("5. Buscar libros")
    print("6. Salir")


def agregar():
    titulo = input("Título: ")
    autor = input("Autor: ")
    genero = input("Género: ")
    estado = input("Estado de lectura [pendiente/en progreso/terminado]: ") or "pendiente"
    with session_scope() as db:
        libro = crud.agregar_libro(db, titulo, autor, genero, estado)
        print(f"✔ Libro agregado (id={libro.id})")


def actualizar():
    try:
        libro_id = int(input("ID del libro a actualizar: "))
    except ValueError:
        print("ID inválido")
        return
    print("Deja vacío cualquier campo que no quieras cambiar.")
    titulo = input("Nuevo título: ") or None
    autor = input("Nuevo autor: ") or None
    genero = input("Nuevo género: ") or None
    estado = input("Nuevo estado: ") or None
    with session_scope() as db:
        libro = crud.actualizar_libro(db, libro_id, titulo=titulo, autor=autor, genero=genero, estado=estado)
        if libro:
            print("✔ Libro actualizado")
        else:
            print("✖ No se encontró el libro")


def eliminar():
    try:
        libro_id = int(input("ID del libro a eliminar: "))
    except ValueError:
        print("ID inválido")
        return
    with session_scope() as db:
        if crud.eliminar_libro(db, libro_id):
            print("✔ Libro eliminado")
        else:
            print("✖ No se encontró el libro")


def listar():
    with session_scope() as db:
        libros = crud.listar_libros(db)
        if not libros:
            print("(sin registros)")
            return
        rows = [[l.id, l.titulo, l.autor, l.genero, l.estado] for l in libros]
        print(tabulate(rows, headers=["ID", "Título", "Autor", "Género", "Estado"], tablefmt="github"))


def buscar():
    titulo = input("Buscar por título (parcial): ") or None
    autor = input("Buscar por autor (parcial): ") or None
    genero = input("Buscar por género (parcial): ") or None
    with session_scope() as db:
        libros = crud.buscar_libros(db, titulo=titulo, autor=autor, genero=genero)
        if not libros:
            print("(sin coincidencias)")
            return
        rows = [[l.id, l.titulo, l.autor, l.genero, l.estado] for l in libros]
        print(tabulate(rows, headers=["ID", "Título", "Autor", "Género", "Estado"], tablefmt="github"))


def run_cli():
    while True:
        menu()
        op = input("Elige una opción: ").strip()
        if op == "1":
            agregar()
        elif op == "2":
            actualizar()
        elif op == "3":
            eliminar()
        elif op == "4":
            listar()
        elif op == "5":
            buscar()
        elif op == "6":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida")
