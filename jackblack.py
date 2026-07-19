import pandas as pd


df = pd.read_csv("mazo_ascii.csv")

# Mostrar cada carta con saltos de línea reales
for i, row in df.iterrows():
    carta = row["ascii"].replace("\\n", "\n")
    print(carta)
    print()
