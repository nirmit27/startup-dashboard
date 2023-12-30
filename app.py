""" Root of the Web Application """

import pandas as pd
import streamlit as st
from data_fetch import Data
import plotly.express as px

# Utility functions


def lb(n=1):  # line breaks
    for _ in range(n):
        st.markdown('''
        <br>
        ''', unsafe_allow_html=True)


def page_header(title, color):
    st.markdown(f"""
    <h1 style="text-align: center; color: {color}; font-size: 2.8rem">
    {title}
    </h1>
    """, unsafe_allow_html=True)


def text(txt):
    st.markdown(f"""
    <p style="text-align: center; font-size: 1.5rem">
    {txt}
    </p>
    """, unsafe_allow_html=True)


# Dataset

df = pd.read_csv('resources/startup_cleaned.csv')

# Page Configuration ...

st.set_page_config(layout='wide', page_title='Startup Analysis', page_icon='📊')

# ---------------------------------- C O N T E N T ---------------------------------- #


def main():
    page_header(title='Indian Startup Funding Dashboard', color='lightblue')
    lb(4)
    c1, c2, c3 = st.columns((3, 10, 3), gap='medium')
    with c2:
        st.image('resources/dataset-cover.jpg',
                 caption='Dataset cover image', use_column_width='auto')
        lb()
        st.markdown("""
        ### Get a detailed analysis of Indian Startups based on a dataset from _Kaggle_. 📊
        """)
        lb()
        st.markdown("""
        #### Dataset link - [Indian Startup Funding](https://www.kaggle.com/datasets/sudalairajkumar/indian-startup-funding)
        """)


def overall():

    # Data items ...

    sdf = df.groupby(by="startup").amount

    total = round(df.amount.sum() / 10000)

    max = round(sdf.max().sort_values(
        ascending=False).head(1).values[0] / 10000)

    mean = round(sdf.sum().mean() / 100)

    # Rendered items ...

    st.title("Overall Analysis")
    st.divider()

    st.subheader('Startup Investments _(in INR)_')

    # C O L U M N S ...

    c1, c2, c3 = st.columns(3, gap='large')

    with c1:
        st.metric('Total', str(total) + 'Cr')
    with c2:
        st.metric('Maximum', str(max) + 'Cr')
    with c3:
        st.metric('Average', str(mean) + 'Cr')
    lb()

    c4, c5 = st.columns(2, gap='large')
    c4, padding, c5 = st.columns((10, 2, 10), gap='medium')

    with c4:  # LINE - CHART
        st.subheader('Month on Month Graph')
        lb()

        opt = st.selectbox('Select the type of aggregation', [
                           'Total Investment', 'Investment Count'])
        lb()
        match(opt):
            case 'Total Investment':
                tdf = Data.momg1(df)

                # Graph 1
                st.line_chart(data=tdf, x='Month', y='Amount in Crores')

            case 'Investment Count':
                tdf2 = Data.momg2(df)
                st.line_chart(data=tdf2, x='Month', y='Count of investments')
        lb()

        st.subheader('Top 5 Startups')
        lb()

        year1 = st.slider('Choose year for Startups', 2015, 2020, 2017)
        top5 = Data.top5st(df, year1)
        st.dataframe(top5, width=600)

    with c5:  # PIE CHART
        st.subheader('Top 5 Sectors')
        cp = Data.catpie(df)
        top5 = px.pie(
            labels=cp.head().values,
            names=cp.head().index,
            height=480,
            color_discrete_sequence=px.colors.sequential.dense_r,
            hole=0.4
        )
        st.plotly_chart(top5)

        lb()
        st.subheader('Top 5 Investors')
        lb()

        year2 = st.slider('Choose year for Investors', 2015, 2020, 2017)
        top5 = Data.top5inv(df, year2)
        st.dataframe(top5, width=600)


def startups(btn1, df, startup):
    if btn1:
        dfs = Data.sup(df, startup)
        rnd = Data.stg(df, startup)
        inv = Data.sinv(df, startup)

        pad1, col, pad2 = st.columns((2, 8, 2), gap='small')

        with col:
            lb()
            st.header(startup)
            st.divider()
            st.subheader('Overall details')
            st.dataframe(dfs)
            lb()

            st.subheader('Stage')
            st.dataframe(rnd)
            lb()

            st.subheader("Investor(s)")
            st.dataframe(inv)

    else:
        lb(2)
        text("Select a <b style='color:lightblue'>startup</b> name from the dropdown menu located in the <b>sidebar</b> to view their details.")


def investors(btn2, df, investor):
    if btn2:
        lb()
        st.header(investor)
        st.divider()
        dfi = Data.inv(df, investor)
        st.dataframe(dfi)

    else:
        lb(2)
        text("Select an <b style='color:lightblue'>investor</b> name from the dropdown menu located in the <b>sidebar</b> to view their details.")

# ----------------------------------------------------------------------------------- #

# ---------------------------------- S I D E B A R ---------------------------------- #


st.sidebar.title('Startup Funding Analysis')

lb()

option = st.sidebar.selectbox('Choose analysis option', [
                              "Data", "Overall Analysis", "Startups", "Investors"])

match option:
    case "Data":
        main()
    case "Overall Analysis":
        overall()
    case "Startups":
        page_header(title="Startup Analysis", color="lightgreen")
        startup = st.sidebar.selectbox(
            "Select a startup", df['startup'].unique().tolist())
        btn1 = st.sidebar.button('Find Startup details')
        startups(btn1, df, startup)
    case "Investors":
        page_header(title="Investor Analysis", color="lightgreen")
        investor = st.sidebar.selectbox(
            "Select an investor", df['investors'].unique().tolist())
        btn2 = st.sidebar.button('Find Investor details')
        investors(btn2, df, investor)

# ----------------------------------------------------------------------------------- #
