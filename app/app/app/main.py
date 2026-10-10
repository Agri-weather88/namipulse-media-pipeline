from fastapi import FastAPI

from app.database import initialize_database, get_connection
from app.collector import collect_all

app = FastAPI(
    title="Namipulse Media Monitoring API",
    version="1.0.0"
)

initialize_database()


@app.get("/")
def home():
    return {
        "system": "Namipulse Media Monitoring",
        "status": "online"
    }


@app.get("/api/articles")
def get_articles():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM articles
        ORDER BY published_at DESC
        """
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


@app.get("/api/articles/latest")
def latest_articles():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM articles
        ORDER BY published_at DESC
        LIMIT 50
        """
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


@app.post("/api/collect")
def collect_news():
    results = collect_all()

    return {
        "status": "completed",
        "results": results
    }
