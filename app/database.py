import sqlite3
from pathlib import Path

DB_PATH = Path("data/media_monitor.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            content TEXT,
            url TEXT UNIQUE,
            source TEXT,
            country TEXT,
            author TEXT,
            published_at TEXT,
            category TEXT,
            image_url TEXT,
            language TEXT,
            collected_at TEXT,
            content_hash TEXT UNIQUE
        )
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_articles_source
        ON articles(source)
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_articles_published
        ON articles(published_at)
    """)

    connection.commit()
    connection.close()
