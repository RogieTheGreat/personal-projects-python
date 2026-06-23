"""
lists_and_dicts_notes.py

Purpose:
- Learn Python list and dict properly
- Written:- Written for R / MATLAB background
- list  = many things
- dict  = one thing (described)
- table = list of dicts
"""

# =====================================================
# 1. LIST BASICS
# =====================================================

# A list is an ordered collection of items
nums = [1, 2, 3]
names = ["Rogie", "Name2", "Name3"]
mixed = [1, "a", True, 3.14]

print("nums:", nums)
print("names:", names)
print("mixed:", mixed)

# Indexing (starts at 0)
print("first name:", names[0])
print("last name:", names[-1])

# -----------------------------------------------------
# Modifying lists
# -----------------------------------------------------

nums.append(4)                 # add ONE item
nums.extend([5, 6])             # add MANY items
nums.remove(2)                  # remove by value
last_item = nums.pop()          # remove last item

print("modified nums:", nums)
print("popped item:", last_item)

# ⚠️ append vs extend
example = []
example.append([1, 2])          # [[1, 2]]
example.extend([3, 4])          # [[1, 2], 3, 4]
print("append vs extend:", example)

# -----------------------------------------------------
# Looping over a list (BEST PRACTICE)
# -----------------------------------------------------

for name in names:
    print("Name:", name)

# Avoid index-based loops unless needed
# for i in range(len(names)):  # usually unnecessary


# =====================================================
# 2. DICT BASICS
# =====================================================

# A dict maps key -> value
person = {
    "name": "Rogie",
    "age": 30,
    "engineer": True
}

print("\nperson dict:", person)

# Accessing values
print("name:", person["name"])
print("age:", person.get("age"))

# Safe access with default
print("salary:", person.get("salary", "Not provided"))

# -----------------------------------------------------
# Modifying dicts
# -----------------------------------------------------

person["age"] = 31
person["city"] = "Melbourne"

print("updated person:", person)

# -----------------------------------------------------
# Looping over dicts (IMPORTANT)
# -----------------------------------------------------

for key, value in person.items():
    print(key, "->", value)


# =====================================================
# 3. LIST vs DICT (WHEN TO USE WHAT)
# =====================================================

"""
Use a list when:
- You have many values
- Order matters
- Items are similar

Use a dict when:
- You want to name values
- You describe one object
"""

# BAD: using list for named data
bad_person = ["Rogie", 30, True]

# GOOD: using dict for named data
good_person = {
    "name": "Rogie",
    "age": 30,
    "engineer": True
}


# =====================================================
# 4. LIST OF DICTS (TABLE / DATABASE THINKING)
# =====================================================

# Each dict = one row
# The list = the table

people = [
    {"name": "Rogie", "age": 30, "engineer": True},
    {"name": "Name2", "age": 25, "engineer": False},
    {"name": "Name3", "age": 15, "engineer": False},
]

print("\npeople table:")
for p in people:
    print(p["name"], p["age"], p["engineer"])

# Accessing rows
first_person = people[0]
print("first person name:", first_person["name"])


# =====================================================
# 5. DICT OF LISTS (COLUMN-ORIENTED, R-LIKE)
# =====================================================

people_columns = {
    "name": ["Rogie", "Name2", "Name3"],
    "age": [30, 25, 15],
    "engineer": [True, False, False],
}

print("\ncolumn-oriented access:")
print("ages:", people_columns["age"])
print("second age:", people_columns["age"][1])

# ⚠️ All lists must stay same length


# =====================================================
# 6. CONVERTING BETWEEN STRUCTURES
# =====================================================

# Dict of lists -> List of dicts
people_rows = [
    {"name": n, "age": a, "engineer": e}
    for n, a, e in zip(
        people_columns["name"],
        people_columns["age"],
        people_columns["engineer"]
    )
]

print("\nconverted to rows:")
for p in people_rows:
    print(p)

# List of dicts -> Dict of lists
people_columns_again = {
    "name": [p["name"] for p in people],
    "age": [p["age"] for p in people],
    "engineer": [p["engineer"] for p in people],
}

print("\nconverted back to columns:", people_columns_again)


# =====================================================
# 7. COMMON MISTAKES (READ THIS)
# =====================================================

"""
❌ Using list indexes instead of dict keys
❌ Treating dict like a table
❌ Forgetting .get() defaults
❌ Using append() instead of extend()
"""

# ✅ BEST PRACTICE SUMMARY
"""
- list           -> many things
- dict           -> describe one thing
- list of dicts  -> table / database rows
- dict of lists  -> column-based data
"""

print("\n✅ End of lists_and_dicts_notes.py")
# - Focus on data structures, not math

