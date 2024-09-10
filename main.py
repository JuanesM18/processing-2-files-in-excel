import streamlit as st
import pandas as pd
import mysql.connector

st.title('Processing two files to the database')

uploaded_file1 = st.file_uploader("Load the Vehicles Excel file", type=["xlsx", "xls"])

uploaded_file2 = st.file_uploader("Load the Costumers Excel file", type=["xlsx", "xls"])

if uploaded_file1 is not None and uploaded_file2 is not None:
    df_vehicles = pd.read_excel(uploaded_file1)
    df_costumers = pd.read_excel(uploaded_file2)

    st.write("**Contents of the Vehicles file:**")
    st.dataframe(df_vehicles)

    st.write("**Contents of the Costumers file:**")
    st.dataframe(df_costumers)

    merged_df = pd.merge(df_costumers, df_vehicles, left_on='Vehiculo', right_on='Referencia')

    st.write("**Combined data:**")
    st.dataframe(merged_df)
else:
    st.write("Please upload both Excel files.")