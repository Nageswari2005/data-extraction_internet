# recommender.py
def generate_recommendations(df):
    res = []
    avg_usage = df['data_mb'].mean()
    max_usage = df['data_mb'].max()

    if avg_usage > 100:
        res.append("Consider optimizing background app data usage.")
    if max_usage > 300:
        res.append("Check for high-consumption apps or downloads.")
    if 'Zoom' in df['application'].unique():
        res.append("Zoom usage detected – use with WiFi to save data.")
    
    return res
