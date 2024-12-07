import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def PaintNonOrientatedGraphWithWay (matrix : np.array, way : np.array) -> None :
    G = nx.Graph()
    G.add_nodes_from(list(range(1, matrix.shape[0] + 1)))
    for i in range(matrix.shape[0]) :
        for j in range(i, matrix.shape[0]) :
            if matrix[i][j] :
                G.add_weighted_edges_from([(i + 1, j + 1, matrix[i][j])])
    Positions = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, Positions, node_color="black", node_size=100)
    Weights = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edges(G, Positions, width=2, alpha=0.5, edge_color="blue")
    EdgeLabels = {edge : f"{Weights[edge]}" for edge in G.edges()}
    HighlightedEdges = []
    for i in range(1, way.size) :
        HighlightedEdges.append((way[i - 1] + 1, way[i] + 1))
    nx.draw_networkx_edges(G, Positions, edgelist=HighlightedEdges, edge_color="green", width=3)
    nx.draw_networkx_edge_labels(G, Positions, edge_labels=EdgeLabels, font_color="red")
    plt.title("Our Task Graph Visualisation")
    plt.axis("off")
    plt.show()
    return


def PaintNonOrientatedGraphWithCycle (matrix : np.array, way : np.array) -> None :
    G = nx.Graph()
    G.add_nodes_from(list(range(1, matrix.shape[0] + 1)))
    for i in range(matrix.shape[0]) :
        for j in range(i, matrix.shape[0]) :
            if matrix[i][j] :
                G.add_weighted_edges_from([(i + 1, j + 1, matrix[i][j])])
    Positions = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, Positions, node_color="black", node_size=100)
    Weights = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edges(G, Positions, width=2, alpha=0.5, edge_color="blue")
    EdgeLabels = {edge : f"{Weights[edge]}" for edge in G.edges()}
    HighlightedEdges = []
    for i in range(1, way.size + 1) :
        HighlightedEdges.append((way[i - 1] + 1, way[i % way.size] + 1))
    nx.draw_networkx_edges(G, Positions, edgelist=HighlightedEdges, edge_color="green", width=3)
    nx.draw_networkx_edge_labels(G, Positions, edge_labels=EdgeLabels, font_color="red")
    plt.title("Our Task Graph Visualisation")
    plt.axis("off")
    plt.show()
    return


def PaintVertexSetInNonWeightedGraph (matrix : np.array, vertex_list : np.array) -> None :
    G = nx.Graph()
    G.add_nodes_from(list(range(1, matrix.shape[0] + 1)))
    for i in range(matrix.shape[0]) :
        for j in range(i + 1, matrix.shape[0]) :
            if matrix[i][j] :
                G.add_weighted_edges_from([(i + 1, j + 1, matrix[i][j])])
    Positions = nx.spring_layout(G)
    for i in range(vertex_list.size) :
        vertex_list[i] += 1
    nx.draw_networkx_nodes(G, Positions, node_color="black", node_size=100)
    nx.draw_networkx_nodes(G, Positions, node_color="red", node_size=100, nodelist=vertex_list)
    nx.draw_networkx_edges(G, Positions, width=2, alpha=0.5, edge_color="blue")
    HighlightedEdges = []
    for i in range(vertex_list.size):
        for j in range(i + 1, vertex_list.size) :
            HighlightedEdges.append((vertex_list[i], vertex_list[j]))
    nx.draw_networkx_edges(G, Positions, edgelist=HighlightedEdges, edge_color="red", width=3)
    plt.title("Our Clique Visualisation")
    plt.axis("off")
    plt.show()
    return



def PaintVertexSetInWeightedGraph (matrix : np.array, vertex_list : np.array) -> None :
    G = nx.Graph()
    G.add_nodes_from(list(range(1, matrix.shape[0] + 1)))
    for i in range(matrix.shape[0]) :
        for j in range(i, matrix.shape[0]) :
            if matrix[i][j] :
                G.add_weighted_edges_from([(i + 1, j + 1, matrix[i][j])])
    Positions = nx.spring_layout(G)
    for i in range(vertex_list.size) :
        vertex_list[i] += 1
    nx.draw_networkx_nodes(G, Positions, node_color="black", node_size=100)
    nx.draw_networkx_nodes(G, Positions, node_color="red", node_size=150, nodelist=vertex_list)
    nx.draw_networkx_edges(G, Positions, width=2, alpha=0.5, edge_color="blue")
    HighlightedEdges = []
    for i in range(vertex_list.size):
        for j in range(i + 1, vertex_list.size) :
            HighlightedEdges.append((vertex_list[i], vertex_list[j]))
    nx.draw_networkx_edges(G, Positions, edgelist=HighlightedEdges, edge_color="red", width=3)
    Weights = nx.get_edge_attributes(G, "weight")
    EdgeLabels = {edge : f"{Weights[edge]}" for edge in G.edges()}
    nx.draw_networkx_edge_labels(G, Positions, edge_labels=EdgeLabels, font_color="black", font_size=7)
    plt.title("Our Clique Visualisation")
    plt.axis("off")
    plt.show()
    return