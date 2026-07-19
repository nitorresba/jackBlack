import pandas as pd

def dibujar_carta(valor, palo):
    if valor == "10":
        linea_sup = f"|{valor}   |"
        linea_inf = f"|   {valor}|"
    else:
        linea_sup = f"|{valor}    |"
        linea_inf = f"|    {valor}|"

    carta = [
        "+-----+",
        linea_sup,
        f"|  {palo}  |",
        linea_inf,
        "+-----+"
    ]
    return "\n".join(carta)

valores = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
palos = ["♥","♦","♣","♠"]

mazo = []
for palo in palos:
    for valor in valores:
        mazo.append({
            "valor": valor,
            "palo": palo,
            "ascii": dibujar_carta(valor, palo)
        })


df = pd.DataFrame(mazo)
print(df)

df.to_csv("mazo_ascii.csv", index=False)


