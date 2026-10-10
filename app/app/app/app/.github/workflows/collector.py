import hashlib
from datetime import datetime, timezone

import feedparser

from app.database import get_connection


RSS_FEEDS = {
    "BBC": "https://feeds.bbci.co.uk/news/rss.xml",
}


def create_hash(title, url):
    value = f"{title.strip().lower()}|{url.strip().lower()}"
    return hashlib.sha256(value.encode()).hexdigest()


def collect_feed(source, feed_url):
    feed = feedparser.parse(feed_url)

    found = 0
    inserted = 0
    duplicates = 0

    connection = get_connection()

    for entry in feed.entries:
        found += 1

        title = entry.get("title", "").strip()
        description = entry.get("summary", "").strip()
        url = entry.get("link", "").strip()

        if not title or not url:
            continue

        content_hash = create_hash(title, url)

        published_at = entry.get(
            "published",
            datetime.now(timezone.utc).isoformat()
        )

        try:
            connection.execute(
                """
                INSERT INTO articles (
                    title,
                    description,
                    url,
                    source,
                    country,
                    published_at,
                    collected_at,
                    content_hash
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    title,
                    description,
                    url,
                    source,
                    "International",
                    published_at,
                    datetime.now(timezone.utc).isoformat(),
                    content_hash,
                ),
            )

            inserted += 1

        except Exception:
            duplicates += 1

    connection.commit()
    connection.close()

    return {
        "source": source,
        "found": found,
        "inserted": inserted,
        "duplicates": duplicates,
    }


def collect_all():
    results = []

    for source, feed_url in RSS_FEEDS.items():
        results.append(
            collect_feed(source, feed_url)
        )

    return results
