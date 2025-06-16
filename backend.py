from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import networkx as nx
import pandas as pd
from io import StringIO
import random
from pyvis.network import Network

app = FastAPI()

# Allow CORS for local Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def graph_to_html(net: Network):
    return net.generate_html()

@app.post("/upload/")
async def upload_edges(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(StringIO(contents.decode()))
    # Expect columns: source,target (simple edge list)
    G = nx.from_pandas_edgelist(df, source='source', target='target')
    return get_graph_response(G)

@app.get("/generate/")
def generate_graph(n_nodes: int = Query(10, ge=2, le=100), p_edge: float = Query(0.2, ge=0, le=1)):
    # Generate random Erdos-Renyi graph
    G = nx.erdos_renyi_graph(n_nodes, p_edge)
    return get_graph_response(G)

def get_graph_response(G: nx.Graph, degree_threshold: int = 0, show_labels: bool = True, highlight_hubs: bool = True):
    # Filter nodes by degree threshold
    filtered_nodes = [n for n, d in G.degree() if d >= degree_threshold]
    H = G.subgraph(filtered_nodes).copy()

    # Create pyvis network
    net = Network(height="600px", width="100%", notebook=False)
    net.from_nx(H)

    if not show_labels:
        for node in net.nodes:
            node['label'] = ''

    if highlight_hubs:
        max_degree = max(dict(H.degree()).values()) if H.number_of_nodes() > 0 else 0
        for node in net.nodes:
            if H.degree(node['id']) == max_degree and max_degree > 0:
                node['color'] = 'red'
            else:
                node['color'] = 'blue'

    # Stats
    stats = {
        'num_nodes': H.number_of_nodes(),
        'num_edges': H.number_of_edges(),
        'degree_distribution': dict(H.degree()),
    }

    html = net.generate_html()

    return {
        "stats": stats,
        "html": html
    }

@app.get("/filter/")
def filter_graph(degree_threshold: int = 0, show_labels: bool = True, highlight_hubs: bool = True):
    # For simplicity, just generate a default random graph and filter it here
    G = nx.erdos_renyi_graph(20, 0.2)
    return get_graph_response(G, degree_threshold, show_labels, highlight_hubs)
