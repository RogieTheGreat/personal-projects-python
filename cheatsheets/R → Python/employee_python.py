# ==========================================
# PYTHON DATA WRANGLING EXAMPLE
# ==========================================

import pandas as pd

# ------------------------------------------
# STEP 1 - IMPORT CSV
# ------------------------------------------

df = pd.read_csv("employee.csv")

print("\nOriginal Data")
print(df)

# ------------------------------------------
# STEP 2 - VIEW DATA
# ------------------------------------------

print("\nColumn Names")
print(df.columns)

print("\nData Info")
print(df.info())

# ------------------------------------------
# STEP 3 - RENAME COLUMN
# ------------------------------------------

df = df.rename(columns={
    "EmployeeID": "ID"
})

# ------------------------------------------
# STEP 4 - FILTER
# Hours greater than 40
# ------------------------------------------

filtered = df.query("Hours > 40")

print("\nHours > 40")
print(filtered)

# ------------------------------------------
# STEP 5 - CREATE NEW COLUMN
# Overtime based on 38 hour week
# ------------------------------------------

filtered = filtered.assign(
    Overtime=lambda d: d["Hours"] - 38
)

print("\nWith Overtime")
print(filtered)

# ------------------------------------------
# STEP 6 - GROUP AND SUMMARISE
# ------------------------------------------

summary = (

    filtered

      .groupby("Department")

      .agg(
          Avg_Hours=("Hours", "mean"),
          Max_Hours=("Hours", "max"),
          Employee_Count=("ID", "count")
      )

      .reset_index()

)

print("\nDepartment Summary")
print(summary)

# ------------------------------------------
# STEP 7 - COMBINE COLUMNS
# Similar to mutate(paste())
# ------------------------------------------

filtered["Department_Shift"] = (
    filtered["Department"]
    + "_"
    + filtered["Shift"]
)

print("\nCombined Field")
print(filtered[
    ["Name", "Department_Shift"]
])

# ------------------------------------------
# STEP 8 - SORT
# Highest hours first
# ------------------------------------------

filtered = filtered.sort_values(
    "Hours",
    ascending=False
)

print("\nSorted")
print(filtered)

# ------------------------------------------
# STEP 9 - EXPORT
# ------------------------------------------

filtered.to_csv(
    "employee_filtered.csv",
    index=False
)

summary.to_csv(
    "employee_summary.csv",
    index=False
)

print("\nFiles Exported")
print("employee_filtered.csv")
print("employee_summary.csv")