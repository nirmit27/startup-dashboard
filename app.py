""" Root of the Web Application """

import time as t
import numpy as np
import pandas as pd
import streamlit as st

if __name__ == "__main__":
    # ---------------------------- C O N T E N T ---------------------------- #

    st.markdown("""
    <h1 style="text-align: center; color: lightblue; margin-bottom: 30px">
    Indian Startup Funding Dashboard
    </h1>
    """, unsafe_allow_html=True)

    df = pd.read_csv('resources/startup_funding.csv')

    # ---------------------------- S I D E B A R ---------------------------- #

    st.sidebar.title('Startup Funding Analysis')

    st.markdown("""
    """)

    option = st.sidebar.selectbox('Choose analysis option', ["Overall Analysis", "Startups", "Investors"])

    match option:
        case "Overall Analysis":
            st.subheader("Overall Analysis")
            st.markdown("""
                """)
            st.dataframe(df.head(10))
            st.divider()
        case "Startups":
            startup = st.sidebar.selectbox("Choose startup", df['Startup Name'].unique().tolist())
            btn1 = st.sidebar.button('Find Startup details')
            st.header("Startup Analysis")
            if btn1:
                st.markdown("""
                                """)
                st.subheader(f"{startup}")
                st.divider()
        case "Investors":
            investor = st.sidebar.selectbox("Choose startup", df['Investors Name'].unique().tolist())
            btn2 = st.sidebar.button('Find Investor details')
            st.header("Investor Analysis")
            if btn2:
                st.markdown("""
                                """)
                st.subheader(f"{investor}")
                st.divider()
