from utils.db import get_connection

def test_db():
    conn = get_connection()
    if conn:
        print("✅ Conexión exitosa a la base de datos")
        cur = conn.cursor()
        cur.execute("SELECT NOW()")
        result = cur.fetchone()
        print("🕒 Hora del servidor:", result[0])
        cur.close()
        conn.close()
    else:
        print("❌ No se pudo conectar a la base de datos")

if __name__ == "__main__":
    test_db()
