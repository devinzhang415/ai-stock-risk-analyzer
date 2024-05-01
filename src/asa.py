#!/usr/bin/env python
"""
Using a LLM, generate insights from company 10-K filings.

Usage: python asa.py <company name> <email address> <tickers>
       Tickers should be space-delimited.
"""

import sys
import time
from edgar import Company
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

def asa(tickers: list[str]) -> None:
    """
    Using a LLM, generate insights from company 10-K filings.
    Args:
        tickers: list of stock tickers to analyze.
    Returns:
        None
    """
    # Text chunker and embedder
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    for ticker in tickers:
        ticker = ticker.upper()

        # Download 10-K filings
        company = Company(ticker)
        if company is None:
            print("> Ticker {} is invalid, continuing...".format(ticker))
            continue
        print("> Generating report for ticker {}...".format(ticker))
        filings = company.get_filings(form="10-K", date="1995-01-01:2023-12-31")

        # Parse through filings year by year
        for filing in filings:
            tenk = filing.obj()

            # Parse and chunk risk factors
            risk = tenk["Item 1A"]
            risk_split = splitter.split_text(risk)
            
            # Initialize vector database
            # Fed piece by piece to avoid rate-limiting

            db = Chroma.from_texts(
                    risk_split,
                    embeddings,
                    persist_directory="./chroma_db"
                )

            # for s in risk_split:
            #     Chroma.from_texts(
            #         [s],
            #         embeddings,
            #         persist_directory="./chroma_db"
            #     )
            #     time.sleep(60)

            query = "What are the major risk factors?"
            docs = db.similarity_search(query)
            print(docs[0].page_content)


            break

    print("> Done.")

if __name__ == "__main__":
    # Parse args
    tickers = sys.argv[1:]
    asa(tickers)
