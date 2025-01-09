import csv
import hashlib
import requests
import string
import random
from tri_b import produits_trie
from logging_log import creer_compte, connection, ajout_prod, mdp_compromis
import pandas as pd
from commercants import filtre_nom
import tkinter as tk
from tkinter import messagebox


is_logged_in = False
logged_user = None

def genere_salage(lenght=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=lenght))

def register(email_entry, password_entry, password2_entry, result_label):
    email = email_entry.get()
    password = password_entry.get()
    password2 = password2_entry.get()

    if password == password2:
        salt = genere_salage()
        pw_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix = pw_hash[:5]
        suffix = pw_hash[5:]

        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError(f"Error: {response.status_code}")

        found = False
        hashes = (line.split(':') for line in response.text.splitlines())
        for returned_suffix, count in hashes:
            if returned_suffix == suffix:
                result_label.config(text=f"Mot de passe trop peu sécurisé ! Il a été compromis {count} fois.\nVeuillez mettre un mot de passe plus sécurisé.")
                mdp_compromis()
                return

        with open("users.csv", mode="a", encoding='utf-8', newline="") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow([email, pw_hash, salt])
            creer_compte(email)

        result_label.config(text="Votre compte a été créé avec succès !")
        messagebox.showinfo("Succès", "Votre compte a été créé avec succès !")

    else:
        result_label.config(text="Les mots de passes ne correspondent pas. Veuillez réessayer.")
        messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas. Veuillez réessayer.")

def login(email_entry, password_entry, result_label):

    global is_logged_in, logged_user

    email = email_entry.get()
    password = password_entry.get()

    with open("users.csv", mode="r", encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            reg_name = row[0]
            reg_pass = row[1]
            pw_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            if pw_hash == reg_pass and email == reg_name:
                logged_user = email
                is_logged_in = True
                result_label.config(text=f"Bienvenue {email}")
                messagebox.showinfo("Connexion réussie", f"Bienvenue {email}")
                return

    result_label.config(text="Les informations que vous avez rentrées sont incorrectes !")
    messagebox.showerror("Erreur", "Les informations que vous avez rentrées sont incorrectes !")



def show_main_menu():
    main_menu_window = tk.Toplevel()
    main_menu_window.title("Menu Principal")
    main_menu_window.geometry("350x250")

    def afficher_produits():
        show_prod = tk.Tk()
        show_prod.title("Produits")
        show_prod.geometry("450x250")

        text_area = tk.Text(show_prod, height=15, width=50)
        text_area.pack(padx=10, pady=10)

        with open('produits.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            produits = []
            for row in reader:
                produits.append (f" {row['nom']}: {row['produit']}: {row['quantite']} en stock, Prix = {row['prix']} €")
        
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, "\n".join(produits))


            
    def ajouter_produit():
        def save_product():
            nom = nom_entry.get()
            produit = produit_entry.get()
            quantite = quantite_entry.get()
            prix = prix_entry.get()
            with open('produits.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([nom, produit, quantite, prix])
            messagebox.showinfo("Succès", "Produit ajouté avec succès.")
            ajouter_window.destroy()

        ajouter_window = tk.Toplevel(main_menu_window)
        ajouter_window.geometry("270x190")
        ajouter_window.title("Ajouter un produit")
        
        tk.Label(ajouter_window, text="Nom du commerçant:").pack()
        nom_entry = tk.Entry(ajouter_window)
        nom_entry.pack()

        tk.Label(ajouter_window, text="Nom du produit:").pack()
        produit_entry = tk.Entry(ajouter_window)
        produit_entry.pack()

        tk.Label(ajouter_window, text="Quantité:").pack()
        quantite_entry = tk.Entry(ajouter_window)
        quantite_entry.pack()

        tk.Label(ajouter_window, text="Prix:").pack()
        prix_entry = tk.Entry(ajouter_window)
        prix_entry.pack()

    def supprimer_produit():
        def confirmer_suppression():
            produit_a_supprimer = produit_entry.get()
            produits_restants = []
            produit_trouve = False

            with open('produits.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['produit'] != produit_a_supprimer:
                        produits_restants.append(row)
                    else:
                        produit_trouve = True
            
            if produit_trouve:
                with open('produits.csv', 'w', newline='') as csvfile:
                    fieldnames = ['nom', 'produit', 'quantite', 'prix']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for produit in produits_restants:
                        writer.writerow(produit)
                messagebox.showinfo("Succès", f"Le produit '{produit_a_supprimer}' a été supprimé.")
                supprimer_window.destroy()
            else:
                messagebox.showerror("Erreur", f"Produit '{produit_a_supprimer}' non trouvé.")
        
        supprimer_window = tk.Toplevel(main_menu_window)
        supprimer_window.geometry("250x85")
        supprimer_window.title("Supprimer un produit")
        
        tk.Label(supprimer_window, text="Nom du produit à supprimer:").pack()
        produit_entry = tk.Entry(supprimer_window)
        produit_entry.pack()
        tk.Button(supprimer_window, text="Supprimer", command=confirmer_suppression).pack()

    def trier_par_prix():
        try:
            df = pd.read_csv('produits.csv', on_bad_lines='skip')
            df_sorted = df.sort_values(by="prix", ascending=True, kind="quicksort")
            
            trier_window = tk.Toplevel(main_menu_window)
            trier_window.title("Produits triés par prix")
            trier_window.geometry("450x250")

            text_area = tk.Text(trier_window, height=15, width=50)
            text_area.pack(padx=10, pady=10)

            produits_tries = []
            for _, row in df_sorted.iterrows():
                produits_tries.append(f"{row['nom']}: {row['produit']}: {row['quantite']} en stock, Prix = {row['prix']} €")
            
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, "\n".join(produits_tries))
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")    
    
    def recherche_produit():
        def effectuer_recherche():
            sproduit = produit_entry.get().lower()
            produit_trouve = False

            with open("produits.csv", "r", newline='', encoding='utf-8') as fichier:
                donnee = list(csv.reader(fichier, delimiter=";"))
                for ligne in donnee:
                    if sproduit in ligne[0].lower():  # Recherche par le nom du produit
                        produit_trouve = True
                        messagebox.showinfo("Produit trouvé", f"Produit trouvé : {ligne}")
                        break
            
            if not produit_trouve:
                messagebox.showerror("Erreur", f"Aucun produit correspondant à '{sproduit}' n'a été trouvé.")

        recherche_window = tk.Toplevel(main_menu_window)
        recherche_window.title("Recherche de produit")
        recherche_window.geometry("300x150")
        
        tk.Label(recherche_window, text="Nom du produit à rechercher:").pack(pady=5)
        produit_entry = tk.Entry(recherche_window)
        produit_entry.pack(pady=5)
        tk.Button(recherche_window, text="Rechercher", command=effectuer_recherche).pack(pady=10)


    tk.Button(main_menu_window, text="Afficher les produits", command=afficher_produits).pack(pady=5)
    tk.Button(main_menu_window, text="Ajouter un produit", command=ajouter_produit).pack(pady=5)
    tk.Button(main_menu_window, text="Supprimer un produit", command=supprimer_produit).pack(pady=5)
    tk.Button(main_menu_window,text="Trier par prix", command=trier_par_prix).pack(pady=5)
    tk.Button(main_menu_window,text="Rechercher un produit", command=recherche_produit).pack(pady=5)
    tk.Button(main_menu_window, text="Quitter", command=main_menu_window.destroy).pack(pady=5)




# def change_pw():
#     email = input("Entrez votre email : ")
#     old_password = input("Entrez votre ancien mot de passe : ")

#     with open("users.csv", mode="r", encoding='utf-8') as file:
#         rows = list(csv.reader(file))
#     for row in rows:
#         reg_name = row[0]
#         reg_pass = row[1]
        
#         if email == reg_name:
#             pw_hash = hashlib.sha1(old_password.encode('utf-8')).hexdigest().upper()
#             if pw_hash == reg_pass:
#                 print("Ancien mot de passe validé.")
                
#                 new_password = input("Entrez votre nouveau mot de passe : ")
#                 new_password2 = input("Confirmez votre nouveau mot de passe : ")
                
#                 if new_password == new_password2:
#                     salt = genere_salage()
#                     pw_hash = hashlib.sha1(new_password.encode('utf-8')).hexdigest().upper()
                    
#                     with open("users.csv", mode="w", encoding='utf-8', newline="") as file:
#                         writer = csv.writer(file, delimiter=",")
#                         for r in rows:
#                             if r[0] == email:
#                                 writer.writerow([r[0], pw_hash, salt])
#                             else:
#                                 writer.writerow(r)
                    
#                     print("Votre mot de passe a été modifié avec succès !")
#                     return True
#                 else:
#                     print("Les mots de passe ne correspondent pas. Veuillez réessayer.")
#                     return change_pw()
#     print("Email ou mot de passe incorrect.")
#     return False

def access_login():
    if is_logged_in:
        show_main_menu()
    else:
        messagebox.showwarning("Accès interdit. Réessayer.",
                               "Veuillez vous connecter ou créer un compte.")
        

def main_window():
    window = tk.Tk()
    window.title("Authenfication")

    label_email = tk.Label(window, text="Email:")
    label_email.grid(row=0, column=0)

    email_entry = tk.Entry(window)
    email_entry.grid(row=0, column=1)

    label_password = tk.Label(window, text="Mot de passe:")
    label_password.grid(row=1, column=0)

    password_entry = tk.Entry(window, show="*")
    password_entry.grid(row=1, column=1)

    label_password2 = tk.Label(window, text="Confirmer le mot de passe:")
    label_password2.grid(row=2, column=0)

    password2_entry = tk.Entry(window, show="*")
    password2_entry.grid(row=2, column=1)

    result_label = tk.Label(window, text="")
    result_label.grid(row=4, column=1)

    def show_register_window():
        register(email_entry, password_entry, password2_entry, result_label)

    def show_login_window():
        login(email_entry, password_entry, result_label)

    button_register = tk.Button(window, text="Créer un compte", command=show_register_window)
    button_register.grid(row=3, column=0)

    button_login = tk.Button(window, text="Se connecter", command=show_login_window)
    button_login.grid(row=3, column=1)

    button_access = tk.Button(window, text="Accéder à la suite", command=access_login)
    button_access.grid(row=5, column=0, columnspan=2)

    window.mainloop()

if __name__ == "__main__":
    main_window()