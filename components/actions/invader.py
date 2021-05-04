import numpy as np

class InvaderAction:
    def __init__(self, lands):
        self.lands = lands
    
    def __str__(self):
        return '+'.join(self.lands) + ' ' + type(self).__name__
    
class Explore(InvaderAction):
    def __call__(self, state):
        nodes = state.nodes
        edges = state.edges.reset_index()
        
        # Identify matching lands
        matches = nodes['land'].isin(self.lands)
        matches = nodes[matches]
        
        # Trivial explores (explorers already present)
        trivial = matches['explorers'] > 0
        trivial = matches[trivial]
        shortlisted = set(trivial.index)

        # Non-trivial explores
        oceans = nodes['land'] == 'O'
        buildings = nodes[['towns', 'cities']].any(axis=1)
        start = nodes[oceans|buildings]
        candidates = set([
            *edges.loc[edges['source'].isin(start.index), 'target'],
            *edges.loc[edges['target'].isin(start.index), 'source'],
            *start.index,
        ])
        shortlisted = shortlisted | (candidates & set(matches.index))
                
        # Add explorers
        state.nodes.loc[shortlisted, 'explorers'] += 1
        
        return state
    
class Build(InvaderAction):
    def __call__(self, state):
        nodes = state.nodes
        
        # Identify matching lands
        matches = nodes['land'].isin(self.lands) & nodes[['explorers', 'towns', 'cities']].any(axis=1)
        
        # Classify builds
        add_city = nodes['cities'] < nodes['towns']        
        add_town = ~add_city

        # Add buildings
        state.nodes.loc[matches & add_city, 'cities'] += 1
        state.nodes.loc[matches & add_town, 'towns'] += 1
        
        return state
    
class Ravage(InvaderAction):
    def __call__(self, state):
        nodes = state.nodes
        
        # Identify matching lands
        matches = nodes['land'].isin(self.lands)
        
        # Calculate damage and blight
        damage = nodes[['explorers', 'towns', 'cities', 'defence']] @ np.array([1, 2, 3, -1])
        nodes.loc[matches & (damage > 1), 'blight'] += 1
        
        # Dahan fight back
        nodes.loc[matches, 'dahan'] -= damage//2
        nodes['dahan'] = np.maximum(0, nodes['dahan']).astype(int)
        dahan_damage = 2*nodes['dahan']
        
        attack_cities = matches & (dahan_damage >= 3) & (nodes['cities'] > 0)
        while attack_cities.any():
            dahan_damage[attack_cities] -= 3
            nodes.loc[attack_cities, 'cities'] -= 1
            attack_cities = matches & (dahan_damage >= 3) & (nodes['cities'] > 0)
        
        attack_towns = matches & (dahan_damage >= 2) & (nodes['towns'] > 0)
        while attack_towns.any():
            dahan_damage[attack_towns] -= 2
            nodes.loc[attack_towns, 'towns'] -= 1
            attack_towns = matches & (dahan_damage >= 2) & (nodes['towns'] > 0)
        
        attack_explorers = matches & (dahan_damage >= 1) & (nodes['explorers'] > 0)
        while attack_explorers.any():
            dahan_damage[attack_explorers] -= 1
            nodes.loc[attack_explorers, 'explorers'] -= 1
            attack_explorers = matches & (dahan_damage >= 1) & (nodes['explorers'] > 0)
        
        state.nodes = nodes
        return state