#!/usr/bin/env python
"""
Frontend visualization. Display risk factors for a given company in a risk matrix.

Usage: streamlit run app.py
"""

import streamlit as st
import altair as alt
import asra

def main():
    st.title('AI Stock Risk Analyzer')

    ticker = st.text_input("Input Ticker", placeholder="AAPL", )

    try:
        risks_df = asra.get_risks_df(ticker)
        st.dataframe(risks_df, hide_index=True, use_container_width=True)
    except:
        st.markdown("Please input a ticker.")




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

if __name__ == "__main__":
    main()
