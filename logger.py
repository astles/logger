
# 1 --- first and foremost, we import the necessary libraries
import pandas as pd
import streamlit as st
import plotly.express as px
import os
# import plotly.figure_factory as ff
# import numpy as np

st.set_page_config(layout="wide")
#######################################





# 2 CSS
# TODO: MODIFY CSS
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






# APP STRUCTURE


# Streamlit split into sections


# container -> horizontal sections
# columns -> vertical sections (can be created inside containers or directly in the app)
# sidebar -> a vertical bar on the side of your app


# here is how to create containers
header_container = st.container()
stats_container = st.container()
printNumbers = st.container()
# printTime = st.container()
pie_container = st.container()
conf_reading = st.container()
other_container = st.container()
column = st.container()

#######################################



# You can place things (titles, images, text, plots, dataframes, columns etc.) inside a container
with header_container:

	# ADD LOGO
	#st.image('logo.png')

	## TEXT SIZES
	st.title("LogView")
	# st.header("What the printer is doing!")
	st.subheader("")
	#st.write("Just load your file")


# Another container
#with stats_container:
#placeholder = st.empty()
#placeholder.title("Log mapper")


#### TESTING LOADED FILE
@st.cache
def load_data():
    #df = pd.read_csv("data/cprint.csv")

    # the absoulte path of the file
    #file_path = r"FilePath"
    # get the filename
    print(os.path.basename(file_path))
    #df = pd.read_excel("/Mylocation/TWS Data.xlsx")
    # df=df[df['Price']>0]
    #conlog = df
    #return conlog


#conlog = load_data()

### FILE LOADING
st.sidebar.title("Load Your Files")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=".csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    conlog = df
    st.markdown("#### Data preview")
    st.dataframe(df.head())
    # the absoulte path of the file
    file_path = r"FilePath"

    # get the filename
    print(os.path.basename(file_path))
    print(os.path.basename(file_path))
    confFileName = os.path.basename(file_path)
with stats_container:

## ADD FILE NAME FROM LOAD FILE
    # def file_selector(folder_path='.'):
    #     filenames = os.listdir(folder_path)
    #     selected_filename = st.selectbox('Select a file', filenames)
    #     return os.path.join(folder_path, selected_filename)
    #
    # filename = file_selector()
    # st.write('You selected `%s`' % filename)



### NEW DATA


# st.dataframe(df.style.highlight_max(axis=0))
#ADDING SIDE BAR SLIDER
# Sidebar = Layer Range
#     min_layer = int(conlog['  layer'].min())
#     max_layer = int(conlog['  layer'].max())
#     strtLayer = int(st.sidebar.text_input('Start Layer', '1'))
#     endLayer = int(st.sidebar.text_input('End Layer', '5'))
#
#     selected_layer_range = st.sidebar.slider('Select the layer range', 0, 999, (strtLayer, endLayer), 1)
#     st.write('Range Values', selected_layer_range)
#
# # Filtering data
#     df_selected_model = conlog[(conlog['  layer'].between(selected_layer_range[0], selected_layer_range[1]))]
#     st.header('Confocal Data')
#     st.dataframe(df_selected_model)
###########







#with other_container:



    # # Slider2
    # sld_time = st.slider('  time(sec)', 1, 100)
    #
    # st.write("You selected {}".format(sld_time))
    #
    # st.subheader("Slider")
    # slider_range = st.slider("Seconds range", value=[000, 400])
    # #slider_range = st.slider("Seconds range", value=[000, end, 400])


    # st.info("Our slider range has type: %s" % type(slider_range))
    # st.write("Slider range:", slider_range, slider_range[0], slider_range[1])

    ### NEW DATA

    my_expander = st.expander(label='Filter Data')
    with my_expander:
        st.subheader("Select Layer Range")
        # COLUMNS LAYOUT
        startLay_col, endLay_col, layerSlider = st.columns(3)

        ## SLIDER WITH TEXT INPUT


        min_layer = int(conlog['  layer'].min())
        max_layer = int(conlog['  layer'].max())
        strtLayer = int(startLay_col.text_input('Start Layer', '1'))
        endLayer = int(endLay_col.text_input('End Layer', '5'))

        selected_layer_range = layerSlider.slider('Select the layer range', min_layer, max_layer, (strtLayer, endLayer),
                                                  1)
        st.write('Range Values', selected_layer_range)

        # Filtering data
        df_selected_layer = conlog[(conlog['  layer'].between(selected_layer_range[0], selected_layer_range[1]))]
        # st.header('Confocal Data')
        # st.dataframe(df_selected_model)
        #'Filtered Data'
        #clicked = st.button('Click me!')

        # adding a checkbox
        dfShow = st.checkbox('Show Filtered Data')

        # specifying what should be displayed if the check box is selected
        if dfShow:
            df_selected_layer





    # def my_widget(key):
    #     st.subheader('Hello there!')
    #     return st.button("Click me " + key)

    # This works in the main area

#
# clicked = my_widget("first")

with printNumbers:
    FileName, StatsTime, StatsLayer, = st.columns(3)
    ###NAME OF THE FILE

    # preparing data to display in a bar chart
    FileName.subheader('File name')
    #FileName.metric(".csv", value="Confocal")
    FileName.metric(".csv", (os.path.basename(file_path)))


    ###TIME OF PRINT
    ttime = conlog['  time(sec)'].value_counts()
    ttime2 = conlog['  time(sec)'].max()
    ttime2MinDec = ttime2 // 60
    ttime2Min = int(ttime2MinDec)
    ttime2Hr = ttime2Min//60
    # Title
    StatsTime.subheader('Total Print Time')
    mn, hrs, = st.columns(2)
    # printTime = st.container()
    #Time in Min
    StatsTime.metric("Minuets", value=ttime2Min)
    #hrs.metric("Hrs", value=ttime2Hr)

    ###TOTAL LAYERS
    tLayer = conlog['  layer'].max()
    # Title
    StatsLayer.subheader('Total Layers')
    StatsLayer.metric("Layers", value=tLayer)

with conf_reading:
    #COULUMNS LAYOUT
    Confoc1, Confoc2, = st.columns(2)


    Confoc1.header("CNF Reading 3")
    fig3 = px.scatter(data_frame=df_selected_layer, x='  layer', y=' reading 3', color=' type',
                     symbol=None, size=None, trendline=None, marginal_x='violin', marginal_y
                     ='violin', facet_row=None, facet_col=None, render_mode='auto', )
    fig3.update()
    Confoc1.write(fig3)

    ## CONFOCAL READING 2
    Confoc2.header("CNF Reading 2")
    fig = px.scatter(data_frame=df_selected_layer, x='  time(sec)', y=' reading 2', color=
    ' type', symbol=None, size=None, trendline=None, marginal_x='histogram',
                     marginal_y='histogram', facet_row=None, facet_col=None, render_mode=
                     'auto', )
    fig.update()
    Confoc2.write(fig)

with column:

    # 7 --- creating columns inside a container
    #		(you can create more than 2)
    bar_col, pie_col = st.columns(2)


    #pie_col.print ttime
    st.header("Time Ratios")

   # PLOT TITLE
    pie_col.subheader('Type Breakdown')

    # pie chart
    fig2 = px.pie(data_frame=conlog, names=' type', values='  time(sec)', color=None,)
    #fig2
    pie_col.write(fig2)



    # Layout Params
    # fig2.update_layout(showlegend=True,
    #                   width=400,
    #                   height=400,
    #                   margin=dict(l=20, r=10, b=1, t=1),
    #                   font=dict(color='#383635', size=20))

    # this function adds labels to the pie chart
    # for more information on this chart, visit: https://plotly.com/python/pie-charts/
    #fig2.update_traces(textposition='inside', textinfo='percent+label')

    # after creating the chart, we display it on the app's screen using this command
