# forecast.py
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np

def loaddata(path="internet_usage_sample.csv"):
    df = pd.read_csv(path, parse_dates=['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day'] = df['timestamp'].dt.day_name()
    return df

def train_forecast_model(df):
    df_grouped = df.groupby(df['hour'])['data_mb'].sum().reset_index()
    x = df_grouped[['hour']]
    y = df_grouped[['data_mb']]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    model = LinearRegression()
    model.fit(x_train, y_train)
    return model

def predict_usage(model, hrs):
    return model.predict(np.array(hrs).reshape(-1, 1))
