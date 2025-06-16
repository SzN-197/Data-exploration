# Simple Network Visualization App
Built with:
- [Streamlit](https://streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [NetworkX](https://networkx.org/) and [Pyvis](https://pyvis.readthedocs.io/)
---

## How it works
- Upload a CSV file containing an edge list (`source`, `target`), or
- Generate a random graph (Erdős–Rényi model)
- From there, you can use the following functions:
  - Interactive graph visualization
  - Basic network stats: number of nodes/edges, degree distribution
  - Filter nodes by minimum degree
  - Option to toggle node labels
  - Highlight hub nodes (highest degree)

## Requirements
Install dependencies using pip:

`pip install fastapi uvicorn streamlit pandas networkx pyvis requests`

## How to run
In two separate command prompts:
1. Move to the file folder(s), then
2. 1.
   `uvicorn backend:app --reload`
2. 2.
   `streamlit run app.py`
