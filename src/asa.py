#!/usr/bin/env python
"""
Using a LLM, generate insights from company 10-K filings.

Usage: python asa.py <company name> <email address> <tickers>
       Tickers should be space-delimited.
"""

import edgar
import sys
from openai import OpenAI

def asa(tickers: list[str]) -> None:
    """
    Using a LLM, generate insights from company 10-K filings.
    Args:
        tickers: list of stock tickers to analyze.
    Returns:
        None
    """
    client = OpenAI()

    for ticker in tickers:
        ticker = ticker.upper()

        # Download 10-K filings
        company = edgar.Company(ticker)
        if company is None:
            print("> Ticker {} is invalid, continuing...".format(ticker))
            continue
        print("> Generating report for ticker {}...".format(ticker))
        filings = company.get_filings(form="10-K", date="1995-01-01:2023-12-31")

        # # Parse through filings year by year
        # for filing in filings:
        #     tenk = filing.obj()
        #     print(tenk["Item 1A"])
        #     break

    print("> Done.")

if __name__ == "__main__":
    # Parse args
    tickers = sys.argv[1:]
    asa(tickers)
