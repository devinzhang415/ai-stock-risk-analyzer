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
from asra import asra

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
            * **Description:** Global supply chain disruptions, including component shortages, transportation delays, and geopolitical tensions, could impact Apple's production and delivery timelines.

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
        for i in range(0, len(lines), 4):
            risk = re.findall(risk_pattern, lines[i])
            likelihood = re.findall(likelihood_pattern, lines[i + 1])
            impact = re.findall(impact_pattern, lines[i + 2])
            print(year,risk,likelihood,impact)
            risk_str += "\n{};{};{};{}".format(year, risk[0], likelihood[0], impact[0])

    # Convert string to dataframe
    string_data = io.StringIO(risk_str)
    df = pd.read_csv(string_data, sep=";")

    return df

print(risks_to_df(asra(["GME"])))
# risks_dict = {
#     "2023": """**AAPL 2023 Risk Report Summary**

#             **Risk 1: Supply Chain Disruptions**

#             * **Likelihood:** 0.8 (High)
#             * **Impact:** 0.9 (Very Severe)
#             * **Description:** Global supply chain disruptions, including component shortages, transportation delays, and geopolitical tensions, could impact Apple's production and delivery timelines.

#             **Risk 2: Economic Downturn**

#             * **Likelihood:** 1
#             * **Impact:** 0.7 (Significant)
#             * **Description:** A global economic downturn could reduce consumer spending on Apple products, particularly in discretionary categories."""
# }
# risks_to_df(risks_dict)

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
