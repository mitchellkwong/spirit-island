from typing import Dict
import pandas as pd
from components.states.board import BoardState

def prepare_data(
    boards: Dict[str, pd.DataFrame], 
    adjacency: Dict[str, pd.DataFrame],
):
    board_data = ['board', 'id']
    setup_data = [
        'dahan', 'explorers', 'towns', 'cities', 'blight', 
        'beasts', 'wilds', 'disease', 'strife', 'badlands',
    ]
    
    nodes = list()
    for name, df in boards.items():
        df['defence'] = 0
        df[board_data] = df[board_data].ffill()
        df[setup_data] = df[setup_data].fillna(0).astype(int)
        df['node'] = list(zip(df['board'], df['id']))
        df = df.set_index('node')
        nodes.append(df)
    nodes = pd.concat(nodes)
    
    edges = list()
    for name, df in adjacency.items():
        df = df.ffill().astype(int, errors='ignore')
        df['source'] = list(zip(df['source_board'], df['source_id']))
        df['target'] = list(zip(df['target_board'], df['target_id']))
        df = df.set_index(['source', 'target'])
        edges.append(df)
    edges = pd.concat(edges)
    
    return nodes, edges

# Read data from excel database
nodes = pd.read_excel('data/nodes.xlsx', sheet_name=None, engine='openpyxl')
edges = pd.read_excel('data/edges.xlsx', sheet_name=None, engine='openpyxl')
nodes = pd.Series(nodes)
edges = pd.Series(edges)

# Load base game maps
thematic = BoardState(*prepare_data(nodes[['northwest', 'northeast', 'west', 'east']], edges[['northwest', 'northeast', 'west', 'east', 'thematic']]))
northwest = BoardState(*prepare_data(nodes[['northwest']], edges[['northwest']]))
northeast = BoardState(*prepare_data(nodes[['northeast']], edges[['northeast']]))
west = BoardState(*prepare_data(nodes[['west']], edges[['west']]))
east = BoardState(*prepare_data(nodes[['east']], edges[['east']]))
A = BoardState(*prepare_data(nodes[['A']], edges[['A']]))
B = BoardState(*prepare_data(nodes[['B']], edges[['B']]))
C = BoardState(*prepare_data(nodes[['C']], edges[['C']]))
D = BoardState(*prepare_data(nodes[['D']], edges[['D']]))