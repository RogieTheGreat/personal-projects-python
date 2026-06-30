# ==========================================
# R DATA WRANGLING EXAMPLE
# ==========================================

library(dplyr)

# ------------------------------------------
# STEP 1 - IMPORT CSV
# ------------------------------------------

df <- read.csv("employee.csv")

cat("\nOriginal Data\n")
print(df)

# ------------------------------------------
# STEP 2 - VIEW DATA
# ------------------------------------------

cat("\nStructure\n")
str(df)

cat("\nColumn Names\n")
names(df)

# ------------------------------------------
# STEP 3 - RENAME COLUMN
# ------------------------------------------

df <- df %>%
  rename(
    ID = EmployeeID
  )

# ------------------------------------------
# STEP 4 - FILTER
# Hours greater than 40
# ------------------------------------------

filtered <- df %>%
  filter(Hours > 40)

cat("\nHours > 40\n")
print(filtered)

# ------------------------------------------
# STEP 5 - CREATE NEW COLUMN
# ------------------------------------------

filtered <- filtered %>%
  mutate(
    Overtime = Hours - 38
  )

cat("\nWith Overtime\n")
print(filtered)

# ------------------------------------------
# STEP 6 - GROUP AND SUMMARISE
# ------------------------------------------

summary <- filtered %>%
  group_by(Department) %>%
  summarise(
    Avg_Hours = mean(Hours),
    Max_Hours = max(Hours),
    Employee_Count = n()
  )

cat("\nDepartment Summary\n")
print(summary)

# ------------------------------------------
# STEP 7 - COMBINE COLUMNS
# ------------------------------------------

filtered <- filtered %>%
  mutate(
    Department_Shift =
      paste(
        Department,
        Shift,
        sep = "_"
      )
  )

cat("\nCombined Field\n")
print(
  filtered %>%
    select(
      Name,
      Department_Shift
    )
)

# ------------------------------------------
# STEP 8 - SORT
# ------------------------------------------

filtered <- filtered %>%
  arrange(desc(Hours))

cat("\nSorted\n")
print(filtered)

# ------------------------------------------
# STEP 9 - EXPORT
# ------------------------------------------

write.csv(
  filtered,
  "employee_filtered.csv",
  row.names = FALSE
)

write.csv(
  summary,
  "employee_summary.csv",
  row.names = FALSE
)

cat("\nFiles Exported\n")