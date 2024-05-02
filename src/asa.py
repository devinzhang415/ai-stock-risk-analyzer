#!/usr/bin/env python
"""
Using a LLM, generate insights from company 10-K filings.

Usage: python asa.py <company name> <email address> <tickers>
       Tickers should be space-delimited.
"""

import sys
from edgar import Company
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.agents import Tool
from langchain.chains import RetrievalQA

def asa(tickers: list[str]) -> None:
    """
    Using a LLM, generate insights from company 10-K filings.
    Args:
        tickers: list of stock tickers to analyze.
    Returns:
        None
    """
    # Gemini LLM
    llm = GoogleGenerativeAI(model="gemini-pro", temperature=0)

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
        # filings = company.get_filings(form="10-K", date="1999-01-01:1999-12-31")

        tools = []

        # Parse through filings year by year
        for filing in filings:
            # Get filing year
            year = str(filing.filing_date.year)
            filing_name = "{} {}".format(ticker, year)

            tenk = filing.obj()
            text = ""

            # Exception block as internally tenk-type objects call self's HTML,
            # which may be None. However, no error-checking occurs;
            # no way to determine if HTML will be None as call is internal
            try:
                # Parse and chunk risk factors
                risk = tenk["Item 1A"]
                if risk is None:
                    risk = ""
                text += "\n" + risk
            except:
                None
            
            text_split = splitter.split_text(text)
            
            # # Initialize vector database
            # retriever = FAISS.from_texts(risk_split, embeddings).as_retriever()
            # tool = Tool(
            #     name=filing_name,
            #     description="Useful when you want to answer questions about {}".format(filing_name),
            #     func=RetrievalQA.from_chain_type(llm=llm, retriever=retriever),
            # )
            # tools.append(tool)

    print("> Done.")

if __name__ == "__main__":
    # Parse args
    tickers = sys.argv[1:]
    asa(tickers)
