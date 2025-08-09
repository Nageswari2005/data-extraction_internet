# analyzer.py
from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    daily = df.groupby(df['timestamp'].dt.date)['data_mb'].sum().reset_index()
    model = IsolationForest(contamination=0.05)
    daily['anomaly'] = model.fit_predict(daily[['data_mb']])
    return daily
