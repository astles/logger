import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Set up Streamlit page configuration
st.set_page_config(page_title="Open POs by Vendor and PO", layout="wide")

# Title
st.title("Open Purchase Orders Dashboard")

# Upload file section
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

# Process the file if uploaded
if uploaded_file:
    # Read Excel file
    df = pd.read_excel(uploaded_file, engine='openpyxl')

    # Calculate quantity pending and total pending amount for open POs
    df['Quantity_Pending'] = df['Quantity_Ordered'] - df['Quantity_Delivered']
    df['Total_Pending_Amount'] = df['Unit_Price'] * df['Quantity_Pending'] - df['Amount_Billed']

    # Filter for open POs based on 'Closed_Code' and 'Open_Flag'
    open_pos = df[(df['Closed_Code'] != 'CLOSED') & (df['Open_Flag'] == 'Y')]

    # Vendor selection
    vendors = ['All Vendors'] + sorted(open_pos['Vendor_Name'].unique().tolist())
    selected_vendor = st.selectbox("Select a Vendor", vendors)

    # Filter data based on selected vendor
    if selected_vendor != 'All Vendors':
        vendor_data = open_pos[open_pos['Vendor_Name'] == selected_vendor]
    else:
        vendor_data = open_pos

    # PO selection (filtered by selected vendor if applicable)
    po_numbers = ['All POs'] + sorted(vendor_data['PO_Number'].unique().tolist())
    selected_po = st.selectbox("Select a PO Number", po_numbers)

    # Further filter data based on selected PO number
    if selected_po != 'All POs':
        po_data = vendor_data[vendor_data['PO_Number'] == selected_po]
    else:
        po_data = vendor_data

    # Calculate total open PO amounts per vendor
    vendor_totals = po_data.groupby('Vendor_Name')['Total_Pending_Amount'].sum().reset_index()
    vendor_totals.columns = ['Vendor_Name', 'Total_Open_PO_Amount']

    # Display total open PO amount for each vendor in a table
    st.subheader("Total Open PO Amount by Vendor")
    st.plotly_chart(go.Figure(data=[go.Table(
        header=dict(values=["<b>Vendor</b>", "<b>Total Open PO Amount</b>"],
                    fill_color='lightgrey',
                    align='center'),
        cells=dict(values=[vendor_totals['Vendor_Name'], vendor_totals['Total_Open_PO_Amount']],
                   fill_color='white',
                   align='center'))
    ]))

    # Display bar chart for total open PO amounts by vendor
    st.subheader("Total Open Amount by Vendor")
    bar_fig = px.bar(vendor_totals, x='Vendor_Name', y='Total_Open_PO_Amount', title="Total Open Amount by Vendor")
    bar_fig.update_layout(xaxis_title="Vendor", yaxis_title="Total Open Amount")
    st.plotly_chart(bar_fig)

    # Detailed breakdown of open POs for the selected vendor and PO number
    breakdown_data = po_data[['Vendor_Name', 'Item_Description', 'PO_Number', 'Quantity_Pending', 'Promised_Date']]
    
    # Display breakdown table for the selected vendor and PO number
    st.subheader(f"Breakdown of Open POs for Vendor: {selected_vendor} and PO: {selected_po}")
    st.plotly_chart(go.Figure(data=[go.Table(
        header=dict(values=["<b>Vendor</b>", "<b>Item Description</b>", "<b>PO Number</b>", "<b>Quantity Pending</b>", "<b>Promised Date</b>"],
                    fill_color='lightgrey',
                    align='center'),
        cells=dict(values=[breakdown_data['Vendor_Name'],
                           breakdown_data['Item_Description'],
                           breakdown_data['PO_Number'],
                           breakdown_data['Quantity_Pending'],
                           breakdown_data['Promised_Date']],
                   fill_color='white',
                   align='center'))
    ]))

    # Display total sum of all open orders
    total_open_amount = po_data['Total_Pending_Amount'].sum()
    st.subheader("Total Sum of All Open Orders")
    st.write(f"**${total_open_amount:,.2f}**")
