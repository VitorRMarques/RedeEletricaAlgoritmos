import networkx as nx
import matplotlib.pyplot as plt

def criar_e_plotar_grafo():
    G = nx.Graph()

    G.add_node(1)

    G.add_nodes_from([2, 3])

    G.add_nodes_from([(4, {"color": "red"}), (5, {"color": "green"})])

    H = nx.path_graph(10)

    G.add_nodes_from(H)

    G.add_node(H)

    G.add_edge(1, 2)

    e = (2, 3)

    G.add_edge(*e)

    G.add_edges_from([(1, 2), (1, 3)])

    G.add_edges_from(H.edges)

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(6,4))

    nx.draw(
        G, pos, 
        with_labels=True,
        node_color='skyblue',
        node_size=1200,
        font_size=12,
        font_color='black',
        edge_color='gray',
        width=2
    )

    plt.title("Visualizacao de Grafo com Matplotlib + NetworkX")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    try:
        criar_e_plotar_grafo()
    except Exception as e:
        print(f"Erro ao criar o grafo: {e}" )





