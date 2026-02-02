# Test Coverage Analysis

## Executive Summary

**Current Test Coverage: 0%**

This codebase has no automated tests. The project consists of a Python RSS aggregator (`dismal.py`) and a simple HTML/JavaScript frontend (`index.html`). While the codebase is small, adding tests would improve reliability and make future changes safer.

---

## Current Codebase Structure

| File | Language | Lines | Functions/Components | Test Coverage |
|------|----------|-------|---------------------|---------------|
| `dismal.py` | Python | 46 | 3 functions | 0% |
| `index.html` | HTML/JS | 42 | 1 script block | 0% |

---

## Detailed Analysis of Untested Code

### 1. `dismal.py` - Python Backend

#### Function: `load_sources(path)`
**Lines 11-13**

```python
def load_sources(path=SOURCES_FILE):
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]
```

**Untested scenarios:**
- Happy path: Loading a valid sources file
- Empty file handling
- File with blank lines (should be filtered)
- File with whitespace-only lines
- **Missing file (raises FileNotFoundError)**
- **Permission denied errors**
- File with invalid encoding

**Risk Assessment:** Medium - If this function fails, the entire aggregator stops.

---

#### Function: `fetch_feed(url)`
**Lines 16-29**

```python
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
```

**Untested scenarios:**
- Happy path: Valid RSS feed parsing
- Atom feed format (different structure)
- Feed with fewer than MAX_ITEMS entries
- Feed with exactly MAX_ITEMS entries
- Feed with more than MAX_ITEMS entries (truncation)
- **Empty feed (no entries)**
- **Malformed XML**
- **Network timeout**
- **HTTP 404 errors**
- **HTTP 500 errors**
- **DNS resolution failure**
- **SSL certificate errors**
- Feed with missing `title` field (fallback to URL)
- Feed with missing `link` field in entries
- Feed with missing `published` field in entries
- Unicode/special characters in titles
- Very long titles (potential display issues)

**Risk Assessment:** High - Network operations are inherently unreliable. This function handles 32 different external RSS feeds.

---

#### Function: `main()`
**Lines 32-45**

```python
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
```

**Untested scenarios:**
- Happy path: Full aggregation workflow
- **Exception handling in the try/except block**
- Error structure in output (when feeds fail)
- JSON output format validation
- `generated` timestamp format (ISO 8601 with Z suffix)
- **Output file write permission errors**
- **Disk full errors**
- Partial failure (some feeds succeed, some fail)
- All feeds fail
- Empty sources file (results in empty feeds array)

**Risk Assessment:** High - This is the main entry point; any issues here break the entire application.

---

### 2. `index.html` - Frontend

**Untested scenarios:**
- Happy path: Loading and rendering valid data.json
- **Network error fetching data.json**
- **Invalid JSON in data.json**
- **Missing data.json file**
- Empty feeds array rendering
- Feed with error field (graceful degradation)
- XSS vulnerability (entry.link or entry.title containing malicious HTML)
- Very long entry titles (layout issues)
- Special characters in feed data
- Mobile responsiveness

**Risk Assessment:** Medium - Frontend failures are visible to users but don't affect data collection.

---

## Recommended Test Improvements

### Priority 1: Core Python Tests (High Impact)

Create `tests/test_dismal.py`:

```python
import pytest
import json
from unittest.mock import patch, mock_open, MagicMock
from dismal import load_sources, fetch_feed, main

class TestLoadSources:
    """Tests for the load_sources function."""

    def test_load_sources_valid_file(self, tmp_path):
        """Should load URLs from a valid sources file."""
        sources_file = tmp_path / "sources.txt"
        sources_file.write_text("https://example.com/feed1\nhttps://example.com/feed2\n")

        result = load_sources(str(sources_file))

        assert result == ["https://example.com/feed1", "https://example.com/feed2"]

    def test_load_sources_filters_blank_lines(self, tmp_path):
        """Should filter out blank lines."""
        sources_file = tmp_path / "sources.txt"
        sources_file.write_text("https://example.com/feed1\n\n\nhttps://example.com/feed2\n")

        result = load_sources(str(sources_file))

        assert result == ["https://example.com/feed1", "https://example.com/feed2"]

    def test_load_sources_strips_whitespace(self, tmp_path):
        """Should strip leading/trailing whitespace from URLs."""
        sources_file = tmp_path / "sources.txt"
        sources_file.write_text("  https://example.com/feed1  \n")

        result = load_sources(str(sources_file))

        assert result == ["https://example.com/feed1"]

    def test_load_sources_missing_file(self):
        """Should raise FileNotFoundError for missing file."""
        with pytest.raises(FileNotFoundError):
            load_sources("/nonexistent/path/sources.txt")

    def test_load_sources_empty_file(self, tmp_path):
        """Should return empty list for empty file."""
        sources_file = tmp_path / "sources.txt"
        sources_file.write_text("")

        result = load_sources(str(sources_file))

        assert result == []


class TestFetchFeed:
    """Tests for the fetch_feed function."""

    @patch('dismal.feedparser.parse')
    def test_fetch_feed_valid_rss(self, mock_parse):
        """Should parse a valid RSS feed correctly."""
        mock_parse.return_value = MagicMock(
            feed={'title': 'Test Feed'},
            entries=[
                {'title': 'Entry 1', 'link': 'https://example.com/1', 'published': '2024-01-01'},
                {'title': 'Entry 2', 'link': 'https://example.com/2', 'published': '2024-01-02'},
            ]
        )

        result = fetch_feed('https://example.com/feed')

        assert result['source'] == 'Test Feed'
        assert result['url'] == 'https://example.com/feed'
        assert len(result['entries']) == 2
        assert result['entries'][0]['title'] == 'Entry 1'

    @patch('dismal.feedparser.parse')
    def test_fetch_feed_limits_entries(self, mock_parse):
        """Should limit entries to MAX_ITEMS (5)."""
        mock_parse.return_value = MagicMock(
            feed={'title': 'Test Feed'},
            entries=[{'title': f'Entry {i}', 'link': f'https://example.com/{i}', 'published': ''}
                     for i in range(10)]
        )

        result = fetch_feed('https://example.com/feed')

        assert len(result['entries']) == 5

    @patch('dismal.feedparser.parse')
    def test_fetch_feed_missing_title_uses_url(self, mock_parse):
        """Should use URL as source when feed title is missing."""
        mock_parse.return_value = MagicMock(
            feed={},  # No title
            entries=[]
        )

        result = fetch_feed('https://example.com/feed')

        assert result['source'] == 'https://example.com/feed'

    @patch('dismal.feedparser.parse')
    def test_fetch_feed_empty_entries(self, mock_parse):
        """Should handle feeds with no entries."""
        mock_parse.return_value = MagicMock(
            feed={'title': 'Empty Feed'},
            entries=[]
        )

        result = fetch_feed('https://example.com/feed')

        assert result['entries'] == []

    @patch('dismal.feedparser.parse')
    def test_fetch_feed_missing_entry_fields(self, mock_parse):
        """Should handle entries with missing fields gracefully."""
        mock_parse.return_value = MagicMock(
            feed={'title': 'Test Feed'},
            entries=[{}]  # Entry with no fields
        )

        result = fetch_feed('https://example.com/feed')

        assert result['entries'][0] == {'title': '', 'link': '', 'published': ''}


class TestMain:
    """Tests for the main function."""

    @patch('dismal.load_sources')
    @patch('dismal.fetch_feed')
    def test_main_writes_json_output(self, mock_fetch, mock_load, tmp_path, monkeypatch):
        """Should write aggregated feeds to JSON file."""
        monkeypatch.chdir(tmp_path)
        mock_load.return_value = ['https://example.com/feed']
        mock_fetch.return_value = {
            'source': 'Test Feed',
            'url': 'https://example.com/feed',
            'entries': []
        }

        main()

        with open('data.json') as f:
            data = json.load(f)

        assert 'generated' in data
        assert 'feeds' in data
        assert len(data['feeds']) == 1

    @patch('dismal.load_sources')
    @patch('dismal.fetch_feed')
    def test_main_handles_fetch_errors(self, mock_fetch, mock_load, tmp_path, monkeypatch):
        """Should catch exceptions and record errors in output."""
        monkeypatch.chdir(tmp_path)
        mock_load.return_value = ['https://example.com/feed']
        mock_fetch.side_effect = Exception('Network error')

        main()

        with open('data.json') as f:
            data = json.load(f)

        assert data['feeds'][0]['error'] == 'Network error'
        assert data['feeds'][0]['entries'] == []
```

### Priority 2: Integration Tests

```python
class TestIntegration:
    """Integration tests with real (but controlled) data."""

    def test_end_to_end_with_mock_server(self):
        """Test full workflow with a mock RSS server."""
        # Use responses library to mock HTTP requests
        pass

    def test_output_json_schema(self, tmp_path, monkeypatch):
        """Validate output matches expected JSON schema."""
        # Use jsonschema library to validate structure
        pass
```

### Priority 3: Frontend Tests (Optional)

Using Jest and jsdom:

```javascript
describe('RSS Feed Renderer', () => {
    test('renders feed entries correctly', async () => {
        // Mock fetch and test DOM rendering
    });

    test('handles fetch errors gracefully', async () => {
        // Test error message display
    });

    test('escapes HTML in entry titles', async () => {
        // Test XSS protection
    });
});
```

---

## Implementation Roadmap

### Phase 1: Setup Testing Infrastructure
1. Add `pytest` to `requirements.txt`
2. Create `tests/` directory
3. Add `pytest.ini` or `pyproject.toml` configuration
4. Update GitHub Actions workflow to run tests

### Phase 2: Core Unit Tests
1. Implement `TestLoadSources` tests
2. Implement `TestFetchFeed` tests
3. Implement `TestMain` tests
4. Achieve >80% code coverage

### Phase 3: Integration & Edge Cases
1. Add integration tests with mocked HTTP responses
2. Add edge case tests (network failures, malformed feeds)
3. Add JSON schema validation

### Phase 4: CI/CD Integration
1. Add test step to `.github/workflows/dismal_json.yml`
2. Add coverage reporting
3. Block deploys on test failures

---

## Required Dependencies for Testing

Add to `requirements.txt`:
```
pytest>=7.0.0
pytest-cov>=4.0.0
responses>=0.23.0  # For mocking HTTP requests
```

---

## Summary

| Area | Priority | Effort | Impact |
|------|----------|--------|--------|
| `load_sources()` tests | High | Low | Medium |
| `fetch_feed()` tests | High | Medium | High |
| `main()` tests | High | Medium | High |
| Integration tests | Medium | Medium | High |
| Frontend tests | Low | High | Low |

The most impactful improvement would be adding unit tests for `fetch_feed()` and `main()`, as these handle external network requests and file I/O - the most likely points of failure.
