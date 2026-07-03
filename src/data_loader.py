import pandas as pd

def load_data(filepath):
    """
    Load the global superstore dataset
    """
    df = pd.read_csv(filepath, encoding="latin1")
    return df