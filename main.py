from app.db import test_connection
from app.cli import run_cli

if __name__ == "__main__":
    print("Probando conexión a la base de datos...")
    if not test_connection():
        print("No se puede continuar sin conexión. Revisa tu .env y que MariaDB esté activo.")
    else:
        run_cli()
