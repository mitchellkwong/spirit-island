from typing import Dict

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

class Network:
    def __init__(self, nodes, edges):
        self.nodes = nodes.sort_index()
        self.edges = edges.sort_index()
    
    def neighbours(self, nodes):
        edges = self.edges.reset_index()
        return set([
            *edges.loc[edges['source'].isin(nodes), 'target'],
            *edges.loc[edges['target'].isin(nodes), 'source'],
        ])
    
    def subset_edges(self, including=None, between=None, where=None):
        edges = self.edges.reset_index()
        
        mask = [True for _ in edges.index]
        if between is not None:
            mask &= edges['source'].isin(between) & edges['target'].isin(between)
        if including is not None:
            mask &= edges['source'].isin(including) | edges['target'].isin(including)
        if where is not None:
            mask &= edges.apply(where, axis=0)
            
        return self.edges.index[mask]
    
    def ego(self, nodes, degree=1.5):
        edges = self.edges.reset_index()
        
        ego_nodes = set(self.nodes.index[self.nodes.index.isin(nodes)])
        ego_edges = self.edges.index[[]]
        
        for _ in range(int(degree)):
            ego_edges = self.subset_edges(including=ego_nodes)
            ego_nodes = ego_nodes | self.neighbours(ego_nodes)
            
        if degree % 1:
            ego_edges = self.subset_edges(between=ego_nodes)
            
        cls = type(self)
        return cls(self.nodes.loc[ego_nodes], self.edges.loc[ego_edges])
    
class BoardState(Network):
    def __init__(self, nodes, edges):
        super().__init__(nodes, edges)
        
        # Try to find a nice network layout
        self.pos = nx.spring_layout(
            self.network, 
            iterations = 100, 
            pos = {
                # Defaults for thematic map
                ('northwest', 3): (0, 10),
                ('northeast', 1): (10, 10),
                ('west', 1): (0, 0), 
                ('east', 3): (10, 0), 
            },
            seed = 5,
        )
    
    def apply(self, action):
        """Apply an action to this board state and return a modified copy"""
        state = self.copy()
        state = action(state)
        return state
    
    def copy(self):
        """Deep copy of all game information"""
        nodes = self.nodes.copy()
        edges = self.edges.copy()
        return BoardState(nodes, edges)

    @property
    def network(self):
        board = nx.Graph()
        board.add_nodes_from(self.nodes.index)
        board.add_edges_from(self.edges.index)
        return board
    
    @property
    def invader_count(self):
        invaders = ['explorers', 'towns', 'cities']
        return self.nodes[invaders]
    
    @property
    def building_count(self):
        buildings = ['towns', 'cities']
        return self.nodes[buildings]
    
    @property
    def invader_sources(self):
        oceans = self.nodes['land'].isin(['O'])
        buildings = self.building_count.any(axis=1)
        return self.nodes.index[oceans|buildings]
    
    @property
    def invader_damage(self):
        ravagers = ['explorers', 'towns', 'cities', 'badlands', 'defence']
        damage = np.array([1, 2, 3, 1, -1])
        return self.nodes[ravagers] @ damage
    
    def draw(self, ax=None):
        blight_count = (self.nodes['blight'] > 0)
        invader_count = self.nodes[['explorers', 'towns', 'cities']].sum(axis=1)
    
        labels = self.nodes[['dahan', 'explorers', 'towns', 'cities', 'blight']]
        labels = {
            index: values if sum(values) > 0 else ''
            for index, *values in labels.itertuples()
        }
        
        colors = pd.Series({
            'O': '#3085AA',
            'J': '#538B56',
            'M': '#808080',
            'S': '#DFB674',
            'W': '#96C8CC',
        }).reindex(self.nodes['land'])
        
        # Plot
        nx.draw_networkx_edges(self.network, self.pos, alpha=0.2, ax=ax)
        nx.draw_networkx_nodes(self.network, self.pos, node_color='black', node_size=500*blight_count, ax=ax)
        nx.draw_networkx_nodes(self.network, self.pos, node_color=colors, ax=ax)
        nx.draw_networkx_nodes(self.network, self.pos, node_color='white', node_size=10*invader_count, ax=ax)
        
    def __repr__(self):
        plt.figure(figsize=(10, 7.5))
        self.draw()
        plt.axis('off')
        plt.show()
        return ''

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
nodes = pd.read_excel('data/nodes.xlsx', sheet_name=None)
edges = pd.read_excel('data/edges.xlsx', sheet_name=None)
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