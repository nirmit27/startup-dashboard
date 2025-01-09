""" Data Cleaning """


class Data:

    @staticmethod
    def investor_list(df):
        il = sorted(set(df["investors"].str.split(", ").sum()))
        return il

    # ------------------------------------- Page 1 ------------------------------------- #

    # for Line Chart - Option 1

    @staticmethod
    def momg1(df):
        tdf = df.groupby(["year", "month"])["amount"].sum().reset_index()
        tdf["Y"] = tdf["amount"] / 10000
        tdf.rename(columns={"Y": "Amount in Crores"}, inplace=True)
        for i in range(tdf.shape[0]):
            tdf.at[i, "Month"] = f"{tdf.at[i, 'month'][:3]} '{tdf.at[i, 'year'] - 2000}"
        tdf.drop(columns=["year", "month"], inplace=True)
        return tdf

    # for Line Chart - Option 2

    @staticmethod
    def momg2(df):
        tdf2 = df.groupby(["year", "month"])["amount"].count().reset_index()
        tdf2.rename(columns={"amount": "Count of investments"}, inplace=True)
        for i in range(tdf2.shape[0]):
            tdf2.at[i, "Month"] = (
                f"{tdf2.at[i, 'month'][:3]} '{tdf2.at[i, 'year'] - 2000}"
            )
        tdf2.drop(columns=["year", "month"], inplace=True)
        return tdf2

    # for Pie Chart ...

    @staticmethod
    def catpie(df):
        cat = df.groupby("vertical")["amount"].sum()
        cat = cat.sort_values(ascending=False)
        return cat.head()

    # for Top 5 Startups DF ...

    @staticmethod
    def top5st(df, y):
        top5 = df.groupby(["startup", "year", "month"])["amount"].sum().reset_index()
        top5["amount"] = top5["amount"] / 10000
        top5.rename(
            columns={"amount": "Amount in Cr.", "month": "Month", "startup": "Startup"},
            inplace=True,
        )
        top5.set_index("Startup", inplace=True)
        return (
            top5.query(f"year == {y}")[["Month", "Amount in Cr."]]
            .head()
            .sort_values(by="Amount in Cr.", ascending=False)
            .head()
        )

    # for Top 5 Investors DF ...

    @staticmethod
    def top5inv(df, y):
        top5 = df.groupby(["investors", "year", "month"])["amount"].sum().reset_index()
        top5["amount"] = top5["amount"] / 10000
        top5.rename(
            columns={
                "amount": "Amount in Cr.",
                "month": "Month",
                "investors": "Investor",
            },
            inplace=True,
        )
        top5.set_index("Investor", inplace=True)
        return (
            top5.query(f"year == {y}")[["Month", "Amount in Cr."]]
            .sort_values(by="Amount in Cr.", ascending=False)
            .head()
        )

    # ------------------------------------- Page 2 ------------------------------------- #

    #  S T A R T U P   A N A L Y S I S

    # Startup details ...

    @staticmethod
    def sup(df, name):
        res = df[df["startup"] == name][
            ["date", "vertical", "subvertical", "city", "round", "amount"]
        ]
        res.rename(columns={"amount": "amount in Cr."}, inplace=True)
        res.set_index("date", inplace=True)
        return res.head()

    # Startup round investment ...

    @staticmethod
    def stg(df, name):
        df.rename(columns={"amount": "amount in Cr."}, inplace=True)
        res = df[df["startup"] == name].groupby("round")["amount in Cr."].sum()
        return res.head()

    # Startup investor(s) ...

    @staticmethod
    def sinv(df, name):
        res = df[df["startup"] == name]["investors"]
        res = res.reset_index(drop=True)
        res.index = res.index + 1
        return res

    # ------------------------------------- Page 3 ------------------------------------- #

    #  I N V E S T O R   A N A L Y S I S

    # Most recent investments (Top 5) ...

    @staticmethod
    def mrinv(df, name):
        recent = df[df["investors"].str.contains(name)][
            ["date", "startup", "vertical", "city", "round", "amount"]
        ].sort_values(by="date", ascending=False)
        recent.rename(columns={"amount": "amount in Cr."}, inplace=True)
        recent.set_index("date", inplace=True)
        return recent.head()

    # Biggest investments ...  B A R

    @staticmethod
    def biginv(df, name):
        df.rename(
            columns={"amount": "Amount in Crores", "startup": "Startup"}, inplace=True
        )
        big = (
            df[df["investors"].str.contains(name)]
            .groupby("Startup")["Amount in Crores"]
            .sum()
        )

        big.sort_values(inplace=True, ascending=False)

        big = big.reset_index()

        return big.head()

    # Sectors invested ...  P I E  # 1

    @staticmethod
    def secinv(df, name):
        sec = (
            df[df["investors"].str.contains(name)]
            .groupby("vertical")["Amount in Crores"]
            .sum()
            .head()
        )
        return sec

    # Stages invested ...   P I E  # 2

    @staticmethod
    def stginv(df, name):
        stg = (
            df[df["investors"].str.contains(name)]
            .groupby("round")["Amount in Crores"]
            .sum()
            .head()
        )
        return stg

    # Cities ...            P I E  # 3

    @staticmethod
    def city(df, name):
        ct = (
            df[df["investors"].str.contains(name)]
            .groupby("city")["Amount in Crores"]
            .sum()
            .head()
        )
        return ct

    # Year on Year investment ...

    @staticmethod
    def yrinv(df, name):
        df.rename(columns={"amount": "Amount in Crores", "year": "Year"}, inplace=True)
        yi = (
            df[df["investors"].str.contains(name)]
            .groupby("Year")["Amount in Crores"]
            .sum()
        )
        return yi
