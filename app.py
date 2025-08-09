# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

from forecast import loaddata, predict_usage, train_forecast_model
from analyzer import detect_anomalies
from recommender import generate_recommendations

st.set_page_config(page_title="Internet Usage Analyzer")
st.title("Internet Data (MB) Dashboard")

tab1, tab2 = st.tabs(["Dashboard", "Assistant Bot"])

with tab1:
    uploaded_file = st.file_uploader("Upload Internet Usage CSV", type=['csv'])
    if uploaded_file:
        df = loaddata(uploaded_file)
        if not {'timestamp', 'device', 'application', 'data_mb'}.issubset(df.columns):
            st.error("CSV must contain: timestamp, device, application, data_mb")
            st.stop()

        st.subheader("Total Data (MB) by Application")
        app_data = df.groupby("application")["data_mb"].sum().sort_values(ascending=False).reset_index()
        st.bar_chart(app_data.set_index('application'))

        st.subheader("Device-wise Data (MB) Distribution (Pie Chart)")
        device_data = df.groupby("device")["data_mb"].sum()
        fig, ax = plt.subplots()
        ax.pie(device_data, labels=device_data.index, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')
        st.pyplot(fig)

        st.subheader("Heatmap: Day vs Hour (Data in MB)")
        df['day'] = pd.Categorical(df['day'], categories=[
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
        ], ordered=True)
        heatmap_data = df.pivot_table(index='day', columns='hour', values='data_mb', aggfunc='sum').fillna(0)
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt=".1f", linewidths=0.3, ax=ax)
        st.pyplot(fig)

        st.subheader("Forecasting Next 24 Hours (Predicted Data in MB)")
        model = train_forecast_model(df)
        forecast = predict_usage(model, list(range(24)))
        forecast_df = pd.DataFrame({'Hour': list(range(24)), 'Predicted_MB': forecast.flatten()})
        st.line_chart(forecast_df.set_index("Hour"))

        st.subheader("Anomaly Detection")
        anomalies = detect_anomalies(df)
        st.dataframe(anomalies[anomalies['anomaly'] == -1])

        st.subheader("Data (MB) Recommendations")
        for rec in generate_recommendations(df):
            st.info(rec)

with tab2:
    st.title("Internet Data (MB) Assistant")
    user_input = st.text_input("Ask me about saving data!")
    if user_input:
        st.write("This feature will be powered soon...")
    

