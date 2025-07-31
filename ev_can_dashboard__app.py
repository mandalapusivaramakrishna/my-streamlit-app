import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🔋 EV CAN Data Dashboard")

st.markdown("Upload your CAN data Excel file to visualize key metrics such as SOC, SOH, voltage, current, and temperature over time.")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Show raw data
        with st.expander("📄 View Raw Extracted Data"):
            st.write(df)

        # Convert Timestamp column to datetime
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

        st.subheader("📈 Time-Series Graphs")

        def plot_metric(y_col, y_label):
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(df['Timestamp'], df[y_col], label=y_label)
            ax.set_xlabel("Time")
            ax.set_ylabel(y_label)
            ax.set_title(f"{y_label} Over Time")
            ax.legend()
            st.pyplot(fig)

        # Plot each metric
        plot_metric("SOC", "SOC (%)")
        plot_metric("SOH", "SOH (%)")
        plot_metric("Current", "Current (A)")
        plot_metric("Temperature", "Temperature (°C)")
        plot_metric("Voltage Min", "Min Voltage (V)")
        plot_metric("Voltage Max", "Max Voltage (V)")

    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload a valid Excel file.")
