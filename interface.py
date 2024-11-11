import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import hashlib
import matplotlib.pyplot as plt
# Initialize the main application window
root = tk.Tk()
root.title("Admin Tools")
root.geometry("1000x800")

# Create a display frame to show different views
display_frame = tk.Frame(root)
display_frame.pack(fill="both", expand=True)
def show_about():
    messagebox.showinfo("ABOUT", "Cette application de gestion de recrutement aide à simplifier le processus de recrutement en permettant aux utilisateurs d'ajouter, d'évaluer et de gérer efficacement les candidats. Les utilisateurs peuvent saisir les informations des candidats, calculer des scores basés sur des critères clés, et suivre les performances globales. Conçue pour soutenir les équipes de recrutement, cette application offre une interface simple pour maintenir une base de données de candidats et visualiser les scores d’évaluation")
def show_help():
    messagebox.showinfo("HELP", "Pour utiliser l'application, commencez par entrer les informations d'un candidat, puis cliquez sur 'Ajouter Candidat'. Vous pouvez modifier les détails en sélectionnant un candidat et en utilisant le bouton 'Modifier Candidat'. Pour visualiser les scores des candidats dans un graphique, allez dans le menu 'Outils' et sélectionnez 'Afficher Graphique'. Pour vous déconnecter ou accéder à d'autres options administratives, explorez le menu 'Outils'. En cas de problème, assurez-vous que tous les champs sont correctement remplis ou contactez le support")

def afficher_graphique():
    # Clear the display area first
    for widget in display_frame.winfo_children():
        widget.destroy()
    
    # Connect to the database and retrieve data
    conn = sqlite3.connect("recrutement.db")
    df = pd.read_sql_query("SELECT nom, score FROM candidats", conn)
    conn.close()

    # Create a matplotlib figure and plot the data
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(df["nom"], df["score"], color="skyblue")
    ax.set_xlabel("Candidats")
    ax.set_ylabel("Score")
    ax.set_title("Évaluation des Candidats")

    # Embed the figure in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=display_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=False)

def show_admins():
    for widget in display_frame.winfo_children():
        widget.destroy()
    conn = sqlite3.connect("recrutement.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users")
    admins = cursor.fetchall()
    conn.close()
    
    tree = ttk.Treeview(display_frame, columns=("ID", "Username"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Username", text="Username")
    
    for admin in admins:
        tree.insert("", tk.END, values=admin)
    
    tree.pack(fill="both", expand=True)

def add_admin():
    for widget in display_frame.winfo_children():
        widget.destroy()
    
    label_add = tk.Label(display_frame, text="Add a new admin", font=("Arial", 12))
    label_add.pack(pady=10)

    label_new_username = tk.Label(display_frame, text="New Username")
    label_new_username.pack(pady=5)
    entry_new_username = tk.Entry(display_frame)
    entry_new_username.pack(pady=5)

    label_new_password = tk.Label(display_frame, text="New Password")
    label_new_password.pack(pady=5)
    entry_new_password = tk.Entry(display_frame, show="*")
    entry_new_password.pack(pady=5)

    def save_user():
        new_username = entry_new_username.get()
        new_password = entry_new_password.get()
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

        conn = sqlite3.connect("recrutement.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, hashed_password))
            conn.commit()
            messagebox.showinfo("Registration", "User registered successfully!")
            show_admins()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
        finally:
            conn.close()

    btn_save = tk.Button(display_frame, text="Save Admin", command=save_user)
    btn_save.pack(pady=20)

def delete_admin():
    for widget in display_frame.winfo_children():
        widget.destroy()
    
    label_delete = tk.Label(display_frame, text="Enter Admin ID to Delete", font=("Arial", 12))
    label_delete.pack(pady=10)

    entry_id = tk.Entry(display_frame)
    entry_id.pack(pady=5)

    def confirm_delete():
        admin_id = entry_id.get()
        conn = sqlite3.connect("recrutement.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (admin_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Delete Admin", f"Admin with ID {admin_id} deleted successfully.")
        show_admins()

    btn_delete = tk.Button(display_frame, text="Delete Admin", command=confirm_delete)
    btn_delete.pack(pady=20)

def ajouter_candidat():
    for widget in display_frame.winfo_children():
        widget.destroy()

    label = tk.Label(display_frame, text="Ajouter un Candidat", font=("Arial", 12))
    label.pack(pady=10)

    entries = {}
    fields = ["Nom", "Experience", "Diplome", "Competences Techniques", "Qualites Humaines", "Mobilite"]
    for i, field in enumerate(fields):
        label_field = tk.Label(display_frame, text=field)
        label_field.pack()
        entry_field = tk.Entry(display_frame)
        entry_field.pack(pady=5)
        entries[field] = entry_field

    def save_candidat():
        data = {field: entries[field].get() for field in fields}
        data = {k: int(v) if v.isdigit() else v for k, v in data.items()}

        conn = sqlite3.connect("recrutement.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO candidats (nom, experience, diplome, competences_techniques, qualites_humaines, mobilite, score, categorie)
            VALUES (?, ?, ?, ?, ?, ?, 0, "")
        ''', (data["Nom"], data["Experience"], data["Diplome"], data["Competences Techniques"], data["Qualites Humaines"], data["Mobilite"]))
        conn.commit()
        conn.close()
        messagebox.showinfo("Succès", f"Candidat {data['Nom']} ajouté avec succès!")

    btn_save = tk.Button(display_frame, text="Save Candidat", command=save_candidat)
    btn_save.pack(pady=20)

def afficher_candidats():
    for widget in display_frame.winfo_children():
        widget.destroy()

    conn = sqlite3.connect("recrutement.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidats")
    rows = cursor.fetchall()
    conn.close()

    tree = ttk.Treeview(display_frame, columns=("ID", "Nom", "Expérience", "Diplôme", "Compétences", "Qualités", "Mobilité", "Score", "Catégorie"), show="headings")
    headers = ["ID", "Nom", "Expérience", "Diplôme", "Compétences", "Qualités", "Mobilité", "Score", "Catégorie"]
    for header in headers:
        tree.heading(header, text=header)

    for row in rows:
        tree.insert("", tk.END, values=row)
    
    tree.pack(fill="both", expand=True)
def logout():
    root.destroy()
    subprocess.Popen(["python", "login.py"])

menu_bar = tk.Menu(root)
tools_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="USERS", menu=tools_menu)
tools_menu.add_command(label="Afficher Admins", command=show_admins)
tools_menu.add_command(label="Ajouter Admins", command=add_admin)
tools_menu.add_command(label="Supprimer Admins", command=delete_admin)

candidature_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="CANDIDATURE", menu=candidature_menu)
candidature_menu.add_command(label="Ajouter Candidat", command=ajouter_candidat)
candidature_menu.add_command(label="Supprimer Candidat", command=delete_admin)  # Assuming deletion based on ID
candidature_menu.add_command(label="Afficher Candidats", command=afficher_candidats)


graph_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="GRAPH", menu=graph_menu)
graph_menu.add_command(label="Affichage Graphique", command=afficher_graphique)

help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="HELP", menu=help_menu)
help_menu.add_command(label="HELP", command=show_help)
help_menu.add_command(label="ABOUT", command=show_about)

logout_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="LOGOUT", menu=logout_menu)
logout_menu.add_command(label="DECONNEXION", command=logout)

root.config(menu=menu_bar)
root.mainloop()
