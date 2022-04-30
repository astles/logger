
# 1 --- first and foremost, we import the necessary libraries
import pandas as pd
import streamlit as st
import plotly.express as px
# import plotly.figure_factory as ff
# import numpy as np


#######################################





# 2 --- you can add some css to your Streamlit app to customize it
# TODO: Change values below and observer the changes in your app
st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 90%;
        padding-top: 5rem;
        padding-right: 5rem;
        padding-left: 5rem;
        padding-bottom: 5rem;
    }}
    img{{
    	max-width:40%;
    	margin-bottom:40px;
    }}
</style>
""",
        unsafe_allow_html=True,
    )
#######################################






# 3 --- build the structure of your app


# Streamlit apps can be split into sections


# container -> horizontal sections
# columns -> vertical sections (can be created inside containers or directly in the app)
# sidebar -> a vertical bar on the side of your app


# here is how to create containers
header_container = st.container()
stats_container = st.container()
pie_container = st.container()
other_container = st.container()
column = st.container()
#######################################



# You can place things (titles, images, text, plots, dataframes, columns etc.) inside a container
with header_container:

	# for example a logo or a image that looks like a website header
	#st.image('logo.png')

	# different levels of text you can include in your app
	st.title("LogView")
	st.header("What the printer is doing!")
	st.subheader("")
	st.write("Just load your file")








# Another container
#with stats_container:
#placeholder = st.empty()
#placeholder.title("Log mapper")

with stats_container:

    uploaded_file = st.file_uploader("Upload CSV", type=".csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        st.markdown("#### Data preview")
        st.dataframe(df.head())

      #  ab = st.multiselect("A/B column", options=df.columns)
    # if ab:
    #     control = df[ab[0]].unique()[0]
    #     treatment = df[ab[0]].unique()[1]
    #     decide = st.radio(f"Is {treatment} Variant B?", options=["Yes", "No"])
    #     if decide == "No":
    #         control, treatment = treatment, control
    #     visitors_a = df[ab[0]].value_counts()[control]
    #     visitors_b = df[ab[0]].value_counts()[treatment]

with other_container:

    st.header("CNF Reading 2")
    fig = px.scatter(data_frame=df, x='  time(sec)', y=' reading 2', color=
        ' type', symbol=None, size=None, trendline=None, marginal_x='histogram',
        marginal_y='histogram', facet_row=None, facet_col=None, render_mode=
        'auto', )
    fig.update()
    fig


with column:

    # 7 --- creating columns inside a container
    #		(you can create more than 2)
    bar_col, pie_col = st.columns(2)

    # preparing data to display in a bar chart
    ttime = df['  time(sec)'].value_counts()

    # don't forget to add titles to your plots
    bar_col.subheader('Total Print Time')
    bar_col.metric("total time", value=266)


    #pie_col.print ttime
    st.header("Time Ratios")

   # PLOT TITLE
    pie_col.subheader('Breakdown')

    # pie chart
    fig2 = px.pie(data_frame=df, names=' type', values='  time(sec)', color=None,
                  )
    fig2
    pie_col.write(fig2)



    # TODO: change the values of the update_layout function and see the effect
    fig2.update_layout(showlegend=False,
                      width=400,
                      height=400,
                      margin=dict(l=1, r=1, b=1, t=1),
                      font=dict(color='#383635', size=15))

    # this function adds labels to the pie chart
    # for more information on this chart, visit: https://plotly.com/python/pie-charts/
    fig2.update_traces(textposition='inside', textinfo='percent+label')

   
