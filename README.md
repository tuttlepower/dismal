# dismal

Dismal is a lightweight RSS aggregator focused on quantitative finance, trading and machine learning news. The Python script fetches a handful of entries from each feed listed in `sources.txt` and stores them in `data.json`. The static `index.html` page displays the collected items as simple cards.

## Usage
1. Install dependencies with `pip install -r requirements.txt`.
2. Run `python dismal.py` to generate `data.json`.
   The script prints progress as it fetches each feed. If a feed cannot be
   retrieved, an error message is stored in the JSON file.
3. Open `index.html` in a browser to view the latest items. Any per-feed
   errors will be displayed above the entries.

Network restrictions may prevent the script from downloading feeds. In that
case the JSON will contain error messages rather than entries.

## Feed Sources
A sample of the current feeds is listed below:

- NBER: <https://back.nber.org/rss/new.xml>
- arXiv Econ: <http://export.arxiv.org/rss/econ>
- arXiv CS: <http://export.arxiv.org/rss/cs>
- arXiv Quant Finance: <http://export.arxiv.org/rss/q-fin>
- Netflix Tech Blog: <https://netflixtechblog.com/feed>
- Lyft Engineering: <https://eng.lyft.com/feed>
- Spotify Engineering: <https://engineering.atspotify.com/rss>
- GitHub Blog: <https://github.blog/feed>
- HackerNews: <https://hnrss.org/frontpage>
- NPR: <https://feeds.npr.org/1019/rss.xml>
- Bloomberg Markets: <https://feeds.bloomberg.com/markets/news.rss>
- FRED Blog: <https://fredblog.stlouisfed.org/feed>
- JMLR: <https://www.jmlr.org/jmlr.xml>
- SEC Trading Suspensions: <https://www.sec.gov/rss/litigation/suspensions.xml>
- NASA News: <https://www.jpl.nasa.gov/feeds/news/>

Additional feeds can be added to `sources.txt` as needed.
