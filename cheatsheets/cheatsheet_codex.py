# ==========================================
# PYTHON CHEAT SHEET (WITH EXAMPLES)
# ==========================================

# ---------- VARIABLES ----------

name = "Rogie"
age = 30

print(name)
# Rogie

print(type(age))
# <class 'int'>


# ---------- LISTS ----------

numbers = [10, 20, 30, 40, 50]

print(numbers[0])
# 10

print(numbers[-1])
# 50

print(numbers[1:4])
# [20, 30, 40]

numbers.append(60)

print(numbers)
# [10, 20, 30, 40, 50, 60]


# ---------- LIST COMPREHENSION ----------

squares = [x**2 for x in range(5)]

print(squares)
# [0, 1, 4, 9, 16]


# ---------- DICTIONARIES ----------

person = {
    "name": "Rogie",
    "role": "System Engineer"
}

print(person["name"])
# Rogie

print(person.get("role"))
# System Engineer

for key, value in person.items():
    print(key, value)

# name Rogie
# role System Engineer


# ---------- IF STATEMENTS ----------

temperature = 32

if temperature > 30:
    print("Hot")
else:
    print("Cold")

# Hot

status = "Pass" if 75 >= 50 else "Fail"

print(status)
# Pass


# ---------- FOR LOOPS ----------

for i in range(3):
    print(i)

# 0
# 1
# 2


# ---------- ENUMERATE ----------

fruits = ["Apple", "Orange", "Banana"]

for idx, fruit in enumerate(fruits):
    print(idx, fruit)

# 0 Apple
# 1 Orange
# 2 Banana


# ---------- ZIP ----------

names = ["John", "Mary"]
scores = [85, 92]

for name, score in zip(names, scores):
    print(name, score)

# John 85
# Mary 92


# ---------- FUNCTIONS ----------

def add(a, b):
    return a + b

print(add(10, 5))
# 15


# ---------- F-STRINGS ----------

name = "Rogie"

print(f"Hello {name}")
# Hello Rogie


# ---------- COMMON STRING METHODS ----------

text = " hello world "

print(text.strip())
# hello world

print(text.upper())
# HELLO WORLD

print(text.replace("world", "python"))
# hello python


# ---------- EXCEPTION HANDLING ----------

try:
    result = 10 / 0

except Exception as e:
    print(e)

# division by zero


# ---------- FILES ----------

with open("sample.txt", "w") as file:
    file.write("Hello")

print("File Saved")

# File Saved


# ---------- DATETIME ----------

from datetime import datetime

now = datetime.now()

print(now)

# 2026-06-30 16:00:00.xxx
# (example output)


# ---------- PATHLIB ----------

from pathlib import Path

print(Path("sample.txt").exists())

# True


# ---------- NUMPY ----------

import numpy as np

arr = np.array([10, 20, 30])

print(arr + 5)

# [15 25 35]

print(np.mean(arr))

# 20.0


# ---------- PANDAS ----------

import pandas as pd

df = pd.DataFrame({
    "Name": ["John", "Mary"],
    "Age": [25, 30]
})

print(df)

#   Name  Age
# 0 John   25
# 1 Mary   30

print(df["Age"].mean())

# 27.5


# ---------- FILTER DATA ----------

adults = df[df["Age"] >= 30]

print(adults)

#   Name  Age
# 1 Mary   30


# ---------- SORTING ----------

numbers = [5, 2, 8, 1]

print(sorted(numbers))

# [1, 2, 5, 8]

print(sorted(numbers, reverse=True))

# [8, 5, 2, 1]


# ---------- MATPLOTLIB ----------

import matplotlib.pyplot as plt

x = [1, 2, 3]
y = [10, 20, 30]

plt.plot(x, y)
plt.title("Sales")
plt.show()

# Produces:
#
#      *
#    *
#  *
#
# Upward trend chart


# ---------- MOST USEFUL ONE-LINERS ----------

len([1,2,3])
# 3

sum([1,2,3])
# 6

max([1,2,3])
# 3

min([1,2,3])
# 1

round(3.14159, 2)
# 3.14


# ---------- MAIN PROGRAM ----------

def main():
    print("Starting Program")

if __name__ == "__main__":
    main()

# Starting Program


# ==========================================
# TOP 20 COMMANDS YOU'LL USE DAILY
# ==========================================
#
# print()
# type()
# len()
# range()
# enumerate()
# zip()
# sorted()
# sum()
# max()
# min()
# f"..."
# .append()
# .split()
# .replace()
# datetime.now()
# Path().exists()
# try/except
# pd.read_csv()
# df.head()
# plt.plot()
#
# ==========================================