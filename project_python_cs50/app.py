"""Restaurant manager GUI.

This script loads restaurant data, lets the user browse/filter restaurants,
edit restaurant details, and manage dishes for the currently selected restaurant.
The code is organised into sections so the main flow is easier to follow.
"""

import tkinter as tk
from tkinter import messagebox
import re
from project import *

restaurants = load_restaurants()
filtered_indices = []
selected_restaurant_index = None
selected_dish_index = None
current_filter_city = None


def main():
    root.mainloop()

# region Validation / Formatting


def format_title(text):
    """Clean up user text by trimming whitespace and capitalising each word."""
    return text.strip().title()


def valid_name_city(text):
    """Allow only letters, numbers, and spaces for restaurant/city names."""
    return re.fullmatch(r"[A-Za-z0-9 ]+", text) is not None


def valid_tel(text):
    """Validate telephone numbers using 8 to 15 digits."""
    return re.fullmatch(r"\d{8,15}", text) is not None


def valid_dish_text(text):
    """Allow only letters, numbers, and spaces for dish text fields."""
    return re.fullmatch(r"[A-Za-z0-9 ]+", text) is not None


# endregion

# region Helper Functions

def clear_restaurant_fields():
    name_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)
    tel_entry.delete(0, tk.END)
    rating_entry.delete(0, tk.END)


def clear_edit_restaurant_fields():
    edit_name_entry.delete(0, tk.END)
    edit_city_entry.delete(0, tk.END)
    edit_tel_entry.delete(0, tk.END)
    edit_rating_entry.delete(0, tk.END)


def clear_dish_fields():
    dish_name_entry.delete(0, tk.END)
    dish_type_entry.delete(0, tk.END)
    dish_price_entry.delete(0, tk.END)


def reset_dish_selection():
    global selected_dish_index
    selected_dish_index = None
    dish_listbox.selection_clear(0, tk.END)
    clear_dish_fields()
    dish_mode_label.config(text="Dish mode: Add new dish", fg="darkgreen")


def disable_dish_section():
    dish_name_entry.config(state="disabled")
    dish_type_entry.config(state="disabled")
    dish_price_entry.config(state="disabled")
    add_dish_btn.config(state="disabled")
    update_dish_btn.config(state="disabled")
    delete_dish_btn.config(state="disabled")
    reset_dish_btn.config(state="disabled")
    selected_label.config(text="Selected restaurant: None")
    dish_mode_label.config(text="Dish mode: Disabled", fg="grey")


def enable_dish_section(r):
    dish_name_entry.config(state="normal")
    dish_type_entry.config(state="normal")
    dish_price_entry.config(state="normal")
    add_dish_btn.config(state="normal")
    update_dish_btn.config(state="normal")
    delete_dish_btn.config(state="normal")
    reset_dish_btn.config(state="normal")
    selected_label.config(text=f"Selected restaurant: {r.name}")


def disable_edit_restaurant_section():
    edit_name_entry.config(state="disabled")
    edit_city_entry.config(state="disabled")
    edit_tel_entry.config(state="disabled")
    edit_rating_entry.config(state="disabled")
    update_restaurant_btn.config(state="disabled")
    reset_restaurant_btn.config(state="disabled")
    edit_selected_label.config(text="Editing: None", fg="grey")
    clear_edit_restaurant_fields()


def enable_edit_restaurant_section(r):
    edit_name_entry.config(state="normal")
    edit_city_entry.config(state="normal")
    edit_tel_entry.config(state="normal")
    edit_rating_entry.config(state="normal")
    update_restaurant_btn.config(state="normal")
    reset_restaurant_btn.config(state="normal")
    edit_selected_label.config(text=f"Editing: {r.name}", fg="blue")


def populate_edit_restaurant_fields(r):
    clear_edit_restaurant_fields()
    edit_name_entry.insert(0, r.name)
    edit_city_entry.insert(0, r.city)
    edit_tel_entry.insert(0, r.tel)
    edit_rating_entry.insert(0, str(r.rating))


def update_restaurant_details():
    """Refresh the details panel for the currently selected restaurant."""
    output.delete("1.0", tk.END)

    if selected_restaurant_index is None:
        return

    r = restaurants[selected_restaurant_index]

    output.insert(tk.END, f"{r.name} ({r.city})\n")
    output.insert(tk.END, f"Tel: {r.tel}\n")
    output.insert(tk.END, f"Rating: {r.rating}/5\n\n")
    output.insert(tk.END, "Dishes:\n")

    if not r.dishes:
        output.insert(tk.END, "  No dishes yet\n")
    else:
        for d in r.dishes:
            output.insert(tk.END, f" - {d.name} ({d.type}): ${d.price:.2f}\n")


def refresh_dish_list():
    """Reload the dish list for the selected restaurant."""
    dish_listbox.delete(0, tk.END)

    if selected_restaurant_index is None:
        return

    r = restaurants[selected_restaurant_index]

    for d in r.dishes:
        dish_listbox.insert(tk.END, f"{d.name} ({d.type}) - ${d.price:.2f}")


def select_restaurant_by_real_index(real_index):
    """
    Re-select a restaurant from the full data list after a filter or update.

    This keeps the GUI in sync when the restaurant list changes but the
    selected restaurant should still remain visible and highlighted.
    """
    global selected_restaurant_index

    if real_index in filtered_indices:
        list_index = filtered_indices.index(real_index)
        result_list.selection_clear(0, tk.END)
        result_list.selection_set(list_index)
        result_list.activate(list_index)
        result_list.see(list_index)
        selected_restaurant_index = real_index
        r = restaurants[real_index]
        enable_dish_section(r)
        enable_edit_restaurant_section(r)
        populate_edit_restaurant_fields(r)
        refresh_dish_list()
        update_restaurant_details()
    else:
        selected_restaurant_index = None
        result_list.selection_clear(0, tk.END)
        dish_listbox.delete(0, tk.END)
        output.delete("1.0", tk.END)
        disable_dish_section()
        disable_edit_restaurant_section()


def refresh_restaurant_list(filtered_city=None):
    """
    Rebuild the visible restaurant list using the current city filter.

    If a filter is provided, only restaurants from that city are shown.
    If the previously selected restaurant is still visible, it is reselected.
    """
    global filtered_indices
    global current_filter_city

    current_filter_city = filtered_city

    previous_selected = selected_restaurant_index

    result_list.delete(0, tk.END)
    filtered_indices = []

    for i, r in enumerate(restaurants):
        if filtered_city is None or r.city.lower() == filtered_city.lower():
            result_list.insert(tk.END, f"{r.name} ({r.city})")
            filtered_indices.append(i)

    if previous_selected is not None:
        select_restaurant_by_real_index(previous_selected)


# endregion

# region Restaurant Functions

def add_restaurant():
    """Validate and save a new restaurant from the add form."""
    if len(restaurants) >= MAX_RESTO:
        messagebox.showerror("Error", "Maximum number of restaurants reached.")
        return

    name = format_title(name_entry.get())
    city = format_title(city_entry.get())
    tel = tel_entry.get().strip()
    rating_raw = rating_entry.get().strip()

    if not name:
        messagebox.showerror("Error", "Restaurant name is required.")
        return

    if not valid_name_city(name):
        messagebox.showerror(
            "Error", "Restaurant name must contain letters, numbers and spaces only.")
        return

    if not city:
        messagebox.showerror("Error", "City is required.")
        return

    if not valid_name_city(city):
        messagebox.showerror("Error", "City must contain letters, numbers and spaces only.")
        return

    if not tel:
        messagebox.showerror("Error", "Telephone is required.")
        return

    if not valid_tel(tel):
        messagebox.showerror("Error", "Telephone must be 8 to 15 digits only.")
        return

    try:
        rating = int(rating_raw)
    except ValueError:
        messagebox.showerror("Error", "Rating must be a whole number from 1 to 5.")
        return

    if not (1 <= rating <= 5):
        messagebox.showerror("Error", "Rating must be between 1 and 5.")
        return

    for r in restaurants:
        if r.name == name and r.city == city and r.tel == tel:
            messagebox.showerror("Error", "That restaurant already exists.")
            return

    restaurants.append(Restaurant(name=name, city=city, tel=tel, rating=rating))
    save_restaurants(restaurants)
    refresh_restaurant_list(current_filter_city)
    clear_restaurant_fields()

    messagebox.showinfo("Success", f"Restaurant '{name}' added successfully.")


def update_selected_restaurant():
    """Update the currently selected restaurant using the edit form."""
    global selected_restaurant_index

    if selected_restaurant_index is None:
        messagebox.showerror("Error", "Select a restaurant first.")
        return

    name = format_title(edit_name_entry.get())
    city = format_title(edit_city_entry.get())
    tel = edit_tel_entry.get().strip()
    rating_raw = edit_rating_entry.get().strip()

    if not name:
        messagebox.showerror("Error", "Restaurant name is required.")
        return

    if not valid_name_city(name):
        messagebox.showerror(
            "Error", "Restaurant name must contain letters, numbers and spaces only.")
        return

    if not city:
        messagebox.showerror("Error", "City is required.")
        return

    if not valid_name_city(city):
        messagebox.showerror("Error", "City must contain letters, numbers and spaces only.")
        return

    if not tel:
        messagebox.showerror("Error", "Telephone is required.")
        return

    if not valid_tel(tel):
        messagebox.showerror("Error", "Telephone must be 8 to 15 digits only.")
        return

    try:
        rating = int(rating_raw)
    except ValueError:
        messagebox.showerror("Error", "Rating must be a whole number from 1 to 5.")
        return

    if not (1 <= rating <= 5):
        messagebox.showerror("Error", "Rating must be between 1 and 5.")
        return

    # Simple duplicate guard against another record
    for i, r in enumerate(restaurants):
        if i != selected_restaurant_index and r.name == name and r.city == city and r.tel == tel:
            messagebox.showerror(
                "Error", "Another restaurant with the same name, city, and tel already exists.")
            return

    r = restaurants[selected_restaurant_index]
    r.name = name
    r.city = city
    r.tel = tel
    r.rating = rating

    save_restaurants(restaurants)

    current_real_index = selected_restaurant_index
    refresh_restaurant_list(current_filter_city)
    select_restaurant_by_real_index(current_real_index)

    messagebox.showinfo("Success", f"Restaurant '{name}' updated successfully.")


def reset_edit_restaurant_form():
    if selected_restaurant_index is None:
        return
    r = restaurants[selected_restaurant_index]
    populate_edit_restaurant_fields(r)


def search_city():
    """Filter restaurants by a city name entered in the search box."""
    city = search_entry.get().strip()

    if city == "":
        refresh_restaurant_list()
        return

    city = format_title(city)

    if not valid_name_city(city):
        messagebox.showerror("Error", "City search must contain letters, numbers and spaces only.")
        return

    refresh_restaurant_list(filtered_city=city)


def clear_search():
    search_entry.delete(0, tk.END)
    refresh_restaurant_list()


def show_selected(event=None):
    global selected_restaurant_index

    try:
        list_index = result_list.curselection()[0]
    except IndexError:
        return

    real_index = filtered_indices[list_index]
    selected_restaurant_index = real_index

    r = restaurants[real_index]

    enable_dish_section(r)
    enable_edit_restaurant_section(r)
    populate_edit_restaurant_fields(r)

    reset_dish_selection()
    refresh_dish_list()
    update_restaurant_details()


def delete_restaurant():
    """Delete the selected restaurant and all of its dishes after confirmation."""
    global selected_restaurant_index, selected_dish_index

    if selected_restaurant_index is None:
        messagebox.showerror("Error", "Select a restaurant first.")
        return

    r = restaurants[selected_restaurant_index]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Delete restaurant '{r.name}' and all its dishes?"
    )
    if not confirm:
        return

    restaurants.pop(selected_restaurant_index)
    save_restaurants(restaurants)

    selected_restaurant_index = None
    selected_dish_index = None

    result_list.selection_clear(0, tk.END)
    dish_listbox.delete(0, tk.END)
    output.delete("1.0", tk.END)

    disable_dish_section()
    disable_edit_restaurant_section()

    refresh_restaurant_list(current_filter_city)

    messagebox.showinfo("Success", "Restaurant deleted.")


# endregion

# region Dish Functions

def on_dish_select(event=None):
    """Load the selected dish into the dish editing fields."""
    global selected_dish_index

    if selected_restaurant_index is None:
        return

    try:
        dish_index = dish_listbox.curselection()[0]
    except IndexError:
        return

    selected_dish_index = dish_index
    r = restaurants[selected_restaurant_index]
    d = r.dishes[dish_index]

    clear_dish_fields()
    dish_name_entry.insert(0, d.name)
    dish_type_entry.insert(0, d.type)
    dish_price_entry.insert(0, f"{d.price:.2f}")

    dish_mode_label.config(text=f"Dish mode: Editing '{d.name}'", fg="blue")


def add_dish():
    """Add a new dish to the currently selected restaurant."""
    if selected_restaurant_index is None:
        messagebox.showerror("Error", "Select a restaurant first.")
        return

    r = restaurants[selected_restaurant_index]

    if len(r.dishes) >= MAX_DISH:
        messagebox.showerror("Error", "Maximum number of dishes reached for this restaurant.")
        return

    name = format_title(dish_name_entry.get())
    dtype = format_title(dish_type_entry.get())
    price_raw = dish_price_entry.get().strip()

    if not name:
        messagebox.showerror("Error", "Dish name is required.")
        return

    if not valid_dish_text(name):
        messagebox.showerror("Error", "Dish name must contain letters, numbers and spaces only.")
        return

    if not dtype:
        messagebox.showerror("Error", "Dish type is required.")
        return

    if not valid_dish_text(dtype):
        messagebox.showerror("Error", "Dish type must contain letters, numbers and spaces only.")
        return

    try:
        price = float(price_raw)
    except ValueError:
        messagebox.showerror("Error", "Price must be a valid number.")
        return

    if price < 0:
        messagebox.showerror("Error", "Price cannot be negative.")
        return

    r.dishes.append(Menu(name=name, type=dtype, price=price))
    save_restaurants(restaurants)

    refresh_dish_list()
    update_restaurant_details()
    reset_dish_selection()

    messagebox.showinfo("Success", f"Dish '{name}' added to {r.name}.")


def update_selected_dish():
    """Save changes made to the selected dish."""
    if selected_restaurant_index is None:
        messagebox.showerror("Error", "Select a restaurant first.")
        return

    if selected_dish_index is None:
        messagebox.showerror("Error", "Select a dish first.")
        return

    r = restaurants[selected_restaurant_index]

    name = format_title(dish_name_entry.get())
    dtype = format_title(dish_type_entry.get())
    price_raw = dish_price_entry.get().strip()

    if not name:
        messagebox.showerror("Error", "Dish name is required.")
        return

    if not valid_dish_text(name):
        messagebox.showerror("Error", "Dish name must contain letters, numbers and spaces only.")
        return

    if not dtype:
        messagebox.showerror("Error", "Dish type is required.")
        return

    if not valid_dish_text(dtype):
        messagebox.showerror("Error", "Dish type must contain letters, numbers and spaces only.")
        return

    try:
        price = float(price_raw)
    except ValueError:
        messagebox.showerror("Error", "Price must be a valid number.")
        return

    if price < 0:
        messagebox.showerror("Error", "Price cannot be negative.")
        return

    r.dishes[selected_dish_index].name = name
    r.dishes[selected_dish_index].type = dtype
    r.dishes[selected_dish_index].price = price

    save_restaurants(restaurants)
    refresh_dish_list()
    update_restaurant_details()

    dish_listbox.selection_set(selected_dish_index)
    dish_listbox.activate(selected_dish_index)
    on_dish_select()

    messagebox.showinfo("Success", f"Dish updated to '{name}'.")


def delete_selected_dish():
    """Delete the currently selected dish after confirmation."""
    global selected_dish_index

    if selected_restaurant_index is None:
        messagebox.showerror("Error", "Select a restaurant first.")
        return

    if selected_dish_index is None:
        messagebox.showerror("Error", "Select a dish first.")
        return

    r = restaurants[selected_restaurant_index]
    d = r.dishes[selected_dish_index]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Delete dish '{d.name}'?"
    )
    if not confirm:
        return

    r.dishes.pop(selected_dish_index)
    save_restaurants(restaurants)

    refresh_dish_list()
    update_restaurant_details()
    reset_dish_selection()

    messagebox.showinfo("Success", f"Dish '{d.name}' deleted.")


# endregion

# region UI Setup

root = tk.Tk()
root.title("Botchog Restaurant Manager")

# ✅ Optimised default size (NOT maximised)
width = 1200
height = 750

# ✅ Center the window
root.update_idletasks()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = int((screen_width / 2) - (width / 2))
y = int((screen_height / 2) - (height / 2))

root.geometry(f"{width}x{height}+{x}+{y}")

# ✅ Allow resizing
root.minsize(980, 620)
root.resizable(True, True)


# Make root responsive
root.columnconfigure(0, weight=1, uniform="main")
root.columnconfigure(1, weight=1, uniform="main")
root.columnconfigure(2, weight=1, uniform="main")
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# ----- Add Restaurant Frame -----
add_frame = tk.LabelFrame(root, text="Add Restaurant", padx=10, pady=10)
add_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

add_frame.columnconfigure(0, weight=0)
add_frame.columnconfigure(1, weight=1)

tk.Label(add_frame, text="Name").grid(row=0, column=0, sticky="w", pady=4, padx=(0, 8))
tk.Label(add_frame, text="City").grid(row=1, column=0, sticky="w", pady=4, padx=(0, 8))
tk.Label(add_frame, text="Tel").grid(row=2, column=0, sticky="w", pady=4, padx=(0, 8))
tk.Label(add_frame, text="Rating (1-5)").grid(row=3, column=0, sticky="w", pady=4, padx=(0, 8))

name_entry = tk.Entry(add_frame)
city_entry = tk.Entry(add_frame)
tel_entry = tk.Entry(add_frame)
rating_entry = tk.Entry(add_frame)

name_entry.grid(row=0, column=1, sticky="ew", pady=4)
city_entry.grid(row=1, column=1, sticky="ew", pady=4)
tel_entry.grid(row=2, column=1, sticky="ew", pady=4)
rating_entry.grid(row=3, column=1, sticky="ew", pady=4)

tk.Button(add_frame, text="Add Restaurant", command=add_restaurant).grid(
    row=4, column=0, columnspan=2, sticky="ew", pady=(10, 0)
)

# ----- Edit Restaurant Frame -----
edit_frame = tk.LabelFrame(root, text="Edit Restaurant", padx=10, pady=10)
edit_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

edit_frame.columnconfigure(0, weight=0)
edit_frame.columnconfigure(1, weight=1)

edit_selected_label = tk.Label(edit_frame, text="Editing: None", fg="grey")
edit_selected_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

tk.Label(edit_frame, text="Name").grid(row=1, column=0, sticky="w", pady=4, padx=(0, 8))
tk.Label(edit_frame, text="City").grid(row=2, column=0, sticky="w", pady=4, padx=(0, 8))
tk.Label(edit_frame, text="Tel").grid(row=3, column=0, sticky="w", pady=4, padx=(0, 8))
tk.Label(edit_frame, text="Rating (1-5)").grid(row=4, column=0, sticky="w", pady=4, padx=(0, 8))

edit_name_entry = tk.Entry(edit_frame)
edit_city_entry = tk.Entry(edit_frame)
edit_tel_entry = tk.Entry(edit_frame)
edit_rating_entry = tk.Entry(edit_frame)

edit_name_entry.grid(row=1, column=1, sticky="ew", pady=4)
edit_city_entry.grid(row=2, column=1, sticky="ew", pady=4)
edit_tel_entry.grid(row=3, column=1, sticky="ew", pady=4)
edit_rating_entry.grid(row=4, column=1, sticky="ew", pady=4)

update_restaurant_btn = tk.Button(edit_frame, text="Update Restaurant",
                                  command=update_selected_restaurant)
update_restaurant_btn.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(10, 4))

reset_restaurant_btn = tk.Button(edit_frame, text="Reset Edit Form",
                                 command=reset_edit_restaurant_form)
reset_restaurant_btn.grid(row=6, column=0, columnspan=2, sticky="ew", pady=4)

disable_edit_restaurant_section()

# ----- Browse Restaurants Frame -----
search_frame = tk.LabelFrame(root, text="Browse Restaurants", padx=10, pady=10)
search_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

search_frame.columnconfigure(0, weight=1)
search_frame.columnconfigure(1, weight=1)
search_frame.rowconfigure(2, weight=1)

tk.Label(search_frame, text="Search by City").grid(row=0, column=0, sticky="w")
search_entry = tk.Entry(search_frame)
search_entry.grid(row=0, column=1, sticky="ew", padx=(6, 0))

tk.Button(search_frame, text="Search", command=search_city).grid(
    row=1, column=0, sticky="ew", pady=6, padx=(0, 6))
tk.Button(search_frame, text="Clear", command=clear_search).grid(
    row=1, column=1, sticky="ew", pady=6)

result_list = tk.Listbox(search_frame, exportselection=False)
result_list.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=6)
result_list.bind("<<ListboxSelect>>", show_selected)

resto_scroll = tk.Scrollbar(search_frame, orient="vertical", command=result_list.yview)
result_list.config(yscrollcommand=resto_scroll.set)
resto_scroll.grid(row=2, column=2, sticky="ns", pady=6, padx=(4, 0))

tk.Button(search_frame, text="Delete Restaurant", command=delete_restaurant).grid(
    row=3, column=0, columnspan=2, sticky="ew", pady=4
)

# ----- Restaurant Details Frame -----
details_frame = tk.LabelFrame(root, text="Restaurant Details", padx=10, pady=10)
details_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

details_frame.rowconfigure(0, weight=1)
details_frame.columnconfigure(0, weight=1)

output = tk.Text(details_frame, wrap="word")
output.grid(row=0, column=0, sticky="nsew")

output_scroll = tk.Scrollbar(details_frame, orient="vertical", command=output.yview)
output.config(yscrollcommand=output_scroll.set)
output_scroll.grid(row=0, column=1, sticky="ns")

# ----- Dish Editor Frame -----
dish_frame = tk.LabelFrame(root, text="Dish Editor", padx=10, pady=10)
dish_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="nsew")

dish_frame.columnconfigure(0, weight=0)
dish_frame.columnconfigure(1, weight=1)
dish_frame.rowconfigure(10, weight=1)

selected_label = tk.Label(dish_frame, text="Selected restaurant: None", fg="blue")
selected_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

dish_mode_label = tk.Label(dish_frame, text="Dish mode: Disabled", fg="grey")
dish_mode_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))

tk.Label(dish_frame, text="Dish Name").grid(row=2, column=0, sticky="w", pady=4, padx=(0, 8))
tk.Label(dish_frame, text="Type").grid(row=3, column=0, sticky="w", pady=4, padx=(0, 8))
tk.Label(dish_frame, text="Price").grid(row=4, column=0, sticky="w", pady=4, padx=(0, 8))

dish_name_entry = tk.Entry(dish_frame)
dish_type_entry = tk.Entry(dish_frame)
dish_price_entry = tk.Entry(dish_frame)

dish_name_entry.grid(row=2, column=1, sticky="ew", pady=4)
dish_type_entry.grid(row=3, column=1, sticky="ew", pady=4)
dish_price_entry.grid(row=4, column=1, sticky="ew", pady=4)

add_dish_btn = tk.Button(dish_frame, text="Add Dish", command=add_dish)
add_dish_btn.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(10, 4))

update_dish_btn = tk.Button(dish_frame, text="Update Selected Dish", command=update_selected_dish)
update_dish_btn.grid(row=6, column=0, columnspan=2, sticky="ew", pady=4)

delete_dish_btn = tk.Button(dish_frame, text="Delete Selected Dish", command=delete_selected_dish)
delete_dish_btn.grid(row=7, column=0, columnspan=2, sticky="ew", pady=4)

reset_dish_btn = tk.Button(dish_frame, text="Reset Dish Form", command=reset_dish_selection)
reset_dish_btn.grid(row=8, column=0, columnspan=2, sticky="ew", pady=4)

tk.Label(dish_frame, text="Dishes").grid(row=9, column=0, sticky="w", pady=(12, 4))

dish_listbox = tk.Listbox(dish_frame, exportselection=False)
dish_listbox.grid(row=10, column=0, columnspan=2, sticky="nsew", pady=4)
dish_listbox.bind("<<ListboxSelect>>", on_dish_select)

dish_scroll = tk.Scrollbar(dish_frame, orient="vertical", command=dish_listbox.yview)
dish_listbox.config(yscrollcommand=dish_scroll.set)
dish_scroll.grid(row=10, column=2, sticky="ns", pady=4, padx=(4, 0))

disable_dish_section()
refresh_restaurant_list()


if __name__ == "__main__":
    main()


# endregion
