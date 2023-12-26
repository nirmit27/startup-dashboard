""" Data Cleaning """

import numpy as np
import pandas as pd


class Cleaner:

    @staticmethod
    def cols(df):
        print(df.columns)


if __name__ == "__main__":
    data = pd.read_csv('resources/startup_funding.csv')

    Cleaner.cols(data)
