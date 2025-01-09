""" Root of the Web Application """

import pandas as pd
import streamlit as st
from data_fetch import Data
import plotly.express as px
import matplotlib.pyplot as plt


# Utility functions


def lb(n=1):  # line breaks
    for _ in range(n):
        st.markdown(
            """
        <br>
        """,
            unsafe_allow_html=True,
        )


def page_header(title, color, size=2.8, top=100, bottom=50):
    st.markdown(
        f"""
    <h1 style="text-align: center; color: {color}; font-size: {size}rem; margin-top: -{top}px; margin-bottom: -{bottom}px">
    {title}
    </h1>
    """,
        unsafe_allow_html=True,
    )


def text(txt):
    st.markdown(
        f"""
    <p style="text-align: center; font-size: 1.5rem">
    {txt}
    </p>
    """,
        unsafe_allow_html=True,
    )


# Dataset

df = pd.read_csv("resources/startup_cleaned.csv")

# Page Configuration ...

ch_color = "#0e1117"
st.set_page_config(layout="wide", page_title="Startup Analysis", page_icon="📊")


# ---------------------------------- C O N T E N T ---------------------------------- #


def main():
    page_header(
        title="Indian Startup Funding Dashboard", color="lightblue", size=2.5, top=80
    )
    lb(3)
    c1, c2, c3 = st.columns((3, 8, 3), gap="medium")
    with c2:
        st.image(
            "resources/dataset-cover.jpg",
            caption="Dataset cover image",
            use_column_width="auto",
        )
        lb()
        st.markdown(
            """
        ##### A detailed analysis of Indian Startups based on a **Kaggle** dataset.
        Choose an analysis option from the **dropdown menu** in the sidebar to view the corresponding details. 📊
        """
        )
        st.markdown(
            """
        > Dataset link - [Indian Startup Funding](https://www.kaggle.com/datasets/sudalairajkumar/indian-startup-funding)
        """
        )


def overall():
    # Data items ...

    sdf = df.groupby(by="startup").amount

    total = round(df.amount.sum() / 10000)

    max = round(sdf.max().sort_values(ascending=False).head(1).values[0] / 10000)

    mean = round(sdf.sum().mean() / 100)

    # Rendered items ...

    page_header(title="Overall Analysis", color="lightblue", size=2.25)

    # C O L U M N S ...

    c1, c2, c3 = st.columns(3, gap="large")

    with c1:
        st.metric("Total Investment", str(total) + "Cr")
    with c2:
        st.metric("Maximum Investment", str(max) + "Cr")
    with c3:
        st.metric("Average Investment", str(mean) + "Cr")

    c4, padding, c5 = st.columns((10, 2, 10), gap="medium")
    c6, padding, c7 = st.columns((10, 2, 10), gap="medium")

    # LINE - CHART ...

    with c4:
        st.subheader("Month on Month Graph")

        opt = st.selectbox(
            "Select the type of aggregation", ["Total Investment", "Investment Count"]
        )

        if opt == "Total Investment":
            tdf = Data.momg1(df)

            # Graph 1
            st.line_chart(data=tdf, x="Month", y="Amount in Crores")

        elif opt == "Investment Count":
            tdf2 = Data.momg2(df)
            st.line_chart(data=tdf2, x="Month", y="Count of investments")

    # PIE CHART ...

    with c5:
        st.subheader("Top 5 Sectors")
        cp = Data.catpie(df)
        top5 = px.pie(
            labels=cp.index.values,
            values=cp.values,
            names=cp.index.values,
            height=400,
            width=500,
            color_discrete_sequence=px.colors.sequential.Tealgrn_r,
            hole=0.4,
        )
        st.plotly_chart(top5)

    with c6:
        st.subheader("Top 5 Startups")

        year1 = st.slider("Choose year for Startups", 2015, 2020, 2017)
        top5 = Data.top5st(df, year1)
        st.dataframe(top5, width=600)

    with c7:
        st.subheader("Top 5 Investors")

        year2 = st.slider("Choose year for Investors", 2015, 2020, 2017)
        top5 = Data.top5inv(df, year2)
        st.dataframe(top5, width=600)


def startups(btn1, df, startup):
    if btn1:
        dfs = Data.sup(df, startup)
        rnd = Data.stg(df, startup)
        inv = Data.sinv(df, startup)

        pad1, col, pad2 = st.columns((2, 8, 2), gap="small")

        with col:
            st.header(startup)
            st.divider()
            st.subheader("Overall details")
            st.dataframe(dfs)

            c1, pad, c2 = st.columns((10, 1, 10), gap="small")

            with c1:
                st.subheader("Stage")
                st.dataframe(rnd)

            with c2:
                st.subheader("Investor(s)")
                st.dataframe(inv)

    else:
        lb(2)
        text(
            "Select a <b style='color:lightblue'>startup</b> name from the dropdown menu located in the <b>sidebar</b> to view their details."
        )


def investors(btn2, df, investor):
    if btn2:
        st.header(investor)
        st.divider()

        col1, padd, col2 = st.columns((7, 2, 7), gap="small")
        col3, padd, col4 = st.columns((7, 2, 7), gap="small")
        col5, padd, col6 = st.columns((7, 2, 7), gap="small")

        with col1:
            recent = Data.mrinv(df, investor)
            st.subheader("Most recent investments")
            st.dataframe(recent)

        with col2:
            top5 = Data.biginv(df, investor)
            st.subheader("Top 5 investments")

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(top5["Startup"], top5["Amount in Crores"], color="lightblue")

            # Chart Color Customization ...

            ax.set_facecolor(ch_color)
            fig.set_facecolor(ch_color)

            # Chart LEGEND colors ...

            ax.tick_params(axis="x", colors="white", labelsize=8)
            ax.tick_params(axis="y", colors="white", labelsize=8)

            # Chart BORDER colors ...

            ax.spines["top"].set_color(ch_color)
            ax.spines["bottom"].set_color("white")
            ax.spines["left"].set_color("white")
            ax.spines["right"].set_color(ch_color)

            plt.xlabel("Startup", color="white", fontsize=10)
            plt.ylabel("Amount in Crores", color="white", fontsize=10)

            st.pyplot(fig)

        with col3:
            sec = Data.secinv(df, investor)
            st.subheader("Sectors of investment")
            pie1 = px.pie(
                labels=sec.index.values,
                values=sec.values,
                names=sec.index.values,
                hole=0.4,
                height=400,
                width=500,
                color_discrete_sequence=px.colors.sequential.Teal,
            )
            st.plotly_chart(pie1)

        with col4:
            city = Data.city(df, investor)
            st.subheader("Cities of investment")
            pie3 = px.pie(
                labels=city.index.values,
                values=city.values,
                names=city.index.values,
                hole=0.4,
                height=400,
                width=500,
                color_discrete_sequence=px.colors.sequential.Darkmint_r,
            )
            st.plotly_chart(pie3)

        with col5:
            stg = Data.stginv(df, investor)
            st.subheader("Stages of investment")
            pie2 = px.pie(
                labels=stg.index.values,
                values=stg.values,
                names=stg.index.values,
                hole=0.4,
                height=400,
                width=500,
                color_discrete_sequence=px.colors.sequential.Blugrn_r,
            )
            st.plotly_chart(pie2)

        with col6:
            yearly = Data.yrinv(df, investor)
            st.subheader("Year on year investment")
            st.line_chart(yearly, y="Amount in Crores")

    else:
        lb(2)
        text(
            "Select an <b style='color:lightblue'>investor</b> name from the dropdown menu located in the <b>sidebar</b> to view their details."
        )


# ---------------------------------- S I D E B A R ---------------------------------- #


st.sidebar.title("Startup Funding Analysis")

lb()

option = st.sidebar.selectbox(
    "Choose analysis option", ["Data", "Overall Analysis", "Startups", "Investors"]
)

if option == "Data":
    main()
elif option == "Overall Analysis":
    overall()
elif option == "Startups":
    page_header(title="Startup Analysis", color="lightgreen", size=2.5)
    startup = st.sidebar.selectbox("Select a startup", df["startup"].unique().tolist())
    btn1 = st.sidebar.button("Find Startup details")
    startups(btn1, df, startup)
elif option == "Investors":
    page_header(title="Investor Analysis", color="lightgreen", size=2.5)
    investor = st.sidebar.selectbox("Select an investor", Data.investor_list(df))
    btn2 = st.sidebar.button("Find Investor details")
    investors(btn2, df, investor)
