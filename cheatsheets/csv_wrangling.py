# ============================================
# CSV WRANGLING CHEAT SHEET
# ============================================

import pandas as pd


# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------

"""
Import CSV
↓
Inspect Columns
↓
Rename Headers
↓
Clean Data
↓
Filter Data
↓
Add/Edit Columns
↓
Aggregate/Summarise
↓
Export CSV

"""


# --------------------------------------------------
# STEP 1 - IMPORT CSV
# --------------------------------------------------

df = pd.read_csv("employees.csv")

print(df.head())

# Example CSV:
#
# EmployeeID,FullName,Dept,Salary
# 1001,John Smith,Engineering,95000
# 1002,Mary Jones,Quality,85000
# 1003,David Lee,Engineering,100000


# --------------------------------------------------
# STEP 2 - VIEW STRUCTURE
# --------------------------------------------------

print(df.head())      # first 5 rows
print(df.tail())      # last 5 rows

print(df.info())      # column types

print(df.columns)

# Output:
#
# Index([
#   'EmployeeID',
#   'FullName',
#   'Dept',
#   'Salary'
# ])


# --------------------------------------------------
# STEP 3 - RENAME HEADERS
# --------------------------------------------------

df.rename(columns={
    "EmployeeID": "ID",
    "FullName": "Name",
    "Dept": "Department"
}, inplace=True)

print(df.columns)

# Output:
#
# Index([
#   'ID',
#   'Name',
#   'Department',
#   'Salary'
# ])


# --------------------------------------------------
# STEP 4 - VIEW SPECIFIC COLUMN
# --------------------------------------------------

print(df["Name"])

# Output:
#
# John Smith
# Mary Jones
# David Lee


# --------------------------------------------------
# STEP 5 - FILTER ROWS
# --------------------------------------------------

engineers = df[
    df["Department"] == "Engineering"
]

print(engineers)

# Output:
#
# ID  Name          Department  Salary
# 1001 John Smith   Engineering 95000
# 1003 David Lee    Engineering 100000


# --------------------------------------------------
# STEP 6 - FILTER MULTIPLE CONDITIONS
# --------------------------------------------------

high_paid = df[
    (df["Department"] == "Engineering") &
    (df["Salary"] > 90000)
]

print(high_paid)


# --------------------------------------------------
# STEP 7 - CREATE NEW COLUMN
# --------------------------------------------------

df["Bonus"] = df["Salary"] * 0.10

print(df)

# Output:
#
# Salary Bonus
# 95000  9500
# 85000  8500


# --------------------------------------------------
# STEP 8 - MODIFY EXISTING COLUMN
# --------------------------------------------------

df["Salary"] = df["Salary"] + 5000

print(df["Salary"])


# --------------------------------------------------
# STEP 9 - REPLACE VALUES
# --------------------------------------------------

df["Department"] = df[
    "Department"
].replace({
    "Eng": "Engineering",
    "QA": "Quality"
})

print(df["Department"])


# --------------------------------------------------
# STEP 10 - DROP COLUMN
# --------------------------------------------------

df.drop(columns=["Bonus"], inplace=True)


# --------------------------------------------------
# STEP 11 - SORT DATA
# --------------------------------------------------

df.sort_values(
    by="Salary",
    ascending=False,
    inplace=True
)

print(df)


# --------------------------------------------------
# STEP 12 - FIND MISSING DATA
# --------------------------------------------------

print(df.isna().sum())

# Output:
#
# ID            0
# Name          0
# Department    2
# Salary        1


# --------------------------------------------------
# STEP 13 - FILL MISSING DATA
# --------------------------------------------------

df["Department"] = df[
    "Department"
].fillna("Unknown")

df["Salary"] = df[
    "Salary"
].fillna(0)


# --------------------------------------------------
# STEP 14 - REMOVE DUPLICATES
# --------------------------------------------------

df.drop_duplicates(inplace=True)


# --------------------------------------------------
# STEP 15 - QUICK STATS
# --------------------------------------------------

print(df.describe())

# Output:
#
# mean salary
# min salary
# max salary
# std deviation


# --------------------------------------------------
# STEP 16 - GROUP DATA
# --------------------------------------------------

summary = df.groupby(
    "Department"
)["Salary"].mean()

print(summary)

# Output:
#
# Engineering 97500
# Quality     85000


# --------------------------------------------------
# STEP 17 - ROW COUNTS
# --------------------------------------------------

print(df.shape)

# Output:
#
# (100, 4)
#
# 100 rows
# 4 columns


# --------------------------------------------------
# STEP 18 - SAVE TO NEW CSV
# --------------------------------------------------

df.to_csv(
    "employees_clean.csv",
    index=False
)

print("Saved")


# --------------------------------------------------
# STEP 19 - SAVE FILTERED DATA
# --------------------------------------------------

engineers.to_csv(
    "engineering_only.csv",
    index=False
)


# --------------------------------------------------
# STEP 20 - FULL REAL-WORLD EXAMPLE
# --------------------------------------------------

df = pd.read_csv("employees.csv")

# Rename headers
df.rename(columns={
    "EmployeeID":"ID",
    "FullName":"Name",
    "Dept":"Department"
}, inplace=True)

# Remove duplicates
df.drop_duplicates(inplace=True)

# Fill blanks
df.fillna("Unknown", inplace=True)

# Add bonus
df["Bonus"] = df["Salary"] * 0.1

# Engineering only
filtered = df[
    df["Department"] == "Engineering"
]

# Export result
filtered.to_csv(
    "engineering_report.csv",
    index=False
)

print("Report created.")


"""

pd.read_csv()

df.head()

df.info()

df.columns

df.rename()

df.drop()

df.fillna()

df.groupby()

df.sort_values()

df.to_csv()

"""