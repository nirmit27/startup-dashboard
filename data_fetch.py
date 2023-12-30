""" Data Cleaning """

import numpy as np
import pandas as pd


class Data:

    # ------------------------------------- Page 1 ------------------------------------- #

    # for Line Chart - Option 1

    @staticmethod
    def momg1(df):
        tdf = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        tdf['Y'] = tdf['amount'] / 10000
        tdf.rename(columns={'Y': 'Amount in Crores'}, inplace=True)
        for i in range(tdf.shape[0]):
            tdf.at[i,
                   'Month'] = f"{tdf.at[i, 'month'][:3]} '{tdf.at[i, 'year'] - 2000}"
        tdf.drop(columns=['year', 'month'], inplace=True)
        return tdf

    # for Line Chart - Option 2

    @staticmethod
    def momg2(df):
        tdf2 = df.groupby(['year', 'month'])[
            'amount'].count().reset_index()
        tdf2.rename(columns={'amount': 'Count of investments'}, inplace=True)
        for i in range(tdf2.shape[0]):
            tdf2.at[i,
                    'Month'] = f"{tdf2.at[i, 'month'][:3]} {tdf2.at[i, 'year'] - 2000}"
        tdf2.drop(columns=['year', 'month'], inplace=True)
        return tdf2

    # for Pie Chart ...

    @staticmethod
    def catpie(df):
        cat = df.groupby('vertical')[['vertical', 'amount']].head(5)
        cat = cat.set_index('vertical')
        return cat

    # for Top 5 Startups DF ...

    @staticmethod
    def top5st(df, y):
        top5 = df.groupby(['startup', 'year', 'month'])[
            'amount'].sum().reset_index()
        top5['amount'] = top5['amount'] / 10000
        top5.rename(columns={'amount': "Amount in Cr.",
                    'month': 'Month', 'startup': 'Startup'}, inplace=True)
        top5.set_index('Startup', inplace=True)
        return top5.query(f"year == {y}")[['Month', 'Amount in Cr.']].head().sort_values(by='Amount in Cr.', ascending=False).head()

    # for Top 5 Investors DF ...

    @staticmethod
    def top5inv(df, y):
        top5 = df.groupby(['investors', 'year', 'month'])[
            'amount'].sum().reset_index()
        top5['amount'] = top5['amount'] / 10000
        top5.rename(columns={'amount': "Amount in Cr.",
                    'month': 'Month', 'investors': 'Investor'}, inplace=True)
        top5.set_index('Investor', inplace=True)
        return top5.query(f"year == {y}")[['Month', 'Amount in Cr.']].sort_values(by='Amount in Cr.', ascending=False).head()

    # ---------------------------------------------------------------------------------- #

    # ------------------------------------- Page 2 ------------------------------------- #
