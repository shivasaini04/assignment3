from typing import List, Optional
from app.models.user import User
from app.config.database import get_db_connection, get_db_cursor

class UserRepository:
    @staticmethod
    def create_user(user: User) -> int:
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (user.name, user.email, user.hash_password())
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all_users() -> List[dict]:
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute("SELECT id, name, email FROM users")
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[dict]:
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def update_user(user_id: int, name: str, email: str) -> bool:
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                "UPDATE users SET name = ?, email = ? WHERE id = ?",
                (name, email, user_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete_user(user_id: int) -> bool:
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def search_users_by_name(name: str) -> List[dict]:
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                "SELECT id, name, email FROM users WHERE name LIKE ?",
                (f"%{name}%",)
            )
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_user_by_credentials(email: str, password: str) -> Optional[dict]:
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute("SELECT id, name, email, password FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            
            if user and User.verify_password(user['password'], password):
                return {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email']
                }
            return None
