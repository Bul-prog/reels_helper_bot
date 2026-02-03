import sqlite3
from datetime import datetime, timedelta

# =====================
# CONNECTION
# =====================

conn = sqlite3.connect("db.sqlite", check_same_thread=False)
cursor = conn.cursor()

# =====================
# TABLES
# =====================

# --- USERS ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    is_subscribed INTEGER DEFAULT 0,
    subscription_until TEXT,
    daily_used INTEGER DEFAULT 0,
    last_reset TEXT
)
""")

# --- PAYMENTS ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    payment_id TEXT UNIQUE NOT NULL,
    provider TEXT NOT NULL,
    amount INTEGER NOT NULL,
    currency TEXT NOT NULL,
    status TEXT NOT NULL,
    plan TEXT NOT NULL,
    created_at TEXT NOT NULL,
    paid_at TEXT,
    raw_event TEXT
)
""")

conn.commit()


# =====================
# MIGRATIONS (SAFE)
# =====================

def ensure_column(table: str, column: str, definition: str):
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cursor.fetchall()]

    if column not in columns:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
        conn.commit()


# добавляем недостающие колонки в users
ensure_column("users", "plan", "TEXT DEFAULT 'free'")
ensure_column("users", "updated_at", "TEXT")


# =====================
# USERS
# =====================

def get_user(user_id: int):
    cursor.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    )
    return cursor.fetchone()


def create_user(user_id: int):
    cursor.execute(
        """
        INSERT OR IGNORE INTO users (user_id, last_reset)
        VALUES (?, ?)
        """,
        (user_id, datetime.utcnow().isoformat())
    )
    conn.commit()


def update_usage(user_id: int, daily_used: int):
    cursor.execute(
        "UPDATE users SET daily_used = ? WHERE user_id = ?",
        (daily_used, user_id)
    )
    conn.commit()


def reset_daily_usage(user_id: int, now_iso: str):
    cursor.execute(
        """
        UPDATE users
        SET daily_used = 0,
            last_reset = ?
        WHERE user_id = ?
        """,
        (now_iso, user_id)
    )
    conn.commit()


def activate_subscription(user_id: int, plan: str):
    until = (datetime.utcnow() + timedelta(days=30)).isoformat()

    cursor.execute(
        """
        UPDATE users
        SET is_subscribed = 1,
            subscription_until = ?,
            plan = ?,
            updated_at = ?
        WHERE user_id = ?
        """,
        (until, plan, datetime.utcnow().isoformat(), user_id)
    )
    conn.commit()


# =====================
# PAYMENTS
# =====================

def payment_exists(payment_id: str) -> bool:
    cursor.execute(
        "SELECT 1 FROM payments WHERE payment_id = ?",
        (payment_id,)
    )
    return cursor.fetchone() is not None


def save_payment(
        user_id: int,
        payment_id: str,
        amount: int,
        currency: str,
        plan: str,
        status: str,
        raw_event: str
):
    cursor.execute(
        """
        INSERT INTO payments
        (
            user_id,
            payment_id,
            provider,
            amount,
            currency,
            status,
            plan,
            created_at,
            paid_at,
            raw_event
        )
        VALUES (?, ?, 'yookassa', ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            payment_id,
            amount,
            currency,
            status,
            plan,
            datetime.utcnow().isoformat(),
            datetime.utcnow().isoformat(),
            raw_event
        )
    )
    conn.commit()


def get_or_create_user(user_id: int):
    user = get_user(user_id)
    if not user:
        create_user(user_id)
        user = get_user(user_id)
    return user
