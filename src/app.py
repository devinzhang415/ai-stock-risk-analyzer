#!/usr/bin/env python
"""
Frontend visualization. Display risk factors for a given company in a risk matrix.

Usage: streamlit run app.py
"""

import streamlit as st
import asra
import plotly.express as px

def main():
    st.title('AI Stock Risk Analyzer')
    st.markdown(
        """
        Parse company 10-K filings and utilize LLMs to analyze company risks.
        """)

    # Select ticker and year
    ticker = st.text_input("Input Ticker", placeholder="AAPL")
    # ticker = st.selectbox('Choose Ticker', ["AAPL", "TSLA", "GME"])
    year = st.slider("Year", 1995, 2023)

    try:
        # Load ticker risk dataframe
        risks_df = asra.get_risks_df(ticker)
        if risks_df is None:
            risks_df = "" # String input to st.dataframe throws error, triggering Exception screen
        year_risks_df = risks_df[risks_df["Year"] == str(year)]
        st.dataframe(year_risks_df, hide_index=True, use_container_width=True)

        # Plot dataframe
        fig = px.scatter(
            year_risks_df,
            x="Impact",
            y="Likelihood",
            text="Risk",
            color="Impact",
            color_continuous_scale=[(0, "green"), (0.3, "yellow"), (1, "red")]
        )
        fig.update_layout(font=dict(size=8))
        fig.update_traces(textposition='top center')
        fig.update_xaxes(range=[0, 1])
        fig.update_yaxes(range=[0, 1])
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    except:
        st.markdown("Please input a valid ticker.")

if __name__ == "__main__":
    main()
