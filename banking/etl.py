import pandas as pd

#Load
try:
    df = pd.read_csv("data.csv")
    print(df.head())

except FileNotFoundError:
    print("data.csv not found")

except pd.errors.EmptyDataError:
    print("data.csv file is empty")

except Exception as e:
    print(f"Unknown exception occured: {e}")

#transform
try:
    curr_year = 2025
    print(df.dtypes)

    df["DOB"] = pd.to_datetime(df["DOB"])
    df["JoinDate"] = pd.to_datetime(df["JoinDate"])

    df["Age"] = curr_year - df["DOB"].dt.year
    df["YearOfService"] = curr_year - df["JoinDate"].dt.year

    df["Salary"] = df["Salary"].astype('float')

except KeyError as e:
    print(f"column not found: {e}")
except ValueError as e:
    print(f"conversion failed: {e}")
except Exception as e:
    print(f"Unknown exception occured: {e}")

#Load
try:
    # df.to_csv("Transformed.csv", index=False)
    pass

except Exception as e:
    print(f"Conversion to transformed.csv failed with an error: {e}")

transformed_df = pd.read_csv("transformed.csv")
print(transformed_df.head())
