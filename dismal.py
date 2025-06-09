import json
from datetime import datetime

import feedparser

SOURCES_FILE = "sources.txt"
OUTPUT_FILE = "data.json"
MAX_ITEMS = 5


def load_sources(path=SOURCES_FILE):
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]


def fetch_feed(url):
    feed = feedparser.parse(url)
    entries = []
    for entry in feed.entries[:MAX_ITEMS]:
        entries.append({
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", "")
        })
    return {
        "source": feed.feed.get("title", url),
        "url": url,
        "entries": entries
    }


def main():
    sources = load_sources()
    aggregated = []
    for url in sources:
        try:
            aggregated.append(fetch_feed(url))
        except Exception as exc:
            aggregated.append({"source": url, "error": str(exc), "entries": []})
    with open(OUTPUT_FILE, "w") as f:
        json.dump({"generated": datetime.utcnow().isoformat() + "Z", "feeds": aggregated}, f, indent=2)


if __name__ == "__main__":
    main()
