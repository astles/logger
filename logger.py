import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Streamlit page settings
st.set_page_config(page_title="Open PO Analysis", layout="centered")

st.title("Open Purchase Orders Analysis")
st.write("Upload a CSV file to analyze open POs for 2024 by vendor and total amount.")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file:
    # Load the data
    df = pd.read_csv(uploaded_file)

    # Filter for open POs
    open_pos = df[df['Closed_Code'] != 'CLOSED'].copy()

    # Convert the Distribution_Creation_Date to datetime format
    open_pos['Distribution_Creation_Date'] = pd.to_datetime(open_pos['Distribution_Creation_Date'], errors='coerce')

    # Filter for POs created in 2024
    open_pos_2024 = open_pos[open_pos['Distribution_Creation_Date'].dt.year == 2024].copy()

    # Calculate Total Open Price
    open_pos_2024['Total_Open_Price'] = (open_pos_2024['Unit_Price'] * 
                                         (open_pos_2024['Quantity_Ordered'] - open_pos_2024['Quantity_Delivered']) 
                                         - open_pos_2024['Amount_Billed'])

    # Calculate total amount for open POs in 2024
    total_open_amount_2024 = open_pos_2024['Total_Open_Price'].sum()

    # Group by Vendor_Name and sum Total_Open_Price
    vendor_totals = open_pos_2024.groupby('Vendor_Name')['Total_Open_Price'].sum().reset_index()
    vendor_totals = vendor_totals.sort_values(by='Total_Open_Price', ascending=False)

    # Add a row for the grand total
    grand_total_row = pd.DataFrame({'Vendor_Name': ['Total'], 'Total_Open_Price': [vendor_totals['Total_Open_Price'].sum()]})
    vendor_totals = pd.concat([vendor_totals, grand_total_row], ignore_index=True)

    # Display the results
    st.subheader("Summary of Open PO Amounts by Vendor for 2024")

    # Plotly table
    table_fig = go.Figure(data=[go.Table(
        header=dict(values=["<b>Vendor</b>", "<b>Total Open Price</b>"],
                    fill_color='lightgrey',
                    align='center',
                    font=dict(color='black', size=14)),
        cells=dict(values=[vendor_totals['Vendor_Name'], vendor_totals['Total_Open_Price']],
                   fill_color='white',
                   align='center',
                   font=dict(color='black', size=12),
                   format=[None, "$,.2f"]))
    ])

    table_fig.update_layout(width=700, height=400)
    st.plotly_chart(table_fig)

    # Plot bar chart for vendor totals
    st.subheader("Total Amount of Open POs by Vendor for 2024")
    fig = px.bar(vendor_totals[:-1], x='Vendor_Name', y='Total_Open_Price', 
                 title="Total Amount of Open POs by Vendor for 2024",
                 labels={'Vendor_Name': 'Vendor', 'Total_Open_Price': 'Total Open Price'},
                 text='Total_Open_Price')

    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', width=700, height=400)
    st.plotly_chart(fig)

    # Display the total sum of open orders as an indicator
    st.subheader("Overall Total of Open Orders for 2024")
    total_indicator = go.Figure(go.Indicator(
        mode="number",
        value=total_open_amount_2024,
        number={'prefix': "$", 'font': {'size': 36}},
        title={'text': "Total Amount of Open POs for 2024"},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))

    total_indicator.update_layout(height=250, width=400)
    st.plotly_chart(total_indicator)
else:
    st.info("Please upload a CSV file to proceed.")
