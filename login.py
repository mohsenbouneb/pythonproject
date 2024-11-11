import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import subprocess

# Function to log in the user
def login():
    username = entry_username.get()
    password = entry_password.get()

    # Hash the entered password to match the stored hash
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Connect to the database
    conn = sqlite3.connect("recrutement.db")
    cursor = conn.cursor()

    # Check if the user exists and the password matches
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Login", "Login successful!")
        root.destroy()  # Close the login window
        subprocess.Popen(["python", "interface.py"])  # Opens interface.py after successful login
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password.")

    # Close the database connection
    conn.close()

# Create the login window
root = tk.Tk()
root.title("Login")
root.geometry("300x300")

# Username label and entry
label_username = tk.Label(root, text="Username")
label_username.pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

# Password label and entry
label_password = tk.Label(root, text="Password")
label_password.pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

# Login button
btn_login = tk.Button(root, text="Login", command=login)
btn_login.pack(pady=10)


# Run the login interface
root.mainloop()
