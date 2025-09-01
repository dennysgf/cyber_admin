from utils.db import get_connection
import bcrypt

def create_user(username, password, rol="usuario"):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        cur.execute(
            "INSERT INTO usuarios (username, password, rol) VALUES (%s, %s, %s) RETURNING id",
            (username, hashed, rol)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        return False

def get_promotions():
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, precio, horas FROM promociones")
        promos = cur.fetchall()
        cur.close()
        conn.close()
        return [{"id": p[0], "price": float(p[1]), "hours": p[2]} for p in promos]
    except Exception as e:
        print(f"Error al obtener promociones: {e}")
        return []

def create_promotion(precio, horas):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO promociones (precio, horas) VALUES (%s, %s) RETURNING id",
            (precio, horas)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al crear promoción: {e}")
        return False

def init_caja():
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM caja")
        count = cur.fetchone()[0]
        if count == 0:
            cur.execute("INSERT INTO caja (monto_actual) VALUES (0)")
            conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error en init_caja: {e}")
        return False

def get_caja():
    conn = get_connection()
    if not conn:
        return 0
    try:
        cur = conn.cursor()
        cur.execute("SELECT monto_actual FROM caja ORDER BY id LIMIT 1")
        monto = cur.fetchone()[0]
        cur.close()
        conn.close()
        return float(monto)
    except Exception as e:
        print(f"Error en get_caja: {e}")
        return 0

def update_caja(monto):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("UPDATE caja SET monto_actual = monto_actual + %s WHERE id = 1", (monto,))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error en update_caja: {e}")
        return False
def get_users():
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, username, tiempo_restante, rol FROM usuarios")
        users = cur.fetchall()
        cur.close()
        conn.close()
        return [{"id": u[0], "username": u[1], "tiempo": u[2], "rol": u[3]} for u in users]
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []

def add_time_to_user(user_id, hours):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE usuarios SET tiempo_restante = tiempo_restante + %s WHERE id = %s",
            (hours, user_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al actualizar tiempo usuario: {e}")
        return False


def insert_recarga(user_id, promo_id, monto):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO recargas (usuario_id, promo_id, monto) VALUES (%s, %s, %s)",
            (user_id, promo_id, monto)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al insertar recarga: {e}")
        return False

def get_recargas():
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT u.username, p.horas, r.monto, r.fecha
            FROM recargas r
            JOIN usuarios u ON r.usuario_id = u.id
            JOIN promociones p ON r.promo_id = p.id
            ORDER BY r.fecha DESC
        """)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return [{"usuario": d[0], "promo": f"{d[1]} horas", "monto": float(d[2]), "fecha": d[3]} for d in data]
    except Exception as e:
        print(f"Error al obtener recargas: {e}")
        return []

def logout_user(user_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE usuarios SET tiempo_restante = 0 WHERE id = %s",
            (user_id,)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al cerrar sesión del usuario: {e}")
        return False
