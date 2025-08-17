
# Biblioteca personal — MariaDB + SQLAlchemy

Migración de una app CLI de biblioteca desde SQLite a **MariaDB** usando **SQLAlchemy (ORM)**.

## Requisitos
- Python 3.10+
- MariaDB 10.6+ (servidor local o remoto)

## Instalación de MariaDB

### Windows
1. Descarga el instalador de MariaDB Community desde la web oficial.
2. Durante la instalación, define una contraseña para `root` y habilita el servicio para que inicie automáticamente.

### macOS (Homebrew)
```bash
brew install mariadb
brew services start mariadb
```

### Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install mariadb-server mariadb-client -y
sudo systemctl enable mariadb
sudo systemctl start mariadb
```

### Asegurar la instalación (opcional pero recomendado)
```bash
sudo mysql_secure_installation
```

## Crear base de datos y usuario

Entra al cliente:
```bash
mariadb -u root -p
```
Y ejecuta (ajusta usuario/clave):
```sql
CREATE DATABASE biblioteca CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'bibliouser'@'%' IDENTIFIED BY 'cambia_esta_clave';
GRANT ALL PRIVILEGES ON biblioteca.* TO 'bibliouser'@'%';
FLUSH PRIVILEGES;
```

> **Nota:** Las tablas se crean automáticamente en el primer arranque por `SQLAlchemy`.

## Configuración

Crea un archivo `.env` en la raíz (basado en `.env.example`):

```env
DB_USER=bibliouser
DB_PASS=cambia_esta_clave
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=biblioteca
```

## Instalación de dependencias

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## Ejecutar la aplicación

```bash
python main.py
```

## Uso
- **1** Agregar nuevo libro
- **2** Actualizar información
- **3** Eliminar libro
- **4** Ver listado de libros
- **5** Buscar por título/autor/género
- **6** Salir

## Cadena de conexión

Este proyecto usa por defecto **PyMySQL**: `mysql+pymysql://usuario:pass@host:puerto/bd`

Si prefieres el conector oficial de MariaDB, instala `mariadb` y cambia en `app/db.py`:
```python
DB_URL = f"mariadb+mariadbconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
```

## Manejo de excepciones
- **OperationalError**: problemas de red/servicio/credenciales.
- **IntegrityError/DataError**: datos inválidos o violaciones de integridad.

La app muestra mensajes claros y hace `rollback()` cuando corresponde.

## Pruebas rápidas
- Verifica la conexión: al iniciar `main.py` se hace `SELECT 1`.
- Agrega un libro y luego consúltalo bajo **4. Ver listado**.

## Notas
- Para ver el SQL generado, activa `echo=True` en `create_engine` (ver `app/db.py`).
- Si usas Docker para MariaDB, expón el puerto 3306 y apunta `DB_HOST` al contenedor o `localhost` si haces port-forwarding.

## Licencia
MIT
