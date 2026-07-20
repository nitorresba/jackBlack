import pandas as pd
import random

# Valores de Blackjack
valores = {
    "A": 11, "2": 2, "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 10, "K": 10
}

# Leer mazo desde CSV
df = pd.read_csv("mazo_ascii.csv")

# Leer carta cubierta desde TXT
with open("carta cubierta.txt", "r") as f:
    carta_txt = f.read().strip()

# se le da un valor a la carta oculta para que el dealer pueda calcular su valor correctamente
carta_respaldo = {"ascii": carta_txt, "valor": "A"}  

# Función para imprimir cartas lado a lado
def imprimir_cartas(cartas_ascii):
    cartas_lineas = [c.split("\n") for c in cartas_ascii]
    max_lineas = max(len(c) for c in cartas_lineas)
    for i in range(max_lineas):
        fila = "   ".join(c[i] for c in cartas_lineas)
        print(fila)

# Calcular valor de una mano
def calcular_valor(mano):
    total = sum(valores[c["valor"]] for c in mano)
    ases = sum(1 for c in mano if c["valor"] == "A")
    while total > 21 and ases > 0:
        total -= 10
        ases -= 1
    return total

# Turno del jugador
def jugar_mano(mano, nombre="Jugador"):
    total = calcular_valor(mano)
    while True:
        if total >= 21:
            break
        accion = input("¿Quieres pedir carta (h) o plantarte (s)? ")
        if accion.lower() == "h":
            mano.append(df.sample(1).to_dict(orient="records")[0])
            cartas = [c["ascii"].replace("\\n", "\n") for c in mano]
            imprimir_cartas(cartas)
            total = calcular_valor(mano)
            print(f"{nombre} total: {total}\n")
        else:
            break
    return mano

# Turno del dealer (que tome cartas hasta 17 como dijo nick)
def turno_dealer(mano):
    while calcular_valor(mano) < 17:
        mano.append(df.sample(1).to_dict(orient="records")[0])
    return mano

# Comparar manos
def comparar(jugador, dealer):
    total_j = calcular_valor(jugador)
    total_d = calcular_valor(dealer)
    print(f"\nJugador: {total_j} | Dealer: {total_d}")
    if total_j > 21:
        print("Jugador pierde (se pasó).")
    elif total_d > 21 or total_j > total_d:
        print("Jugador gana!")
    elif total_j == total_d:
        print("Empate.")
    else:
        print("Dealer gana.")

# --- Juego principal ---
jugador = df.sample(2).to_dict(orient="records")
dealer = [df.sample(1).to_dict(orient="records")[0], carta_respaldo]
dealerfinal = [dealer[0], df.sample(1).to_dict(orient="records")[0]]  # Dealer revela su carta oculta al final
print("=== Mano inicial ===")

# Dealer muestra carta normal + oculta al lado

print("Dealer:")
imprimir_cartas([c["ascii"].replace("\\n", "\n") for c in dealer])



# Jugador muestra sus dos cartas
print("Jugador:")
imprimir_cartas([c["ascii"].replace("\\n", "\n") for c in jugador])
print(f"Total: {calcular_valor(jugador)}\n")

# Turno del jugador
jugador = jugar_mano(jugador, "Jugador")


dealer = turno_dealer(dealerfinal)

# Comparación final
print("\n=== Fin de la ronda ===")
print("Dealer (descubierto):")
# Aquí mostramos todas las cartas reales del dealer 
print("Dealer:")
imprimir_cartas([c["ascii"].replace("\\n", "\n") for c in dealerfinal])


print("Jugador:")
imprimir_cartas([c["ascii"].replace("\\n", "\n") for c in jugador])
print(f"Total: {calcular_valor(jugador)}\n")

comparar(jugador, dealerfinal)