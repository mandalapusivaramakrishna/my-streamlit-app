
import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="EV CAN Data Dashboard", layout="wide")
st.title("📊 EV CAN Data Analytics Dashboard")
st.markdown("Upload your CAN data Excel file to visualize key metrics such as SOC, SOH, voltage, current, and temperature over time.")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file:
    try:
        df_raw = pd.read_excel(uploaded_file, sheet_name=0)
        df_raw = df_raw.dropna(subset=["Timestamp", "Decoded Summary"])

        timestamps = []
        soc_list = []
        soh_list = []
        current_list = []
        temperature_list = []
        avg_voltage_list = []
        min_voltage_list = []
        max_voltage_list = []

        for _, row in df_raw.iterrows():
            ts = row['Timestamp']
            summary = row['Decoded Summary']

            soc = re.search(r'SOC[:=]?\s*([\d.]+)', str(summary))
            soh = re.search(r'SOH[:=]?\s*([\d.]+)', str(summary))
            curr = re.search(r'Current[:=]?\s*(-?[\d.]+)', str(summary))
            temp = re.search(r'Temperature[:=]?\s*([\d.]+)', str(summary))
            avg_v = re.search(r'Average Voltage[:=]?\s*([\d.]+)', str(summary))
            min_v = re.search(r'Min Voltage[:=]?\s*([\d.]+)', str(summary))
            max_v = re.search(r'Max Voltage[:=]?\s*([\d.]+)', str(summary))

            timestamps.append(ts)
            soc_list.append(float(soc.group(1)) if soc else None)
            soh_list.append(float(soh.group(1)) if soh else None)
            current_list.append(float(curr.group(1)) if curr else None)
            temperature_list.append(float(temp.group(1)) if temp else None)
            avg_voltage_list.append(float(avg_v.group(1)) if avg_v else None)
            min_voltage_list.append(float(min_v.group(1)) if min_v else None)
            max_voltage_list.append(float(max_v.group(1)) if max_v else None)

        df = pd.DataFrame({
            'Timestamp': timestamps,
            'SOC (%)': soc_list,
            'SOH (%)': soh_list,
            'Current (A)': current_list,
            'Temperature (°C)': temperature_list,
            'Avg Voltage (V)': avg_voltage_list,
            'Min Voltage (V)': min_voltage_list,
            'Max Voltage (V)': max_voltage_list
        })

        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
        df = df.dropna(subset=['Timestamp'])
        df = df.sort_values('Timestamp')

        st.subheader("📈 Time-Series Graphs")
        metrics = ['SOC (%)', 'SOH (%)', 'Current (A)', 'Temperature (°C)', 'Avg Voltage (V)', 'Min Voltage (V)', 'Max Voltage (V)']
        for metric in metrics:
            if df[metric].notnull().sum() > 0:
                st.line_chart(data=df.set_index('Timestamp')[metric], use_container_width=True)

        with st.expander("📄 View Raw Extracted Data"):
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Failed to process file: {e}")
else:
    st.info("Please upload a CAN data Excel file to continue.")
