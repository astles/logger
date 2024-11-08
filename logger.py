# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go

# # Streamlit page settings
# st.set_page_config(page_title="Open PO Analysis", layout="centered")

# st.title("Open Purchase Orders Analysis")
# st.write("Upload a CSV file to analyze open POs for 2024 by vendor and total amount.")

# # File uploader for CSV
# uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

# if uploaded_file:
#     # Load the data
#     df = pd.read_csv(uploaded_file)

#     # Filter for open POs
#     open_pos = df[df['Closed_Code'] != 'CLOSED'].copy()

#     # Convert the Distribution_Creation_Date to datetime format
#     open_pos['Distribution_Creation_Date'] = pd.to_datetime(open_pos['Distribution_Creation_Date'], errors='coerce')

#     # Filter for POs created in 2024
#     open_pos_2024 = open_pos[open_pos['Distribution_Creation_Date'].dt.year == 2024].copy()

#     # Calculate Total Open Price
#     open_pos_2024['Total_Open_Price'] = (open_pos_2024['Unit_Price'] * 
#                                          (open_pos_2024['Quantity_Ordered'] - open_pos_2024['Quantity_Delivered']) 
#                                          - open_pos_2024['Amount_Billed'])

#     # Calculate total amount for open POs in 2024
#     total_open_amount_2024 = open_pos_2024['Total_Open_Price'].sum()

#     # Group by Vendor_Name and sum Total_Open_Price
#     vendor_totals = open_pos_2024.groupby('Vendor_Name')['Total_Open_Price'].sum().reset_index()
#     vendor_totals = vendor_totals.sort_values(by='Total_Open_Price', ascending=False)

#     # Add a row for the grand total
#     grand_total_row = pd.DataFrame({'Vendor_Name': ['Total'], 'Total_Open_Price': [vendor_totals['Total_Open_Price'].sum()]})
#     vendor_totals = pd.concat([vendor_totals, grand_total_row], ignore_index=True)

#     # Display the results
#     st.subheader("Summary of Open PO Amounts by Vendor for 2024")

#     # Plotly table
#     table_fig = go.Figure(data=[go.Table(
#         header=dict(values=["<b>Vendor</b>", "<b>Total Open Price</b>"],
#                     fill_color='lightgrey',
#                     align='center',
#                     font=dict(color='black', size=14)),
#         cells=dict(values=[vendor_totals['Vendor_Name'], vendor_totals['Total_Open_Price']],
#                    fill_color='white',
#                    align='center',
#                    font=dict(color='black', size=12),
#                    format=[None, "$,.2f"]))
#     ])

#     table_fig.update_layout(width=700, height=400)
#     st.plotly_chart(table_fig)

#     # Plot bar chart for vendor totals
#     st.subheader("Total Amount of Open POs by Vendor for 2024")
#     fig = px.bar(vendor_totals[:-1], x='Vendor_Name', y='Total_Open_Price', 
#                  title="Total Amount of Open POs by Vendor for 2024",
#                  labels={'Vendor_Name': 'Vendor', 'Total_Open_Price': 'Total Open Price'},
#                  text='Total_Open_Price')

#     fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
#     fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', width=700, height=400)
#     st.plotly_chart(fig)

#     # Display the total sum of open orders as an indicator
#     st.subheader("Overall Total of Open Orders for 2024")
#     total_indicator = go.Figure(go.Indicator(
#         mode="number",
#         value=total_open_amount_2024,
#         number={'prefix': "$", 'font': {'size': 36}},
#         title={'text': "Total Amount of Open POs for 2024"},
#         domain={'x': [0, 1], 'y': [0, 1]}
#     ))

#     total_indicator.update_layout(height=250, width=400)
#     st.plotly_chart(total_indicator)
# else:
#     st.info("Please upload a CSV file to proceed.")

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Set up Streamlit page configuration
st.set_page_config(page_title="Open POs by Vendor", layout="wide")

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

    # Calculate total open PO amounts per vendor
    vendor_totals = vendor_data.groupby('Vendor_Name')['Total_Pending_Amount'].sum().reset_index()
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

    # Detailed breakdown of open POs for the selected vendor
    breakdown_data = vendor_data[['Vendor_Name', 'Item_Description', 'PO_Number', 'Quantity_Pending', 'Promised_Date']]
    
    # Display breakdown table for the selected vendor
    st.subheader(f"Breakdown of Open POs for Vendor: {selected_vendor}")
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
    total_open_amount = vendor_data['Total_Pending_Amount'].sum()
    st.subheader("Total Sum of All Open Orders")
    st.write(f"**${total_open_amount:,.2f}**")
