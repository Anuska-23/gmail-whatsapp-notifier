import sqlite3
import os
from . import config
from contextlib import contextmanager

os.makedirs(os.path.dirname(config.DB_PATH), exist_ok=True)

def _connect():
    con = sqlite3.connect(config.DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = _connect()
    cur = con.cursor()
    cur.executescript(
        '''
        CREATE TABLE IF NOT EXISTS processed (
            uid INTEGER PRIMARY KEY
        );
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            from_addr TEXT,
            subject TEXT,
            snippet TEXT,
            wa_status TEXT
        );
        '''
    )
    con.commit()
    con.close()

@contextmanager
def get_db():
    con = _connect()
    try:
        yield con
    finally:
        con.close()

def is_processed(uid: int) -> bool:
    with get_db() as con:
        cur = con.execute("SELECT 1 FROM processed WHERE uid = ?", (uid,))
        return cur.fetchone() is not None

def mark_processed(uid: int):
    with get_db() as con:
        con.execute("INSERT OR IGNORE INTO processed(uid) VALUES(?)", (uid,))
        con.commit()

def add_log(ts, from_addr, subject, snippet, wa_status):
    with get_db() as con:
        con.execute(
            "INSERT INTO logs(ts, from_addr, subject, snippet, wa_status) VALUES(?,?,?,?,?)",
            (ts, from_addr, subject, snippet, wa_status),
        )
        con.commit()

def latest_logs(limit=50):
    with get_db() as con:
        cur = con.execute(
            "SELECT id, ts, from_addr, subject, snippet, wa_status FROM logs ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        return [dict(r) for r in cur.fetchall()]