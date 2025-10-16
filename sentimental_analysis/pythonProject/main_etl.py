import pandas as pd
import sqlite3

# Extract
df = pd.read_csv("employee.csv")

# Transform
# Increasing IT dept salary by 10%
df['name'] = df['name'].str.upper()
df.loc[df['department'] == 'IT', 'salary'] *= 1.10

# Adding a bonus of 5% to all employees and adding bonus column to the dataframe
df['bonus'] = df['salary'] * 0.05

print(df)

#Load
conn = sqlite3.connect("employee.db")
df.to_sql("employee", conn, if_exists="replace", index = False)

print("\n"
      "The employee table database is loaded")

database = pd.read_sql("SELECT * from employee", conn)
print(database)
conn.close()