# 🐍 Python Core Cheatsheet (Engineering Focus)

**Author:** Rogie Bernabe  
**Purpose:** Practical Python reference for automation, systems, and engineering work  

---

## 🧠 1. Basic Program Structure

```python
def main():
    print("Start program")

# Entry point of program
if __name__ == "__main__":
    main()
```

- Always use this structure  
- Keeps code organised and testable  

---

## 🧠 2. Variables and Types

```python
# Variables store data

x = 10          # int
y = 3.14        # float
name = "Rogie"  # string
flag = True     # boolean

# check type
print(type(x))
```

- Python is dynamically typed  
- No need to declare types explicitly  

---

## 🧠 3. Lists

```python
# List = collection of items

numbers = [1, 2, 3]

# add item
numbers.append(4)

# remove item
numbers.remove(2)

# loop through list
for n in numbers:
    print(n)
```

- Used for storing multiple values  
- Very common in data processing  

---

## 🧠 4. Dictionaries

```python
# Dictionary = key-value pairs

person = {
    "name": "Rogie",
    "city": "Melbourne",
    "age": 25
}

# access value
print(person["name"])

# loop through dictionary
for key in person:
    print(key, person[key])
```

- Represents structured real-world data  
- Similar to JSON  

---

## 🧠 5. File Handling

```python
# Writing to a file
with open("data.txt", "w") as f:
    f.write("Hello World")

# Reading from a file
with open("data.txt", "r") as f:
    content = f.read()
    print(content)
```

- `"w"` = write (overwrite)  
- `"r"` = read  
- `with open()` auto-closes file  

---

## 🧠 6. JSON Handling

```python
import json

data = {
    "name": "Rogie",
    "city": "Melbourne"
}

# Save JSON
with open("data.json", "w") as f:
    json.dump(data, f, indent=4)

# Load JSON
with open("data.json", "r") as f:
    data = json.load(f)
    print(data)
```

- JSON = standard data format  
- Used in APIs and automation systems  

---

## 🧠 7. Exception Handling

```python
import sys

try:
    x = int("abc")
except ValueError:
    sys.exit("Invalid input")
```

Prevents crashes  
Essential for user input and file handling  

---

## 🧠 8. Basic Program Pattern

```python
def load_data():
    # load file or data source
    pass

def process_data(data):
    # perform calculations or filtering
    pass

def save_output(result):
    # save results
    pass

def main():
    data = load_data()
    result = process_data(data)
    save_output(result)

if __name__ == "__main__":
    main()
```

Standard real-world program structure  
Used in automation and system workflows  

---

## Key Notes

- Always separate **Markdown (text)** and **Python (code blocks)**  
- Every code block must start and end with ```  
- Use preview (`Ctrl + Shift + V`) to check formatting  

---

##  What This Is For

This cheatsheet is designed to help:

- Build automation tools  
- Process engineering data  
- Structure Python programs properly  
- Serve as a quick reference during coding  

---
