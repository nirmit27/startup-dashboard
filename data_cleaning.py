""" Data Cleaning """

import numpy as np
import pandas as pd

if __name__ == "__main":
    df = pd.read_csv('resources/start_funding.csv')

    print(df.head())
