# dataextraction.py
import pandas as pd

def preprocess_data(path="internet_usage_sample.csv"):
    df = pd.read_csv(path, parse_dates=['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day'] = df['timestamp'].dt.day_name()
    return df
