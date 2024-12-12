import csv

def lire_produits(fichier):
    produits = []
    with open(fichier, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Pour ignorer l'en-tête si nécessaire
        for row in reader:
            produit = row[0]
            quantite = int(row[1])
            prix = float(row[2])
            produits.append({'produit': produit, 'quantite': quantite, 'prix': prix})
    return produits

def tri_bulle(produits, critere='prix'): #tri à bulle
    n = len(produits)
    for i in range(n):
        for j in range(0, n - i - 1):
            if critere == 'prix':
                if produits[j]['prix'] > produits[j + 1]['prix']:
                    produits[j], produits[j + 1] = produits[j + 1], produits[j]
            elif critere == 'quantite':
                if produits[j]['quantite'] > produits[j + 1]['quantite']:
                    produits[j], produits[j + 1] = produits[j + 1], produits[j]
    return produits

def menu(): # le menu pour le tri relier au menu interactif
    fichier = 'produits.csv'
    produits = lire_produits(fichier)

    print("Choisissez un critère de tri :")
    print("1| Trier par prix")
    print("2| Trier par quantité")
    
    choix = input("Entrez votre choix (1 ou 2) : ")

    if choix == '1':
        produits_tries = tri_bulle(produits, critere='prix')
        print("Produits triés par prix :")
    elif choix == '2':
        produits_tries = tri_bulle(produits, critere='quantite')
        print("Produits triés par quantité :")
    else:
        print("Choix invalide. Aucun tri effectué.")
        return
    
    for produit in produits_tries:
        print(f"{produit['produit']} - Quantité : {produit['quantite']} - Prix : {produit['prix']}€")

if __name__ == "__main__":
    menu() 