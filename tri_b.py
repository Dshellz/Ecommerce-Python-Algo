import pandas as pd

produits = pd.read_csv('produits.csv', on_bad_lines='skip')

def tri_bulle(df, colonne):
    n = len(df)
    
    
    for i in range(n): # Algorithme de tri à bulles
        for j in range(0, n-i-1):
            if df[colonne].iloc[j] > df[colonne].iloc[j+1]:
                # Échanger les lignes
                df.iloc[j], df.iloc[j+1] = df.iloc[j+1].copy(), df.iloc[j].copy()
    
    return df


produits_trie = tri_bulle(produits, 'produit') # Mettre le tri à bulles sur la colonne produit