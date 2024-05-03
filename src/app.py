#!/usr/bin/env python
"""
Frontend visualization. Display risk factors for a given company in a risk matrix.

Usage: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import altair as alt
import re
import io

def risks_to_df(risks: str) -> dict[str, pd.DataFrame]:
    """
    Parse LLM risk assessment into a Pandas dataframe.
    Args:
        risks: risk assessment for a given company. Formatted like

        >>>
            **1995:**

            * **Economic downturn:** [Likelihood: 0.5, Impact: 0.7]
            * **Competition from new entrants:** [Likelihood: 0.6, Impact: 0.8]

            **2000:**

            * **Dot-com bubble burst:** [Likelihood: 0.7, Impact: 0.9]
            * **9/11 terrorist attacks:** [Likelihood: 0.2, Impact: 0.8]
            ...
    Return:
        Dictionary of pandas dataframe of risk factors, keyed by year.
    """
    dfs = {}

    # Define the regex patterns to extract year and entries
    year_pattern = r"\*\*(\d+):"
    entry_pattern = r"\*\*\s*([^*]+?)\s*:\*\*\s*\[Likelihood:\s*([\d.]+),\s*Impact:\s*([\d.]+)\]"

    # Find all matches for year and entries
    years = re.findall(year_pattern, risks)
    entries = re.findall(entry_pattern, risks)

    for year in years:
        None


    # curr_year = "" # Current year to assign risks to
    # lines = risks.strip().split("\n")
    # for line in lines:

    #     # Year lines start with "**" and ends with ":**"
    #     if line.startswith("**") and line.endswith(":**"):
    #         curr_year = line[2:][:-3]
    #         if curr_year not in dfs:
    #             dfs[curr_year] = "Risk;Likelihood;Impact"

    #     # Risk lines start with "* **"
    #     elif line.startswith("* **"):
    #         None

    # # Convert risk strings to dataframes
    # for year, risk_str in dfs:
    #     string_data = io.StringIO(risk_str)
    #     df = pd.read_csv(string_data, sep=";")
    #     dfs[year] = df

    return dfs

risks = """
**1995:**

* **Economic downturn:** [Likelihood: 0.5, Impact: 0.7]
* **Competition from new entrants:** [Likelihood: 0.6, Impact: 0.8]

**2000:**

* **Dot-com bubble burst:** [Likelihood: 0.7, Impact: 0.9]
* **9/11 terrorist attacks:** [Likelihood: 0.2, Impact: 0.8]

**2005:**

* **Housing market crash:** [Likelihood: 0.6, Impact: 0.8]
* **Rise of social media:** [Likelihood: 0.8, Impact: 0.7]

**2010:**

* **Global financial crisis:** [Likelihood: 0.7, Impact: 0.9]
* **Increased regulation:** [Likelihood: 0.6, Impact: 0.7]

**2015:**

* **Brexit:** [Likelihood: 0.4, Impact: 0.6]
* **Cybersecurity threats:** [Likelihood: 0.8, Impact: 0.8]

**2020:**

* **COVID-19 pandemic:** [Likelihood: 0.9, Impact: 0.9]
* **Supply chain disruptions:** [Likelihood: 0.7, Impact: 0.8]

**2023:**

* **Economic recession:** [Likelihood: 0.6, Impact: 0.8]
* **Climate change:** [Likelihood: 0.7, Impact: 0.9]
        """
risks_to_df(risks)

# @st.cache_data
# def get_UN_data():
#     AWS_BUCKET_URL = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com"
#     df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
#     return df.set_index("Region")

# try:
#     df = get_UN_data()
#     countries = st.multiselect(
#         "Choose countries", list(df.index), ["China", "United States of America"]
#     )
#     if not countries:
#         st.error("Please select at least one country.")
#     else:
#         data = df.loc[countries]
#         data /= 1000000.0
#         st.write("### Gross Agricultural Production ($B)", data.sort_index())

#         data = data.T.reset_index()
#         data = pd.melt(data, id_vars=["index"]).rename(
#             columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
#         )
#         chart = (
#             alt.Chart(data)
#             .mark_area(opacity=0.3)
#             .encode(
#                 x="year:T",
#                 y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
#                 color="Region:N",
#             )
#         )
#         st.altair_chart(chart, use_container_width=True)
# except:
#     None
