from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import networkx as nx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

class PipelineRequest(BaseModel):
    nodes: List[Dict] 
    edges: List[Dict] 

@app.post("/pipelines/parse")
async def parse_pipeline(request: PipelineRequest):
    print(request)
    nodes = request.nodes
    edges = request.edges

    G = nx.DiGraph()

    for node in nodes:
        G.add_node(node['id'])

    for edge in edges:
        G.add_edge(edge['source'], edge['target'])

    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()

    is_dag = nx.is_directed_acyclic_graph(G)

    return {"num_nodes": num_nodes, "num_edges": num_edges, "is_dag": is_dag}
