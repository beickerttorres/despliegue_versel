import os
from decouple import config
import psycopg2

def main():
    db_name = config('DB_NAME', default='')
    db_user = config('DB_USER', default='')
    db_password = config('DB_PASSWORD', default='')
    db_host = config('DB_HOST', default='')
    db_port = config('DB_PORT', default='5432')

    print(f"Intentando conectar a Postgres en {db_host}:{db_port} como {db_user} a la BD {db_name}...")
    try:
        conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        conn.close()
        print('Conexión exitosa ✅')
    except Exception as e:
        print('Error al conectar a la base de datos:')
        print(e)

if __name__ == '__main__':
    main()
