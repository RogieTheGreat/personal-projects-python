# Python Core Cheatsheet 

Author: Rogie Bernabe
Purpose: Practical Python reference for automation, systems, and engineering work

```markdown

## 1. Basic Program Structure

```python

def main():
    print("Start program")

# Entry point of program

if __name__ == "__main__":
    main()

```markdown

## 2. Variables and Types

```python
# Variable store data

x = 10 # int
y = 3.14 # float
name = "Rogie" # string
flag = True # boolen

# check type 
print(type(x))

# List

```markdown

## 3. List

```python
# List = collection items

numbers = [1,2,3]

# add item

numbers.append(4)

#remove item

numbers.remove(2)

# Loop through list

for n in numbers:
    print(n)


# Note!!

# Dictionaries 

```markdown

## 4. Dictionaries

```python

# Dictionary = key-value pairs

person= {
    "name":"Rogie",
    "city":"Melbourne",
    "age": 25
}

# Access value
print(person["name"])

# Loop through dictionary

for key in person:
    print(key,person[key])

```markdown
## 5. File Handling

```python
# Writing to a file
with open("data.txt","w") as f:
    f.write("Hello World") 

# Reading from a file
with open("data.txt","r") as f:
    content = f.read()
    print(content)


```markdown
## 6. JSON Handling

```python
import json

data = {
    "name":"Rogie",
    "city":"Melbourne"
}

# Save JSON Handling
with open("data.json","w") as f:
    json.dump(data,f,indent=4)


# Load JSON Handling
with open("data.json","r") as f:
    data = json.load(f)
    print(data)
    

# Exception Handling (PREVENT CRASH)

```markdown

## 7. Exception Handling

```python

try:
    x = int("abc")
except ValueError:
    sys.exit("Invalid Input")


# Pattern Template

```markdown

## 8. Basic Program Pattern

```python 

def load_data()
    # load file or data soruce
    pass

def process_data(data)
    # perform calculation or filtering
    pass

def save_output(result)
    # save results to file
    pass

def main():
        data = load_data()
        result = process_data(data)
        save_output(result)

if __name__ == "__main__""
    main()