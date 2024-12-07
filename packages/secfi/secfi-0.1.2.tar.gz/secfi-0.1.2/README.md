# secfi Library

**secfi** is a Python library designed to simplify access to SEC (U.S. Securities and Exchange Commission) filings and perform basic web scraping of the retrieved documents.

```bash
# Installation
pip install secfi
```

## Features

### 1. `getCiks()`
Fetches a DataFrame of all company tickers and their corresponding Central Index Keys (CIKs).

```python
import secfi

ciks = secfi.getCiks()
print(ciks.head())
```

**Returns:**
A DataFrame with columns:
- `cik_str` – The raw CIK string.
- `title` – The company name.
- `cik` – The CIK padded to 10 digits (for SEC queries).

---

### 2. `getFils(ticker: str)`
Fetches recent filings for a specific company by its ticker.

```python
filings = secfi.getFils("AAPL")
print(filings.head())
```

**Parameters:**
- `ticker` (str): The company's ticker symbol.

**Returns:**
A DataFrame containing recent filings with columns like:
- `accessionNumber`
- `filingDate`
- `form`
- `url` (Direct link to the filing document)

---

### 3. `scrapLatest(ticker: str, form: str)`
Retrieves the textual content of the latest SEC filing of a specific form type for a given ticker.

```python
text = secfi.scrapLatest("AAPL", "10-K")
print(text[:500])  # Preview the first 500 characters
```

**Parameters:**
- `ticker` (str): The company's ticker symbol.
- `form` (str): The form type to retrieve (e.g., "10-K", "8-K").

**Returns:**
A string containing the cleaned text content of the filing.

---

### 4. `scrap(url: str, timeout: int = 15)`
Scrapes the textual content of a given URL.

```python
content = secfi.scrap("https://example.com")
print(content[:500])  # Preview the first 500 characters
```

**Parameters:**
- `url` (str): The URL to scrape.
- `timeout` (int): Timeout for the HTTP request (default is 15 seconds).

**Returns:**
The cleaned text content of the URL or an error message if the request fails.

---

## Notes
- The library uses a custom `User-Agent` to comply with SEC API requirements.
- Ensure that requests to the SEC website respect their usage policies and rate limits.

## License
This project is open source and available under the MIT License.




