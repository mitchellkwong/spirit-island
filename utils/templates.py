import pandas as pd

def resource_table():
    return pd.DataFrame(
        data = {'amount': 0, 'change': 0},
        index = [
            'presence', 'energy', 'card_plays', 
            'sun', 'moon', 'fire', 
            'air', 'water', 'earth', 
            'plant', 'animal',
        ]
    )