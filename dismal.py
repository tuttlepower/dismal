import json
from datetime import datetime, timezone

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

    error = None
    if getattr(feed, "bozo", False):
        error = str(getattr(feed, "bozo_exception", ""))
    if hasattr(feed, "status") and feed.status != 200:
        status_err = f"status {feed.status}"
        error = f"{error}; {status_err}" if error else status_err

    return {
        "source": feed.feed.get("title", url),
        "url": url,
        "entries": entries,
        "error": error,
    }


def main():
    sources = load_sources()
    aggregated = []
    for url in sources:
        print(f"Fetching {url}")
        try:
            feed = fetch_feed(url)
            aggregated.append(feed)
            if feed.get("error"):
                print(f"  Error: {feed['error']}")
            else:
                print(f"  {len(feed['entries'])} entries")
        except Exception as exc:
            print(f"Failed to fetch {url}: {exc}")
            aggregated.append({"source": url, "url": url, "entries": [], "error": str(exc)})
    with open(OUTPUT_FILE, "w") as f:
        json.dump({"generated": datetime.now(timezone.utc).isoformat(), "feeds": aggregated}, f, indent=2)


if __name__ == "__main__":
    main()
