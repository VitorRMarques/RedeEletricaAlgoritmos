import networkx as nx
import matplotlib.pyplot as plt
import time
import random
from collections import deque as dq


G = nx.Graph()


comodos = [
    "QD",
    "Sala",
    "Quarto",
    "Cozinha",
    "Banheiro",
    "Lavanderia"
]

G.add_nodes_from(comodos)

qd = {
    "ligado": True,
    "limite_potencia": 7000
}

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

tempo_chuveiro = random.randint(1, 20)
inicio_chuveiro = None


G.add_edge("QD", "Sala", distancia=5)
G.add_edge("QD", "Quarto", distancia=6)
G.add_edge("QD", "Cozinha", distancia=10)
G.add_edge("QD", "Banheiro", distancia=4)
G.add_edge("QD", "Lavanderia", distancia=8)


for nome, dados in perifericos.items():

    G.add_node(nome)

    G.add_edge(
        dados["comodo"],
        nome,
        distancia=1
    )


energia_total = 0
ultimo_tempo = time.time()

def calcular_consumo():

    total = 0

    for comodo, ligado in estado_luzes.items():

        if ligado:

            total += potencia_luzes[comodo]

    for nome, dados in perifericos.items():

        if dados["ligado"]:

            total += dados["watts"]

    return total


def mostrar_consumo():

    global energia_total
    global ultimo_tempo

    agora = time.time()

    delta = agora - ultimo_tempo

    ultimo_tempo = agora

    consumo = calcular_consumo()

    # energia em Wh
    energia_total += (
        consumo * delta
    ) / 3600

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

    estado_qd = (
        "ARMADO" if qd["ligado"] == True
        else "DESARMADO"
    )
    print(f"\nQD: {estado_qd}")

    print("LUZES:")

    for comodo, ligado in estado_luzes.items():

        estado = (
            "LIGADA"
            if ligado
            else "DESLIGADA"
        )

        print(f"{comodo}: {estado}")

    print("\nPERIFÉRICOS:")

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


def bfs_energia(inicio, ligar=True, bloqueados=None):

    if not qd["ligado"]:
        print("QD DESARMADO!")
        print("Rearme o QD antes de energizar o sistema.")
        return

    fila = dq([inicio])
    visitados = set()

    print("\n============ BFS ============\n")
    time.sleep(1)

    while fila:
        atual = fila.popleft()
        time.sleep(1)

        if atual not in visitados:

            visitados.add(atual)
            if atual in estado_luzes:
                estado_luzes[atual] = ligar
                time.sleep(1)
                estado = (
                    "LIGADA"
                    if ligar
                    else "DESLIGADA"
                )
                time.sleep(1)
                print(f"{atual}: {estado}")
            if atual in perifericos:
                perifericos[atual]["ligado"] = ligar
                estado = (
                    "LIGADO"
                    if ligar
                    else "DESLIGADO"
                )
                print(f"{atual}: {estado}")
                time.sleep(1)

            for vizinho in G.neighbors(atual):

                if vizinho == "QD":
                    continue

                if (
                    vizinho not in visitados
                ):
                    fila.append(vizinho)

    print("\n=============================\n")


def bfs_desligar_qd():
    qd["ligado"] = False

    fila = dq(["QD"])
    visitados = set()

    print("\n====== DESARMANDO QD ======")

    while fila:
        atual = fila.popleft()
        if atual not in visitados:
            visitados.add(atual)
            if atual in estado_luzes:
                estado_luzes[atual] = False
                print(f"{atual}: LUZES DESLIGADAS")
            if atual in perifericos:
                perifericos[atual]["ligado"] = False
                print(f"{atual}: PERIFERICO DESLIGADO")
            for vizinho in G.neighbors(atual):
                if vizinho not in visitados:
                    fila.append(vizinho)

    print("\nSOBRECARGA DETECTADA")
    time.sleep(5)
    print("QD DESARMADO!")
    time.sleep(5)
    print("Toda a residencia foi desligada.")
    time.sleep(5)

def rearmar_qd():
    qd["ligado"] = True
    print("\nQD REARMADO!")

def verificar_sobrecarga():

    if not qd["ligado"]:
        return 
    
    consumo = calcular_consumo()

    if consumo > qd["limite_potencia"]:
        print("SOBRECARGA DETECTADA")

        print(f"Consumo atual: {consumo} W")
        print(
            f"limite do QD: "
            f"{qd['limite_potencia']} W"
        )

        bfs_desligar_qd()
        desenhar_grafo()
        mostrar_consumo()

def ligar_e_verificar(nome):
    perifericos[nome]["ligado"] = True
    verificar_sobrecarga()

def verificar_qd():

    if not qd["ligado"]:

        print("\n================================")
        print("QD DESARMADO!")
        print("Rearme o QD para ligar cargas.")
        print("================================\n")

        return False

    return True


def dfs_energia(inicio):

    visitados = set()

    print("\n============ DFS ============\n")
    time.sleep(1)

    def dfs(no):

        visitados.add(no)

        print(f"\nVisitando: {no}")


        if no in estado_luzes:

            estado = (
                "LIGADA"
                if estado_luzes[no]
                else "DESLIGADA"
            )

            print("Tipo: Cômodo")
            print(f"Estado: {estado}")

            print(
                f"Potência Luz: "
                f"{potencia_luzes[no]}W"
            )


        elif no in perifericos:

            estado = (
                "LIGADO"
                if perifericos[no]["ligado"]
                else "DESLIGADO"
            )

            print("Tipo: Periférico")
            print(f"Estado: {estado}")

            print(
                f"Potência: "
                f"{perifericos[no]['watts']}W"
            )


        for vizinho in G.neighbors(no):

            if vizinho not in visitados:

                dfs(vizinho)

    dfs(inicio)

    print("\n=============================\n")

    return visitados


plt.ion()

fig = plt.figure(figsize=(14, 10))

def desenhar_grafo():

    fig.clear()

    ax = fig.add_subplot(111)

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

        # quadro

        if no == "QD":
            if qd["ligado"]:


                cores.append("orange")
            else:


                cores.append("gray")

        # cômodos

        elif no in estado_luzes:

            if estado_luzes[no]:

                cores.append("gold")

            else:

                cores.append("deepskyblue")

        # periféricos

        elif no in perifericos:

            if perifericos[no]["ligado"]:

                cores.append("red")

            else:

                cores.append("dimgray")

        else:

            cores.append("white")


    nx.draw(
        G,
        pos,
        ax=ax,
        with_labels=True,
        node_color=cores,
        node_size=2500,
        font_size=9
    )

    edge_labels = {}

    for u, v, data in G.edges(data=True):

        edge_labels[(u, v)] = (
            f"{data['distancia']}m"
        )

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        ax=ax
    )

    # =================================================

    plt.title(
        f"Sistema Elétrico Residencial\n"
        f"Consumo Atual: "
        f"{calcular_consumo()} W"
    )

    plt.axis("off")

    plt.draw()
    plt.pause(0.1)

# =====================================================
# MENU BFS
# =====================================================

def menu_bfs(comodo):

    acao = input(
        "\n1 -> Ligar\n"
        "2 -> Desligar\n"
        "Escolha: "
    )

    if acao == "1":

        ligar = True

    elif acao == "2":

        ligar = False

    else:

        print("Opção inválida")
        return

    bfs_energia(
        comodo,
        ligar
    )

    desenhar_grafo()
    mostrar_consumo()

# =====================================================
# MENUS DOS CÔMODOS
# =====================================================

def menu_sala():

    while True:

        print("\n===== SALA =====")

        print("1 -> Ligar Luz")
        print("2 -> Desligar Luz")

        print("3 -> Ligar TV")
        print("4 -> Desligar TV")

        print("0 -> Voltar")

        op = input("Escolha: ")

        if op == "1":
            if not qd["ligado"]:
                print("QD DESARMADO")
                continue
            


            estado_luzes["Sala"] = True

        elif op == "2":

            estado_luzes["Sala"] = False

        elif op == "3":
            if not qd["ligado"]:
                print("QD DESARMADO")
                continue
            

            ligar_e_verificar("TV_Sala")
            desenhar_grafo()
            mostrar_consumo()
            verificar_sobrecarga()

        elif op == "4":

            perifericos["TV_Sala"]["ligado"] = False

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

        print("0 -> Voltar")

        op = input("Escolha: ")

        if op == "1":
            if not qd["ligado"]:
                print("QD DESARMADO")
                continue

            estado_luzes["Quarto"] = True

        elif op == "2":

            estado_luzes["Quarto"] = False

        elif op == "3":
            if not qd["ligado"]:
                print("QD DESARMADO")
                continue

            ligar_e_verificar("TV_Quarto")
            desenhar_grafo()
            mostrar_consumo()
            verificar_sobrecarga()

        elif op == "4":

            perifericos["TV_Quarto"]["ligado"] = False

        elif op == "5":
            if not qd["ligado"]:
                print("QD DESARMADO")
                continue

            ligar_e_verificar("Computador")
            desenhar_grafo()
            mostrar_consumo()
            verificar_sobrecarga()

        elif op == "6":

            perifericos["Computador"]["ligado"] = False

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
        print("4 -> Desligar Geladeira")

        print("5 -> Ligar Fogao")
        print("6 -> Desligar Fogao")

        print("7 -> Ligar Liquidificador")
        print("8 -> Desligar Liquidificador")

        print("0 -> Voltar")

        op = input("Escolha: ")

        if op == "1":
            if not qd["ligado"]:
                print("QD DESARMADO")
                continue


            estado_luzes["Cozinha"] = True

        elif op == "2":
            if not qd["ligado"]:
                print("QD DESARMADO")
                continue

            estado_luzes["Cozinha"] = False

        elif op == "3":
            if not qd["ligado"]:
                print("QD DESARMADO")
                continue

            ligar_e_verificar("Geladeira")
            desenhar_grafo()
            mostrar_consumo()
            verificar_sobrecarga()

        elif op == "4":
            if not qd["ligado"]:
                print("QD DESARMADO")
                continue

            perifericos["Geladeira"]["ligado"] = False

        elif op == "5":
            if not qd["ligado"]:
                print("QD DESARMADO")
                continue

            ligar_e_verificar("Fogao")
            desenhar_grafo()
            mostrar_consumo()
            verificar_sobrecarga()

        elif op == "6":
            if not qd["ligado"]:
                print("QD DESARMADO")
                continue

            perifericos["Fogao"]["ligado"] = False

        elif op == "7":
            if not qd["ligado"]:
                print("QD DESARMADO")
                continue

            ligar_e_verificar("Liquidificador")

            desenhar_grafo()
            mostrar_consumo()
            verificar_sobrecarga()

        elif op == "8":
            if not qd["ligado"]:
                print("QD DESARMADO")
                continue

            perifericos["Liquidificador"]["ligado"] = False

        elif op == "0":

            break

        desenhar_grafo()
        mostrar_consumo()

# =====================================================

def menu_banheiro():

    while True:

        print("\n===== BANHEIRO =====")

        print("1 -> Ligar Luz")
        print("2 -> Desligar Luz")

        print("3 -> Ligar Chuveiro")
        print("4 -> Desligar Chuveiro")

        print("0 -> Voltar")

        op = input("Escolha: ")

        if op == "1":
            if not qd["ligado"]:
               print("QD DESARMADO")
               continue

            estado_luzes["Banheiro"] = True

        elif op == "2":
            if not qd["ligado"]:
                print("QD DESARMADO")
                continue

            estado_luzes["Banheiro"] = False

        elif op == "3":
            if not qd["ligado"]:
                print("QD DESARMADO")
                continue

            ligar_e_verificar("Chuveiro")
            desenhar_grafo()
            mostrar_consumo()
            verificar_sobrecarga()

            global inicio_chuveiro

            inicio_chuveiro = time.time()
            time.sleep(1)

            print(
                "\nChuveiro Ligado."
            )
        elif op == "4":
            if not qd["ligado"]:
                print("QD DESARMADO")
                continue

            perifericos["Chuveiro"]["ligado"] = False
            inicio_chuveiro = None
            print("\nChuveiro desligado.")

        elif op == "0":

            break

        desenhar_grafo()
        mostrar_consumo()

# =====================================================

def menu_lavanderia():

    while True:

        print("\n===== LAVANDERIA =====")

        print("1 -> Ligar Luz")
        print("2 -> Desligar Luz")

        print("3 -> Ligar Máquina")
        print("4 -> Desligar Máquina")

        print("0 -> Voltar")

        op = input("Escolha: ")

        if op == "1":
            if not qd["ligado"]:
                print("QD DESARMADO")
                continue

            estado_luzes["Lavanderia"] = True

        elif op == "2":
            if not qd["ligado"]:
                print("QD DESARMADO")
                continue

            estado_luzes["Lavanderia"] = False

        elif op == "3":
            if not qd["ligado"]:
                print("QD DESARMADO")
                continue

            ligar_e_verificar("Maquina_Lavar")
            desenhar_grafo()
            mostrar_consumo()
            verificar_sobrecarga()

        elif op == "4":
            if not qd["ligado"]:
                print("QD DESARMADO")
                continue

            perifericos["Maquina_Lavar"]["ligado"] = False

        elif op == "0":

            break

        desenhar_grafo()
        mostrar_consumo()

# =====================================================
# MENU CÔMODOS
# =====================================================

def menu_comodos():

    while True:

        print("\n==============================")
        print(" MENU DOS CÔMODOS ")
        print("==============================")

        print("\n1 -> Sala")
        print("2 -> Quarto")
        print("3 -> Cozinha")
        print("4 -> Banheiro")
        print("5 -> Lavanderia")

        print("0 -> Voltar")

        op = input("Escolha: ")

        if op == "1":

            menu_sala()

        elif op == "2":

            menu_quarto()

        elif op == "3":

            menu_cozinha()

        elif op == "4":

            menu_banheiro()

        elif op == "5":

            menu_lavanderia()

        elif op == "0":

            break

# =====================================================
# MENU PRINCIPAL
# =====================================================

desenhar_grafo()

while True:

    print("\n==============================")
    print(" SISTEMA ELÉTRICO ")
    print("==============================")

    print("\n1 -> Cômodos")
    print("2 -> Menu BFS (Ligar tudo em uma sala)")
    print("3 -> Verificação DFS (Verificacao Ligados ou Desligados)")
    print("4 -> Rearmar QD")

    print("0 -> Sair")

    entrada = input("\nEscolha: ")

    # =================================================
    # MENU CÔMODOS
    # =================================================

    if entrada == "1":

        menu_comodos()

    # =================================================
    # MENU BFS
    # =================================================

    elif entrada == "2":

        print("\n===== MENU BFS =====")

        print("1 -> Sala")
        print("2 -> Quarto")
        print("3 -> Cozinha")
        print("4 -> Banheiro")
        print("5 -> Lavanderia")

        op = input("Escolha: ")

        if op == "1":

            menu_bfs("Sala")

        elif op == "2":

            menu_bfs("Quarto")

        elif op == "3":

            menu_bfs("Cozinha")

        elif op == "4":

            menu_bfs("Banheiro")

        elif op == "5":

            menu_bfs("Lavanderia")

    # =================================================
    # DFS
    # =================================================

    elif entrada == "3":

        dfs_energia("QD")

    # =================================================

    elif entrada == "4":
        rearmar_qd()

    elif entrada == "0":

        break

    desenhar_grafo()
    mostrar_consumo()
    verificar_sobrecarga()

plt.ioff()
plt.show()