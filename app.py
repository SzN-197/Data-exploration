import streamlit as st
import requests
import tempfile
import os

API_URL = "http://localhost:8000"

st.title("Simple Network Visualization App")

mode = st.radio("Choose network input method:", ["Upload CSV edge list", "Generate random graph"])

if mode == "Upload CSV edge list":
    uploaded_file = st.file_uploader("Upload CSV with 'source','target' columns", type="csv")
else:
    n_nodes = st.slider("Number of nodes", min_value=5, max_value=100, value=20)
    p_edge = st.slider("Probability of edge (0-1)", min_value=0.0, max_value=1.0, value=0.2)

degree_threshold = st.slider("Filter nodes by minimum degree", min_value=0, max_value=10, value=0)
show_labels = st.checkbox("Show node labels", value=True)
highlight_hubs = st.checkbox("Highlight hubs (highest degree)", value=True)

if st.button("Load/Generate Graph"):
    if mode == "Upload CSV edge list":
        if uploaded_file is not None:
            files = {'file': (uploaded_file.name, uploaded_file.getvalue())}
            response = requests.post(f"{API_URL}/upload/", files=files)
        else:
            st.warning("Please upload a CSV file.")
            st.stop()
    else:
        params = {"n_nodes": n_nodes, "p_edge": p_edge}
        response = requests.get(f"{API_URL}/generate/", params=params)

    if response.status_code == 200:
        data = response.json()
        stats = data["stats"]
        html = data["html"]

        st.subheader("Network stats:")
        st.write(f"Number of nodes: {stats['num_nodes']}")
        st.write(f"Number of edges: {stats['num_edges']}")
        st.write("Degree distribution (node: degree):")
        st.write(stats['degree_distribution'])

        # Show network visualization
        # Save html temporarily to embed iframe
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        tmp_file.write(html.encode('utf-8'))
        tmp_file.close()

        st.components.v1.html(open(tmp_file.name, 'r').read(), height=650, scrolling=True)
        os.unlink(tmp_file.name)
    else:
        st.error("Error loading network from backend.")
