from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

load_dotenv()

st.title('Processing two files to the database')

def save_customers(df):
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        Name VARCHAR(255),
        ID VARCHAR(255),
        Email VARCHAR(255),
        PhoneNumber VARCHAR(255),
        Vehicle VARCHAR(255)
    )
    """)

    for index, row in df.iterrows():
        cursor.execute("""
        INSERT INTO customers (Name, ID, Email, PhoneNumber, Vehicle)
        VALUES (%s, %s, %s, %s, %s)
        """, (row['Nombre'], row['Cedula'], row['Correo'], row['Telefono'], row['Vehiculo']))

    conn.commit()
    cursor.close()
    conn.close()

    st.success("Customer data successfully saved to the database.")


def save_vehicles(df):
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (
        Reference VARCHAR(255),
        Year VARCHAR(12),
        Engine_Size VARCHAR(255),
        Buyer VARCHAR(255)
    )
    """)

    for index, row in df.iterrows():
        cursor.execute("""
        INSERT INTO vehicles (Reference, Year, Engine_Size, Buyer)
        VALUES (%s, %s, %s, %s)
        """, (row['Referencia'], row['Año'], row['Cilindraje'], row['Comprador']))

    conn.commit()
    cursor.close()
    conn.close()

    st.success("Vehicle data successfully saved to the database.")


uploaded_file1 = st.file_uploader("Upload the Vehicles Excel file", type=["xlsx", "xls"])

uploaded_file2 = st.file_uploader("Upload the Customers Excel file", type=["xlsx", "xls"])

if uploaded_file1 is not None and uploaded_file2 is not None:
    df_vehicles = pd.read_excel(uploaded_file1)
    df_customers = pd.read_excel(uploaded_file2)

    st.write("**Contents of the Vehicles file:**")
    st.dataframe(df_vehicles)

    st.write("**Contents of the Customers file:**")
    st.dataframe(df_customers)

    merged_df = pd.merge(df_customers, df_vehicles, left_on=['Vehiculo', 'Nombre'], right_on=['Referencia', 'Comprador'], how='left')

    st.write("**Combined data:**")
    st.dataframe(merged_df)

    if st.button("Save to database"):
        save_customers(df_customers)
        save_vehicles(df_vehicles)
else:
    st.write("Please upload both Excel files.")