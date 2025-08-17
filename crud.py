from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DataError, OperationalError
from typing import List, Optional
from .models import Libro

# Crear tablas si no existen
from .models import Base
from .db import engine
Base.metadata.create_all(bind=engine)


def agregar_libro(db: Session, titulo: str, autor: str, genero: str, estado: str = "pendiente") -> Libro:
    try:
        libro = Libro(titulo=titulo.strip(), autor=autor.strip(), genero=genero.strip(), estado=estado.strip())
        db.add(libro)
        db.commit()
        db.refresh(libro)
        return libro
    except (IntegrityError, DataError) as e:
        db.rollback()
        raise ValueError(f"Datos inválidos o violación de integridad: {e}")
    except OperationalError as e:
        db.rollback()
        raise ConnectionError(f"Error de conexión a la BD: {e}")


def actualizar_libro(db: Session, libro_id: int, **campos) -> Optional[Libro]:
    libro = db.get(Libro, libro_id)
    if not libro:
        return None
    try:
        for k, v in campos.items():
            if hasattr(libro, k) and v is not None:
                setattr(libro, k, v.strip() if isinstance(v, str) else v)
        db.commit()
        db.refresh(libro)
        return libro
    except (IntegrityError, DataError) as e:
        db.rollback()
        raise ValueError(f"Actualización inválida: {e}")
    except OperationalError as e:
        db.rollback()
        raise ConnectionError(f"Error de conexión a la BD: {e}")


def eliminar_libro(db: Session, libro_id: int) -> bool:
    libro = db.get(Libro, libro_id)
    if not libro:
        return False
    try:
        db.delete(libro)
        db.commit()
        return True
    except OperationalError as e:
        db.rollback()
        raise ConnectionError(f"Error de conexión a la BD: {e}")


def listar_libros(db: Session) -> List[Libro]:
    return db.query(Libro).order_by(Libro.id.desc()).all()


def buscar_libros(db: Session, titulo: str = None, autor: str = None, genero: str = None) -> List[Libro]:
    q = db.query(Libro)
    if titulo:
        q = q.filter(Libro.titulo.ilike(f"%{titulo}%"))
    if autor:
        q = q.filter(Libro.autor.ilike(f"%{autor}%"))
    if genero:
        q = q.filter(Libro.genero.ilike(f"%{genero}%"))
    return q.order_by(Libro.id.desc()).all()
