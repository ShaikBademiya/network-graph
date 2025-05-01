from pyvis.network import Network
import networkx as nx
import pandas as pd

def get_graph(routes, source, target):
    G = nx.from_pandas_edgelist(
        # routes.head(1000),
        routes.sample(1000),
        source=source,
        target=target
    )

    node_degree = dict(G.degree)

    node_size = {k: ((v // 5 + 2) * 10) for k, v in node_degree.items()}

    nx.set_node_attributes(G, node_size, 'size')
    nx.set_node_attributes(G, node_degree, 'group')

    title_dict = {key: key for key in G.nodes()}
    nx.set_node_attributes(G, title_dict, 'title')

    return G

def get_net():
    net = Network(
        notebook=False,
        cdn_resources='remote',
        height='800px',
        width='100%',
        directed = True,
        neighborhood_highlight=True,
        # select_menu=True,
    )

    ## you can either show buttons, or set options
    # net.show_buttons(filter_="physics")

    net.barnes_hut(
        gravity=-5000,
        central_gravity=0.1,
        spring_length=200,
        spring_strength=0.01,
        overlap=0.5,
    )

    # net.force_atlas_2based(
    #     gravity=-200,
    #     central_gravity=0.02,
    #     spring_length=200,
    #     overlap=0.5,
    # )

    return net

def main():
    # Read CSV
    routes = pd.read_csv("routes.csv")

    # Declare source and target for the graph
    source = 'source airport'
    target = 'destination airport'

    # Create graph using CSV
    graph = get_graph(routes, source, target)

    # Get network object
    net = get_net()

    # Add graph details to the net
    net.from_nx(graph)

    # Create a html for the net
    net.show("routes_net.html", notebook=False)

    # For github pages
    net.show("index.html", notebook=False)


if __name__ == "__main__":
    main()
