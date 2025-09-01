import psycopg2

def get_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            port="5432",
            database="cyber_control",
            user="postgres",
            password="root"
        )
        return connection
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None
