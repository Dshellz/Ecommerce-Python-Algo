import pandas as pd

df = pd.read_csv('produits.csv', on_bad_lines='skip')
df_sorted = df.sort_values(by="prix", ascending=True, kind="quicksort")