#!/usr/bin/env python
"""
Using a LLM, generate insights from company 10-K filings.

Usage: python asa.py <company name> <email address> <tickers>
"""

# https://sec-edgar-downloader.readthedocs.io/en/latest/
from sec_edgar_downloader import Downloader
import sys

def asa(company: str, email: str, tickers: list[str]):
    """
    Using a LLM, generate insights from company 10-K filings.
    Args:
        company: company name to provide to SEC EDGAR to comply with download guidelines.
        email: email to provide to SEC EDGAR to comply with download guidelines.
        tickers: list of stock tickers to analyze.
    Returns:
        None
    """
    d1 = Downloader(company, email)

    for ticker in tickers:
        ticker = ticker.upper()

        # Download 10-K filings
        d1.get("10-K", ticker, after="1995-01-01", before="2023-12-31")

if __name__ == "__main__":
    company, email = sys.argv[1], sys.argv[2]
    tickers = []
    for i in range(3, len(sys.argv)):
        tickers.append(sys.argv[i])
    asa(company, email, tickers)
