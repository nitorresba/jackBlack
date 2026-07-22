import pandas as pd
import os
import webbrowser
import textwrap
# limpiar pantalla = os.system('cls' if os.name == 'nt' else 'clear')

# Valores de Blackjack
valores = {
    "A": 11, "2": 2, "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 10, "K": 10
}

# Leer mazo desde CSV
df = pd.read_csv("mazo_ascii.csv")
df["ascii"] = df["ascii"].str.replace("\r", "")  # el csv se guardó con saltos de línea de windows y dañaba el dibujo

# Leer carta cubierta desde TXT
with open("carta cubierta.txt", "r") as f:
    carta_txt = f.read().strip()

# se le da un valor a la carta oculta para que el dealer pueda calcular su valor correctamente
carta_respaldo = {"ascii": carta_txt, "valor": "A"}

# Leer fichas desde TXT (cada ficha ocupa 5 lineas de dibujo)
def cargar_fichas(ruta="fichas.txt"):
    with open(ruta, "r") as f:
        lineas = f.read().splitlines()
    fichas = {}
    for i in range(0, len(lineas), 5):
        bloque = lineas[i:i + 5]
        etiqueta = bloque[2].replace(":", "").strip()
        fichas[etiqueta] = "\n".join(bloque)
    return fichas

fichas = cargar_fichas()

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

# Elegir con qué ficha se apuesta, según el saldo disponible
def elegir_apuesta(saldo):
    print(f"Saldo actual: ${saldo}")
    disponibles = [f for f in fichas if f != "ALL-IN" and int(f.replace("$", "")) <= saldo]
    if saldo > 0:
        disponibles.append("ALL-IN")
    print("Fichas disponibles:", ", ".join(disponibles))
    while True:
        eleccion = input("¿Con qué ficha quieres apostar? ").strip().upper()
        if eleccion != "ALL-IN":
            eleccion = f"${eleccion.replace('$', '')}"
        if eleccion not in disponibles:
            print("Esa ficha no la tienes disponible, intenta de nuevo.")
            continue
        break
    apuesta = saldo if eleccion == "ALL-IN" else int(eleccion.replace("$", ""))
    os.system('cls' if os.name == 'nt' else 'clear')
    print(fichas[eleccion])
    return apuesta

# Turno del jugador
def jugar_mano(mano, nombre="Jugador"):
    total = calcular_valor(mano)
    while True:
        if total >= 21:
            break
        accion = input("¿Quieres pedir carta (h) o plantarte (s)? ")
        if accion.lower() == "h":
            os.system('cls' if os.name == 'nt' else 'clear')
            mano.append(df.sample(1).to_dict(orient="records")[0])
            cartas = [c["ascii"].replace("\\n", "\n") for c in mano]
            imprimir_cartas(cartas)
            total = calcular_valor(mano)
            print(f"{nombre} total: {total}\n")
        elif accion.lower() == "s":
            os.system('cls' if os.name == 'nt' else 'clear')
            break
    return mano

# Turno del dealer (que tome cartas hasta 17)
def turno_dealer(mano):
    while calcular_valor(mano) < 17:
        mano.append(df.sample(1).to_dict(orient="records")[0])
    return mano

# Comparar manos y ajustar el saldo según la apuesta
def comparar(jugador, dealer, saldo, apuesta):
    total_j = calcular_valor(jugador)
    total_d = calcular_valor(dealer)
    print(f"\nJugador: {total_j} | Dealer: {total_d}")
    if total_j > 21:
        print("Jugador pierde (se pasó).")
        saldo -= apuesta
    elif total_d > 21 or total_j > total_d:
        print("Jugador gana!")
        saldo += apuesta
    elif total_j == total_d:
        print("Empate, se devuelve la ficha.")
    else:
        print("Dealer gana.")
        saldo -= apuesta
    print(f"Saldo: ${saldo}\n")
    return saldo

# guardar los puntajes mas altos
def guardar_puntaje(nombre, saldo, archivo="puntajes.txt"):
    puntajes = []

    with open(archivo, "r") as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                jugador, puntos = linea.rsplit(",", 1)
                puntajes.append((jugador, int(puntos)))

    puntajes.append((nombre, saldo))

    for i in range(len(puntajes)):
        for j in range(len(puntajes) - 1):
            if puntajes[j][1] < puntajes[j + 1][1]:
                aux = puntajes[j]
                puntajes[j] = puntajes[j + 1]
                puntajes[j + 1] = aux

    puntajes = puntajes[:5]

    archivo = open("puntajes.txt", "w")
    for jugador, puntos in puntajes:
        archivo.write(f"{jugador},{puntos}\n")

def top_puntajes():
    puntajes = []
    with open("puntajes.txt", "r") as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                jugador, puntos = linea.rsplit(",", 1)
                puntajes.append((jugador, int(puntos)))
    print("\n=== Top Puntajes ===")
    for i, (jugador, puntos) in enumerate(puntajes, start=1):
        print(f"{i}. {jugador} - ${puntos}")

# --- Juego principal ---
def menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Bienvenido a JackBlack ===")
    top_puntajes()
    print("\nIngresa una de las siguientes opciones:")
    opcion = input("\nReglas\nJugar\nSalir\n\n")
    match opcion:
        case "Reglas":
            os.system('cls' if os.name == 'nt' else 'clear')
            with open("reglas.txt", "r") as reglas:
                texto = reglas.read()
                print(textwrap.fill(texto, width=100))
            print("\nPresiona ENTER para volver al menú principal.")
            input()
            menu()
        case "Jugar":
            os.system('cls' if os.name == 'nt' else 'clear')
            saldo = 1000
            print(f"Empiezas con ${saldo} en fichas.\n")
            nombre = input("Ingresa tu nombre: ")
            while saldo > 0:
                os.system('cls' if os.name == 'nt' else 'clear')
                apuesta = elegir_apuesta(saldo)
                jugador = df.sample(2).to_dict(orient="records")
                dealer_visible = df.sample(1).to_dict(orient="records")[0]
                dealer_oculta = df.sample(1).to_dict(orient="records")[0]  # esta es la carta real que está boca abajo
                dealer = [dealer_visible, carta_respaldo]  # lo que ve el jugador mientras juega su mano

                print("\n=== Inicio de la ronda ===")

                # Dealer muestra carta normal + oculta al lado
                print("Dealer:")
                imprimir_cartas([c["ascii"].replace("\\n", "\n") for c in dealer])

                # Jugador muestra sus dos cartas
                print("Jugador:")
                imprimir_cartas([c["ascii"].replace("\\n", "\n") for c in jugador])
                print(f"Total: {calcular_valor(jugador)}\n")

                # Turno del jugador
                jugador = jugar_mano(jugador, "Jugador")

                # Dealer revela su carta oculta al final y pide si le hace falta
                dealerfinal = turno_dealer([dealer_visible, dealer_oculta])
                os.system('cls' if os.name == 'nt' else 'clear')
                # Comparación final
                print("\n=== Fin de la ronda ===")
                print("Dealer (descubierto):")
                imprimir_cartas([c["ascii"].replace("\\n", "\n") for c in dealerfinal])
                print("Jugador:")
                imprimir_cartas([c["ascii"].replace("\\n", "\n") for c in jugador])
                print(f"Total: {calcular_valor(jugador)}\n")
                saldo = comparar(jugador, dealerfinal, saldo, apuesta)

                if saldo <= 0:
                    print("Te quedaste sin fichas. Fin del juego.")
                    guardar_puntaje(nombre, saldo)
                    break

                otra = input("¿Quieres jugar otra ronda? (s/n) ")
                if otra.lower() != "s":
                    print(f"\nGracias por jugar. Te vas con ${saldo}.")
                    guardar_puntaje(nombre, saldo)
                    webbrowser.open("https://youtu.be/41O_MydqxTU?si=_Q7YfHNm2PKNGFnjju")
                    break
        case "Salir":
            os.system('cls' if os.name == 'nt' else 'clear')
            return
        case _:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("No has ingresado una opción válida. Recuerda usar solo minúsculas y números.\n\nPresiona ENTER para volver al menú principal.")
            input()
            menu()
menu()