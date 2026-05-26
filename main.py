import networkx as nx
import matplotlib.pyplot as plt

# =====================================================
# GRAFO
# =====================================================

G = nx.Graph()

# =====================================================
# CÔMODOS
# =====================================================

comodos = [
    "QD",
    "Sala",
    "Quarto",
    "Cozinha",
    "Banheiro",
    "Lavanderia"
]

G.add_nodes_from(comodos)

# =====================================================
# LUZES
# =====================================================

estado_luzes = {
    "Sala": False,
    "Quarto": False,
    "Cozinha": False,
    "Banheiro": False,
    "Lavanderia": False
}

potencia_luzes = {
    "Sala": 150,
    "Quarto": 150,
    "Cozinha": 200,
    "Banheiro": 100,
    "Lavanderia": 120
}

# =====================================================
# PERIFÉRICOS
# =====================================================

perifericos = {

    "TV_Sala": {
        "comodo": "Sala",
        "watts": 70,
        "ligado": False
    },

    "TV_Quarto": {
        "comodo": "Quarto",
        "watts": 70,
        "ligado": False
    },

    "Computador": {
        "comodo": "Quarto",
        "watts": 150,
        "ligado": False
    },

    "Geladeira": {
        "comodo": "Cozinha",
        "watts": 450,
        "ligado": False
    },

    "Liquidificador": {
        "comodo": "Cozinha",
        "watts": 500,
        "ligado": False
    },

    "Fogao": {
        "comodo": "Cozinha",
        "watts": 400,
        "ligado": False
    },

    "Chuveiro": {
        "comodo": "Banheiro",
        "watts": 6800,
        "ligado": False
    },

    "Maquina_Lavar": {
        "comodo": "Lavanderia",
        "watts": 400,
        "ligado": False
    }
}

# =====================================================
# ARESTAS
# =====================================================

G.add_edge("QD", "Sala", distancia=5)
G.add_edge("QD", "Quarto", distancia=6)
G.add_edge("QD", "Cozinha", distancia=10)
G.add_edge("QD", "Banheiro", distancia=4)
G.add_edge("QD", "Lavanderia", distancia=8)

# periféricos

for nome, dados in perifericos.items():

    G.add_node(nome)

    G.add_edge(
        dados["comodo"],
        nome,
        distancia=1
    )

# =====================================================
# BFS
# =====================================================

def bfs_ligar(comodo):

    estado_luzes[comodo] = True

def bfs_desligar(comodo):

    estado_luzes[comodo] = False

# =====================================================
# PERIFÉRICOS
# =====================================================

def ligar_periferico(nome):

    perifericos[nome]["ligado"] = True

def desligar_periferico(nome):

    perifericos[nome]["ligado"] = False

# =====================================================
# CONSUMO
# =====================================================

def calcular_consumo():

    total = 0

    # luzes

    for comodo, ligado in estado_luzes.items():

        if ligado:
            total += potencia_luzes[comodo]

    # periféricos

    for nome, dados in perifericos.items():

        if dados["ligado"]:
            total += dados["watts"]

    return total

energia_total = 0
def mostrar_consumo():

    global energia_total

    consumo = calcular_consumo()

    # atualização por segundo
    energia_total += consumo / 3600

    print("\n================================")
    print(" MONITORAMENTO ENERGÉTICO ")
    print("================================")

    print(f"\nConsumo Instantâneo: {consumo} W")

    print(
        f"Energia Acumulada: "
        f"{energia_total:.2f} Wh"
    )

    print(
        f"Energia em kWh: "
        f"{energia_total/1000:.4f} kWh"
    )

    print("\n--------------------------------")

    print("Luzes:")

    for comodo, ligado in estado_luzes.items():

        estado = "LIGADA" if ligado else "DESLIGADA"

        print(f"{comodo}: {estado}")

    print("\nPeriféricos:")

    for nome, dados in perifericos.items():

        estado = (
            "LIGADO"
            if dados["ligado"]
            else "DESLIGADO"
        )

        print(
            f"{nome}: "
            f"{estado} "
            f"({dados['watts']}W)"
        )

    print("================================\n")

# =====================================================
# DESENHO
# =====================================================

plt.ion()

fig = plt.figure(figsize=(14, 10))

def desenhar_grafo():

    plt.clf()

    pos = {

        "QD": (0, 0),

        "Sala": (-2, 2),
        "Quarto": (-2, -2),

        "Cozinha": (2, -2),
        "Banheiro": (2, 2),

        "Lavanderia": (4, 0),

        # periféricos

        "TV_Sala": (-4, 2),

        "TV_Quarto": (-4, -1),
        "Computador": (-4, -3),

        "Geladeira": (4, -1),
        "Liquidificador": (5, -2),
        "Fogao": (4, -3),

        "Chuveiro": (4, 3),

        "Maquina_Lavar": (6, 0)
    }

    cores = []

    for no in G.nodes():

        if no == "QD":

            cores.append("orange")

        elif no in estado_luzes:

            if estado_luzes[no]:
                cores.append("yellow")
            else:
                cores.append("lightblue")

        elif no in perifericos:

            if perifericos[no]["ligado"]:
                cores.append("red")
            else:
                cores.append("gray")

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=cores,
        node_size=2500,
        font_size=9
    )

    edge_labels = {}

    for u, v, data in G.edges(data=True):

        edge_labels[(u, v)] = f"{data['distancia']}m"

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels
    )

    plt.title(
        f"Consumo Atual: {calcular_consumo()} W"
    )

    plt.axis("off")

    plt.draw()
    plt.pause(0.1)

# =====================================================
# MENU DOS CÔMODOS
# =====================================================

def menu_sala():

    while True:

        print("\n===== SALA =====")

        print("1 -> Ligar Luz")
        print("2 -> Desligar Luz")

        print("3 -> Ligar TV")
        print("4 -> Desligar TV")

        print("0 -> Sair da Sala")

        op = input("Escolha: ")

        if op == "1":
            bfs_ligar("Sala")

        elif op == "2":
            bfs_desligar("Sala")

        elif op == "3":
            ligar_periferico("TV_Sala")

        elif op == "4":
            desligar_periferico("TV_Sala")

        elif op == "0":
            break

        desenhar_grafo()
        mostrar_consumo()

# =====================================================

def menu_quarto():

    while True:

        print("\n===== QUARTO =====")

        print("1 -> Ligar Luz")
        print("2 -> Desligar Luz")

        print("3 -> Ligar TV")
        print("4 -> Desligar TV")

        print("5 -> Ligar Computador")
        print("6 -> Desligar Computador")

        print("0 -> Sair do Quarto")

        op = input("Escolha: ")

        if op == "1":
            bfs_ligar("Quarto")

        elif op == "2":
            bfs_desligar("Quarto")

        elif op == "3":
            ligar_periferico("TV_Quarto")

        elif op == "4":
            desligar_periferico("TV_Quarto")

        elif op == "5":
            ligar_periferico("Computador")

        elif op == "6":
            desligar_periferico("Computador")

        elif op == "0":
            break

        desenhar_grafo()
        mostrar_consumo()

# =====================================================

def menu_cozinha():

    while True:

        print("\n===== COZINHA =====")

        print("1 -> Ligar Luz")
        print("2 -> Desligar Luz")

        print("3 -> Ligar Geladeira")
        print("4 -> Ligar Fogão")

        print("5 -> Ligar Liquidificador")

        print("6 -> Desligar Geladeira")
        print("7 -> Desligar Fogão")

        print("8 -> Desligar Liquidificador")

        print("0 -> Sair da Cozinha")

        op = input("Escolha: ")

        if op == "1":
            bfs_ligar("Cozinha")

        elif op == "2":
            bfs_desligar("Cozinha")

        elif op == "3":
            ligar_periferico("Geladeira")

        elif op == "4":
            ligar_periferico("Fogao")

        elif op == "5":
            ligar_periferico("Liquidificador")

        elif op == "6":
            desligar_periferico("Geladeira")

        elif op == "7":
            desligar_periferico("Fogao")

        elif op == "8":
            desligar_periferico("Liquidificador")

        elif op == "0":
            break

        desenhar_grafo()
        mostrar_consumo()

def menu_banheiro():
    while True:
        print("\n===== BANHEIRO =====")
        print("1 -> Ligar Luz")
        print("2 -> Desligar Luz")
        print("3 -> Ligar Chuveiro")
        print("0 -> Sair do Banheiro")

        op = input("Escolha: ")

        if op == "1":
            bfs_ligar("Banheiro")

        elif op == "2":
            bfs_desligar("Banheiro")

        elif op == "3":
            ligar_periferico("Chuveiro")

        elif op == "0":
            break

        desenhar_grafo()
        mostrar_consumo()


# =====================================================
# MENU PRINCIPAL
# =====================================================

desenhar_grafo()

while True:

    print("\n==============================")
    print(" SISTEMA ELÉTRICO ")
    print("==============================")

    print("\n1 -> Sala")
    print("2 -> Quarto")
    print("3 -> Cozinha")
    print("4 -> Banheiro")

    print("0 -> Sair")

    entrada = input("Escolha: ")

    if entrada == "1":
        menu_sala()

    elif entrada == "2":
        menu_quarto()

    elif entrada == "3":
        menu_cozinha()

    elif entrada == "4":
        menu_banheiro()

    elif entrada == "0":
        break

    desenhar_grafo()
    mostrar_consumo()

plt.ioff()
plt.show()