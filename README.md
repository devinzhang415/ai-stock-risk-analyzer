# AI Stock Analyzer (ASA)

Using a LLM, generate insights from company 10-K filings.

------

## Use

Provide your company name and email (to comply with SEC download guidelines) and the tickers of the companies you want to analyze.

> python asa.py <company name> <email address> <tickers>

> \>>> python asa.py MyCompany MyName@MyCompany.com AAPL MSFT

------

## Technical Details

ASA uses the [sec-edgar-downloader](https://sec-edgar-downloader.readthedocs.io/en/latest/) to download company filings from the SEC EDGAR database.
