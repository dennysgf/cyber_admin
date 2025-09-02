from utils.db import get_connection
import bcrypt
from datetime import date


# ===== Usuarios =====
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


def add_time_to_user(user_id, seconds):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE usuarios SET tiempo_restante = tiempo_restante + %s WHERE id = %s",
            (seconds, user_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al actualizar tiempo usuario: {e}")
        return False


def remove_time(user_id: int, seconds: int):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE usuarios SET tiempo_restante = GREATEST(tiempo_restante - %s, 0) WHERE id = %s",
            (seconds, user_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error en remove_time: {e}")
        return False


def reset_password(user_id: int, new_password: str):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        cur.execute("UPDATE usuarios SET password = %s WHERE id = %s", (hashed, user_id))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error en reset_password: {e}")
        return False


def logout_user(user_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE usuarios SET is_active = FALSE, current_pc = NULL, hostname = NULL WHERE id = %s",
            (user_id,)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al cerrar sesión del usuario: {e}")
        return False


def set_session_state(user_id: int, active: bool, pc_number: int = None, hostname: str = None):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        if active:
            cur.execute(
                "UPDATE usuarios SET is_active = TRUE, current_pc = %s, hostname = %s WHERE id = %s",
                (pc_number, hostname, user_id)
            )
        else:
            cur.execute(
                "UPDATE usuarios SET is_active = FALSE, current_pc = NULL, hostname = NULL WHERE id = %s",
                (user_id,)
            )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error en set_session_state: {e}")
        return False


def get_active_sessions():
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT current_pc, username, tiempo_restante, id, hostname
            FROM usuarios
            WHERE is_active = TRUE AND current_pc IS NOT NULL
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [
            {
                "pc_number": int(r[0]),
                "username": r[1],
                "tiempo": int(r[2]),
                "user_id": int(r[3]),
                "hostname": r[4]
            }
            for r in rows
        ]
    except Exception as e:
        print(f"Error en get_active_sessions: {e}")
        return []


# ===== Promociones / Recargas =====
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


def insert_recarga(user_id, promo_id, monto):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO recargas (usuario_id, promo_id, monto, fecha) VALUES (%s, %s, %s, NOW())",
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


# ===== Caja diaria =====
def init_caja():
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        today = date.today()
        cur.execute("SELECT id FROM caja WHERE fecha = %s", (today,))
        if not cur.fetchone():
            cur.execute("INSERT INTO caja (fecha, monto) VALUES (%s, 0)", (today,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error en init_caja: {e}")


def add_to_caja(amount: float):
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        today = date.today()
        cur.execute("UPDATE caja SET monto = monto + %s WHERE fecha = %s", (amount, today))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error en add_to_caja: {e}")


def get_caja():
    conn = get_connection()
    if not conn:
        return 0
    try:
        cur = conn.cursor()
        today = date.today()
        cur.execute("SELECT monto FROM caja WHERE fecha = %s", (today,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return float(result[0]) if result else 0
    except Exception as e:
        print(f"Error en get_caja: {e}")
        return 0


def get_historial_cajas():
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT fecha, monto FROM caja ORDER BY fecha DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"Error en get_historial_cajas: {e}")
        return []
