from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer

class Base(DeclarativeBase):
    pass

class Libro(Base):
    __tablename__ = "libros"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    autor: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    genero: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    estado: Mapped[str] = mapped_column(String(40), nullable=False, default="pendiente", index=True)

    def __repr__(self) -> str:
        return f"<Libro id={self.id} titulo='{self.titulo}' autor='{self.autor}'>"
