#!/usr/bin/env python
"""
Using a LLM, generate risk insights from company 10-K filings.

Usage: python asra.py <ticker>
"""

import warnings ; warnings.warn = lambda *args,**kwargs: None # Disable deprecation warnings
import sys
import re
import io
import pandas as pd
from edgar import Company
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.agents import Tool, AgentType, initialize_agent
from langchain.chains import RetrievalQA
import streamlit as st

def get_risks(ticker: str) -> dict[str, str]:
    """
    Using a LLM, generate risk insights from company 10-K filings.
    Args:
        ticker: ticker of the stock to analyze.
    Return:
        Dictionary keyed by year to risk insights for the given year.
        None if ticker is invalid.
    """
    ticker = ticker.upper()

    risks_dict = {}

    # Gemini LLM
    llm = GoogleGenerativeAI(model="gemini-pro", temperature=0)

    # Text chunker and embedder
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Download 10-K filings
    company = Company(ticker)
    if company is None:
        print("> Ticker {} is invalid, continuing...".format(ticker))
        return None
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
            # Accessing this is the main time requirement of this function call
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

def risks_to_df(risks_dict: dict[str, str]) -> pd.DataFrame:
    """
    Parse LLM risk assessment into a Pandas dataframe.
    Args:
        risks_dict: risk assessment for a given company. Keyed by year. Entries are formatted like

        >>> risks["2023"]
        >>>
            **AAPL 2023 Risk Report Summary**

            **Risk 1: Supply Chain Disruptions**

            * **Likelihood:** 0.8 (High)
            * **Impact:** 0.9 (Very Severe)

            **Risk 2: Economic Downturn**

            * **Likelihood:** 0.6
            * **Impact:** 0.7 (Significant)
            * **Description:** A global economic downturn could reduce consumer spending on Apple products, particularly in discretionary categories.
            ...
    Return:
        Pandas dataframe of risk factors, with columns year, risk, likelihood, and impact.
    """
    # Regex patterns for finding risk, likelihood, and impact
    risk_pattern = r"\*\*Risk \d+:\s*(.*)\*\*"
    likelihood_pattern = r"\* \*\*Likelihood:\*\* (\d\.\d+|\d)"
    impact_pattern = r"\* \*\*Impact:\*\* (\d\.\d+|\d)"

    # Match each line and parse the data
    risk_str = "Year;Risk;Likelihood;Impact"
    for year, lines in risks_dict.items():
        lines = re.split("\n+", lines.strip())[1:]
        for line in lines:

            # Check if line contains risk
            risk = re.findall(risk_pattern, line)
            if risk:
                risk_str += "\n{};{};".format(year, risk[0])
                continue

            # Check if line contains likelihood
            likelihood = re.findall(likelihood_pattern, line)
            if likelihood:
                risk_str += "{};".format(likelihood[0])
                continue
                
            # Check if line contains impact
            impact = re.findall(impact_pattern, line)
            if impact:
                risk_str += "{}".format(impact[0])
                continue

    # Convert string to dataframe
    string_data = io.StringIO(risk_str)
    df = pd.read_csv(string_data, sep=";")

    # Format Year column as string
    df["Year"] = df["Year"].astype(str)

    return df

@st.cache_data
def get_risks_df(ticker: str) -> pd.DataFrame:
    """
    Get company risk assessment as a dataframe.
    Args:
        ticker: ticker of the stock to analyze.
    Return:
        Pandas dataframe of risk factors, with columns year, risk, likelihood, and impact.
        None if ticker is invalid.
    """
    risks_dict = get_risks(ticker)
    if risks_dict is None:
        return None
    risks_df = risks_to_df(risks_dict)
    return risks_df

if __name__ == "__main__":
    ticker = sys.argv[1]
    risks_df = get_risks_df(ticker)
    print(risks_df)
