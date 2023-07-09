from tkinter import *
from tkinter import messagebox
import random
import pyclip
import json
import os

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generator():
    """Generates a new random strong password"""
    password_entry.delete(0, END)

    password_letters = [random.choice(letters) for _ in range(random.randint(4, 8))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    generated_password = "".join(password_list)
    password_entry.insert(0, generated_password)


def copy_text():
    password = password_entry.get()
    pyclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    """Get the website and password and save them to a separate file."""
    website = website_entry.get().title()
    password = password_entry.get()
    username = username_entry.get()
    new_data = {
        website: {
            "Email/Username": username,
            "Password": password
        }
    }

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops...", message="Don\'t leave any field empty")
    else:
        try:
            with open("data.json", 'r') as data_file:
                data = json.load(data_file)
                data.update(new_data)
        except FileNotFoundError:
            with open("data.json", 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        except json.decoder.JSONDecodeError:
            with open("data.json", 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            with open("data.json", 'w') as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


def restore_data():
    delete = messagebox.askyesno(title="Restore Data", message="Are you sure? You want to delete all the passwords?")
    if delete:
        os.remove("data.json")

# ---------------------------- SEARCH PASSWORD ------------------------------- #


def search():
    website = website_entry.get().title()
    try:
        with open("data.json") as data_file:
            content = json.load(data_file)
            is_ok = messagebox.askyesno(title=website, message=f"Email/UserName :{content[website]['Email/Username']}"
                                                               f"\n Password :{content[website]['Password']}\n"
                                                               f"Do you want to copy the password?")
    except FileNotFoundError:
        messagebox.showwarning(title="oops", message=f"Sorry!  The data file not found!")
    except KeyError:
        messagebox.showwarning(title="oops", message=f"No details for {website} exists!")
    else:
        if is_ok:
            pyclip.copy(content[website]['Password'])

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Generator")
window.config(padx=50, pady=50, bg="#FCD2D1")

# Canvas
canvas = Canvas(width=200, height=200, bg="#FCD2D1", highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=1, column=2)

# Labels
website_label = Label(text="Website :", font=("Comic Sans MS", 10, "bold"), fg="#FF5C58", bg="#FCD2D1")
website_label.grid(row=2, column=1)
website_label.config(padx=10, pady=10)

user_label = Label(text="Email/UserName :", font=("Comic Sans MS", 10, "bold"), fg="#FF5C58", bg="#FCD2D1")
user_label.grid(row=3, column=1)
user_label.config(padx=10, pady=10)

password_label = Label(text="Password :", font=("Comic Sans MS", 10, "bold"), fg="#FF5C58", bg="#FCD2D1")
password_label.grid(row=4, column=1)
password_label.config(padx=10, pady=10)

# Entries
website_entry = Entry(width=35, bg="#FFEDD3")
website_entry.grid(row=2, column=2, columnspan=2)
website_entry.focus()

username_entry = Entry(width=56, bg="#FFEDD3")
username_entry.grid(row=3, column=2, columnspan=3)
username_entry.insert(0, "mhdhassimcr717@gmail.com")

password_entry = Entry(width=31, bg="#FFEDD3")
password_entry.grid(row=4, column=2)

# Buttons
generator_button = Button(text="Generate Password", bd=1, command=generator, font=("Times", 10, "normal"), bg="#FF5C58",
                          fg="white", width=15)
generator_button.grid(row=4, column=4, padx=5, pady=5)

add_button = Button(text="Add", bd=1, width=49, command=save, font=("Times", 10, "normal"), bg="#FF5C58", fg="white")
add_button.grid(row=5, column=2, columnspan=3, pady=10)

search_button = Button(text="Search", bd=1, font=("Times", 10, "normal"), bg="#FF5C58", fg="white", width=15,
                       command=search)
search_button.grid(row=2, column=4, padx=5)

copy_button = Button(text="📋", command=copy_text, bg="#FF5C58", fg="#F8F0DF", bd=1)
copy_button.grid(row=4, column=3, padx=5, pady=5)

reset_button = Button(text="Restore", bg="#FF5C58", fg="#F8F0DF", bd=0, command=restore_data, font=("Times", 8,))
reset_button.grid(row=0, column=5)

window.mainloop()
