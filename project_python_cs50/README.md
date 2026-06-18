# Botchog Restaurant Manager (Python GUI)

Video Demo: https://youtu.be/aU8kw1byBfE

Name: Rogie Bernabe
GitHub: RogieTheGreat
Location: Melbourne, Australia
Date: 2026

---

## About

This project is a Restaurant Management System developed in Python.
It is a continuation and improvement of my earlier version written in C (terminal-based). The original version focused on basic CRUD operations in a command-line interface, while this version enhances usability by introducing a graphical user interface (GUI) using Tkinter.

The goal of this project was to transform a simple program into a more user-friendly and structured application, while also practising Python programming concepts and GUI development.

---

## What it does

The system allows users to:

- Add restaurants
- Edit restaurant information
- Delete restaurants
- Search restaurants by city
- Add, edit, and delete dishes
- View full restaurant details including menu items

Each restaurant can store multiple dishes, and users can easily navigate between restaurant selection and dish management.

All data is saved locally using a file (`data.pkl`) and also exported into a JSON format (`data.json`) for readability.

---

## Why I made it

I created this project to:

- Practice converting a program from C to Python
- Learn GUI development using Tkinter
- Improve user experience compared to a terminal program
- Handle real-world input with validation
- Build a structured CRUD-based application

This project helped me understand how to design a system beyond simple scripts and move toward real application development.

---

## How it works

The system is built using Python dataclasses to represent structured data.

### Each Restaurant contains:
- Name
- City
- Telephone number
- Rating
- A list of dishes (maximum of 7)

### Each Dish contains:
- Name
- Type
- Price

The application allows the user to select a restaurant first, and then perform operations on its associated dishes.

Data persistence is implemented using:
- `pickle` → to store Python objects directly
- `json` → to export data into a readable format

---

## Design Choices

- **Dataclasses** were used to organise restaurant and menu data for clarity and scalability
- **Pickle** was chosen for saving/loading objects without manual parsing
- **JSON export** was added for transparency and easier debugging
- **Modular functions** were implemented to separate logic from the user interface
- The GUI (`app.py`) is separated from core logic (`project.py`) to follow better software structure

Validation functions were introduced (e.g., phone number and name formatting) to ensure data integrity.

---

## What I learned

While developing this project, I learned:

- Synchronising GUI elements with underlying data
- Implementing validation logic using Python
- Building a CRUD system from scratch
- Improving UX (selection handling, editing, flow)
- Converting logic from C into Python
- Structuring code into reusable and testable functions

---

## Limitations

- Data is stored locally (no database or cloud storage)
- Fixed limits (30 restaurants, 7 dishes per restaurant)
- UI is basic and not styled beyond Tkinter defaults

---

## Future Improvements

- Improve UI design (possibly using web frameworks like Flask)
- Replace pickle with a proper database (e.g., SQLite)
- Add sorting and filtering features
- Enable multi-user or online functionality

---

## How to Run

Run core program:
