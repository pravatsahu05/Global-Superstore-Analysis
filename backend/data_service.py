from src.data_loader import load_data
from src.preprocessing import clean_data, feature_engineering

def get_processed_data():

    df = load_data("data/global_superstore.csv")
    df = clean_data(df)
    df = feature_engineering(df)

    return df