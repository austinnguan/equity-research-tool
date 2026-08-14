"""
Convert an SEC filing from HTML to clean text.

Two ways in:
  1. fetch_10k_html(url, outfile)   -- download from EDGAR, then convert
  2. convert_html_file(infile, outfile) -- convert an .htm you already saved

Conversion is always a separate pre-step. parse_10k.py only ever reads the .txt.

Usage:
    python fetch_10k_html.py                      # download from EDGAR
    python fetch_10k_html.py chipotle10k.html     # convert a local file
"""

import sys
import requests
from bs4 import BeautifulSoup

# SEC requires a real User-Agent header (name + email) or it blocks the request
HEADERS = {"User-Agent": "Austin Guan austinlguan@gmail.com"}

FILING_URL = "https://www.sec.gov/Archives/edgar/data/1058090/000105809026000009/cmg-20251231.htm"
OUTFILE = "chipotle_10k.txt"


def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser")

    # strip tags that add noise, not content
    for tag in soup(["script", "style"]):
        tag.decompose()

    # Modern EDGAR filings are inline XBRL. The <ix:header> block holds hundreds
    # of KB of machine-readable context/unit definitions that render as nothing
    # in a browser but dump garbage into get_text(). Same for ix:hidden.
    for tag in soup.find_all(["ix:header", "ix:hidden"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    # collapse the blank-line mess HTML->text conversion always leaves behind
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def _save(clean_text, outfile):
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(clean_text)
    print(f"Saved {len(clean_text):,} characters to {outfile}")


def fetch_10k_html(url, outfile):
    """Download a filing from EDGAR and convert it."""
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    _save(html_to_text(resp.text), outfile)


def convert_html_file(infile, outfile):
    """Convert an .htm file already saved to disk."""
    with open(infile, encoding="utf-8", errors="ignore") as f:
        html = f.read()
    _save(html_to_text(html), outfile)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        convert_html_file(sys.argv[1], OUTFILE)
    else:
        fetch_10k_html(FILING_URL, OUTFILE)
