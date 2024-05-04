#!/usr/bin/env python
"""
Using a LLM, generate risk insights from company 10-K filings.

Usage: python asra.py <tickers>
       Tickers should be space-delimited.
"""

import warnings ; warnings.warn = lambda *args,**kwargs: None # Disable deprecation warnings
import sys
from edgar import Company
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.agents import Tool, AgentType, initialize_agent
from langchain.chains import RetrievalQA

def asra(tickers: list[str]) -> dict[str, str]:
    """
    Using a LLM, generate risk insights from company 10-K filings.
    Args:
        tickers: list of stock tickers to analyze.
    Return:
        Dictionary keyed by year to risk insights for the given year.
    """
    risks_dict = {}

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

        # Parse through filings year by year
        for filing in filings:
            # Get filing year
            year = str(filing.filing_date.year)
            filing_name = "{} {}".format(ticker, year)

            # Get filing text
            tenk = filing.obj()
            text = ""

            # Exception block as internally tenk-type objects call self's HTML,
            # which may be None. However, no error-checking occurs;
            # no way to determine if HTML will be None as call is internal
            try:
                # Parse and chunk risk factors
                risk = tenk["Item 1A"]
                if risk is None:
                    continue
                text += "\n" + risk
            except:
                None
            
            if text == "":
                continue

            # Chunk text
            text_split = splitter.split_text(text)
            
            # Form database
            retriever = FAISS.from_texts(text_split, embeddings).as_retriever()
            tool = Tool(
                name="{} Risk Report".format(filing_name),
                description="Useful when you want to answer questions about the risks {} faces in {}".format(ticker, year),
                func=RetrievalQA.from_chain_type(llm=llm, retriever=retriever),
            )

            # Query database
            # Despite being optimized for OpenAI, a multi function agent is still speedy for other models
            agent = initialize_agent(
                agent=AgentType.OPENAI_MULTI_FUNCTIONS,
                tools=[tool],
                llm=llm,
                verbose=False,
                max_execution_time=600
            )
            question = """
                        Summarize the {} Risk Report.
                        Score each risk by how likely it is to happen, and the impact it has.
                        Score on a scale between 0 and 1.
                    """.format(filing_name)
            answer = agent({"input": question})["output"]
            print(answer)

            risks_dict[year] = answer

    print("> Done.")
    return risks_dict

if __name__ == "__main__":
    # Parse args
    tickers = sys.argv[1:]
    asra(tickers)
