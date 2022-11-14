# To use the requests library:
import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
from st_aggrid import GridOptionsBuilder, AgGrid
pd.options.mode.chained_assignment = None
import matplotlib.pyplot as plt
import rfpimp

#page layout and header
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: white;'>Ion Etching Machine Dashboard</h1>", unsafe_allow_html=True)

#sidebar
side = st.sidebar.radio("View", ["Live", "Historical", "Data Exploration"])

if side == "Live":
    #upload the CSV
    uploaded_file = st.file_uploader("Choose a CSV")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        df_stream_test_list = uploaded_file.getvalue().decode('utf-8').splitlines()         
    
        df_stream_test = []
        #remove header, will manually make header names
        df_stream_test_list.remove(df_stream_test_list[0])
        for i in range(len(df_stream_test_list)):
            df_stream_test.append(df_stream_test_list[i].split(","))
        
        #make dataframe with header names hard coded
        df_stream_test = pd.DataFrame(df_stream_test, columns =['TIME','IONGAUGEPRESSURE','ETCHBEAMVOLTAGE','FLOWCOOLFLOWRATE','FLOWCOOLPRESSURE','ETCHGASCHANNEL1READBACK','ETCHPBNGASREADBACK','FIXTURETILTANGLE','ACTUALROTATIONANGLE','ETCHSOURCEUSAGE','ACTUALSTEPDURATION','TTF_FlowCool Pressure Dropped Below Limit','IsFailure']) 
        
        #train test split
        df_stream_xTest = df_stream_test.drop(['TIME', 'TTF_FlowCool Pressure Dropped Below Limit', 'IsFailure'], axis=1)
        df_stream_yTest = df_stream_test['IsFailure']
        df_stream_yTest = list(map(float, df_stream_yTest))
        
        #loaded classifier from pickle
        import pickle
        filename = 'Streamlit/RFC_10.sav'
        RFC = pickle.load(open(filename, 'rb'))
        
        #loaded Regressor from pickle        
        import pickle
        filename = 'Streamlit/RFR_Overfit.sav'
        RFR_Overfit = pickle.load(open(filename, 'rb'))
        
        #left and right columns to see live dashboard with machine status
        left, right = st.columns([3, 1])
        #session state for machine state
        if 'rfc_pred' not in st.session_state:
            st.session_state['rfc_pred'] = 'Machine running steady'
            
        #add data inserted to session state
        if 'data' not in st.session_state:
            st.session_state['data'] = df_stream_test
        
        with left:
        #line graphs
            tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10= st.tabs(['IONGAUGEPRESSURE','ETCHBEAMVOLTAGE','FLOWCOOLFLOWRATE','FLOWCOOLPRESSURE','ETCHGASCHANNEL1READBACK','ETCHPBNGASREADBACK','FIXTURETILTANGLE','ACTUALROTATIONANGLE','ETCHSOURCEUSAGE','ACTUALSTEPDURATION'])
        
        #start right section
        with right:
            t = st.empty()
            t.markdown("<p style='font-size: 20px;color: Green'>" + st.session_state.rfc_pred + "</p>", unsafe_allow_html=True)
        
        #feature importance
        imp = rfpimp.importances(RFR_Overfit, df_stream_xTest, df_stream_yTest)
        x = 0
        
        #create titles, line graphs, and print feature importance (1-10 with 1 being the highest)
        with tab1:
            df_plot_1 = df_stream_test[['TIME','IONGAUGEPRESSURE']]
            df_plot_1 = pd.DataFrame(df_plot_1)
            df_plot_1 = df_plot_1.set_index('TIME')
            st.write("IONGAUGEPRESSURE LINE GRAPH")
            for i in range(len(imp['Importance'])):
                if imp['Importance'].index[i] == 'IONGAUGEPRESSURE':
                    x = i
            st.write('Feature is of importance: ' + str(x + 1))
            line_chart_1 = st.line_chart(width = 500, height = 300)
        with tab2:
            df_plot_2 = df_stream_test[['TIME','ETCHBEAMVOLTAGE']]
            df_plot_2 = pd.DataFrame(df_plot_2)
            df_plot_2 = df_plot_2.set_index('TIME')
            st.write("ETCHBEAMVOLTAGE LINE GRAPH")
            for i in range(len(imp['Importance'])):
                if imp['Importance'].index[i] == 'ETCHBEAMVOLTAGE':
                    x = i
            st.write('Feature is of importance: ' + str(x + 1))
            line_chart_2 = st.line_chart(width = 500, height = 300)
        with tab3:
            df_plot_3 = df_stream_test[['TIME','FLOWCOOLFLOWRATE']]
            df_plot_3 = pd.DataFrame(df_plot_3)
            df_plot_3 = df_plot_3.set_index('TIME')
            st.write("FLOWCOOLFLOWRATE LINE GRAPH")
            for i in range(len(imp['Importance'])):
                if imp['Importance'].index[i] == 'FLOWCOOLFLOWRATE':
                    x = i
            st.write('Feature is of importance: ' + str(x + 1))
            line_chart_3 = st.line_chart(width = 500, height = 300)
        with tab4:
            df_plot_4 = df_stream_test[['TIME','FLOWCOOLPRESSURE']]
            df_plot_4 = pd.DataFrame(df_plot_4)
            df_plot_4 = df_plot_4.set_index('TIME')
            st.write("FLOWCOOLPRESSURE LINE GRAPH")
            for i in range(len(imp['Importance'])):
                if imp['Importance'].index[i] == 'FLOWCOOLPRESSURE':
                    x = i
            st.write('Feature is of importance: ' + str(x + 1))
            line_chart_4 = st.line_chart(width = 500, height = 300)
        with tab5:
            df_plot_5 = df_stream_test[['TIME','ETCHGASCHANNEL1READBACK']]
            df_plot_5 = pd.DataFrame(df_plot_5)
            df_plot_5 = df_plot_5.set_index('TIME')
            st.write("ETCHGASCHANNEL1READBACK LINE GRAPH")
            for i in range(len(imp['Importance'])):
                if imp['Importance'].index[i] == 'ETCHGASCHANNEL1READBACK':
                    x = i
            st.write('Feature is of importance: ' + str(x + 1))
            line_chart_5 = st.line_chart(width = 500, height = 300)
        with tab6:
            df_plot_6 = df_stream_test[['TIME','ETCHPBNGASREADBACK']]
            df_plot_6 = pd.DataFrame(df_plot_6)
            df_plot_6 = df_plot_6.set_index('TIME')
            st.write("ETCHPBNGASREADBACK LINE GRAPH")
            for i in range(len(imp['Importance'])):
                if imp['Importance'].index[i] == 'ETCHPBNGASREADBACK':
                    x = i
            st.write('Feature is of importance: ' + str(x + 1))
            line_chart_6 = st.line_chart(width = 500, height = 300)
        with tab7:
            df_plot_7 = df_stream_test[['TIME','FIXTURETILTANGLE']]
            df_plot_7 = pd.DataFrame(df_plot_7)
            df_plot_7 = df_plot_7.set_index('TIME')
            st.write("FIXTURETILTANGLE LINE GRAPH")
            for i in range(len(imp['Importance'])):
                if imp['Importance'].index[i] == 'FIXTURETILTANGLE':
                    x = i
            st.write('Feature is of importance: ' + str(x + 1))
            line_chart_7 = st.line_chart(width = 500, height = 300)
        with tab8:
            df_plot_8 = df_stream_test[['TIME','ACTUALROTATIONANGLE']]
            df_plot_8 = pd.DataFrame(df_plot_8)
            df_plot_8 = df_plot_8.set_index('TIME')
            st.write("ACTUALROTATIONANGLE LINE GRAPH")
            for i in range(len(imp['Importance'])):
                if imp['Importance'].index[i] == 'ACTUALROTATIONANGLE':
                    x = i
            st.write('Feature is of importance: ' + str(x + 1))
            line_chart_8 = st.line_chart(width = 500, height = 300)
        with tab9:
            df_plot_9 = df_stream_test[['TIME','ETCHSOURCEUSAGE']]
            df_plot_9 = pd.DataFrame(df_plot_9)
            df_plot_9 = df_plot_9.set_index('TIME')
            st.write("ETCHSOURCEUSAGE LINE GRAPH")
            for i in range(len(imp['Importance'])):
                if imp['Importance'].index[i] == 'ETCHSOURCEUSAGE':
                    x = i
            st.write('Feature is of importance: ' + str(x + 1))
            line_chart_9 = st.line_chart(width = 500, height = 300)
        with tab10:
            df_plot_10 = df_stream_test[['TIME','ACTUALSTEPDURATION']]
            df_plot_10 = pd.DataFrame(df_plot_10)
            df_plot_10 = df_plot_10.set_index('TIME')
            st.write("ACTUALSTEPDURATION LINE GRAPH")
            for i in range(len(imp['Importance'])):
                if imp['Importance'].index[i] == 'ACTUALSTEPDURATION':
                    x = i
            st.write('Feature is of importance: ' + str(x + 1))
            line_chart_10 = st.line_chart(width = 500, height = 300)
        
        #loop through the CSV 1 row at a time, and populate line graph with that data
        for i in range(len(df_plot_1)):
            time.sleep(0.5)
            plot_1 = pd.DataFrame(df_plot_1.iloc[i]).T
            line_chart_1.add_rows(plot_1)
            plot_2 = pd.DataFrame(df_plot_2.iloc[i]).T
            line_chart_2.add_rows(plot_2)
            plot_3 = pd.DataFrame(df_plot_3.iloc[i]).T
            line_chart_3.add_rows(plot_3)
            plot_4 = pd.DataFrame(df_plot_4.iloc[i]).T
            line_chart_4.add_rows(plot_4)
            plot_5 = pd.DataFrame(df_plot_5.iloc[i]).T
            line_chart_5.add_rows(plot_5)
            plot_6 = pd.DataFrame(df_plot_6.iloc[i]).T
            line_chart_6.add_rows(plot_6)
            plot_7 = pd.DataFrame(df_plot_7.iloc[i]).T
            line_chart_7.add_rows(plot_7)
            plot_8 = pd.DataFrame(df_plot_8.iloc[i]).T
            line_chart_8.add_rows(plot_8)
            plot_9 = pd.DataFrame(df_plot_9.iloc[i]).T
            line_chart_9.add_rows(plot_9)
            plot_10 = pd.DataFrame(df_plot_10.iloc[i]).T
            line_chart_10.add_rows(plot_10)
            predictions = RFC.predict_proba(df_stream_xTest.iloc[[i]])
            if predictions[0][1] > 0.55:
                RUL_pred = int(RFR_Overfit.predict(df_stream_xTest.iloc[[i]])[0])
                #update session state with the predicted RUL
                if RUL_pred > 250:
                    st.session_state.rfc_pred = "Warning, RUL : " + str(RUL_pred - 250) + " seconds"
                    t.markdown("<p style='font-size: 20px;color: Yellow'>" + st.session_state.rfc_pred + "</p>", unsafe_allow_html=True)
                elif RUL_pred <= 250:
                    st.session_state.rfc_pred = "Warning, RUL : 0 seconds. \n MACHINE HAS FAILED"
                    t.markdown("<p style='font-size: 20px;color: Red'>" + st.session_state.rfc_pred + "</p>", unsafe_allow_html=True)
        #print all the data that was just inserted
        del st.session_state['rfc_pred']

#historical view. Using CSV train
if side == "Historical":
    #load training data
    df_stream_train_raw = pd.read_csv(r'https://raw.githubusercontent.com/JacobShaw98/PHM_RUL/main/Streamlit/690_fault_1_df_train.csv', delimiter=',', engine = 'python', encoding = 'utf8')
    df_stream_train_raw.columns = ['TIME','IONGAUGEPRESSURE','ETCHBEAMVOLTAGE','FLOWCOOLFLOWRATE','FLOWCOOLPRESSURE','ETCHGASCHANNEL1READBACK','ETCHPBNGASREADBACK','FIXTURETILTANGLE','ACTUALROTATIONANGLE','ETCHSOURCEUSAGE','ACTUALSTEPDURATION','TTF_FlowCool Pressure Dropped Below Limit','IsFailure']
    
    if 'data' in st.session_state:
        test = st.session_state.data
        test = test.astype(np.float64)
        test = test.astype({"TIME": np.int64})
        df_stream_train_raw = pd.concat([df_stream_train_raw, test])
    
    #get bounds for slider
    lower = df_stream_train_raw.iloc[0,0].item()
    upper = df_stream_train_raw.iloc[-1,0].item()
    #create slider
    slider = st.slider("Select Time Range", value = [lower, upper])
    
    #make data fit the slider values
    df_stream_train = df_stream_train_raw[df_stream_train_raw.TIME > slider[0]]
    df_stream_train = df_stream_train[df_stream_train.TIME < slider[1]]
    df_stream_train_prePF = df_stream_train[df_stream_train.IONGAUGEPRESSURE != 75.79964582251432] #drop annoying row

    #let user select what data they want to see for Pass Fail
    pf = st.radio(
        "What data would you like to see?",
        ('All', 'Pass', 'Fail'),
        horizontal = True)
    
    if pf =='All':
        df_stream_train = df_stream_train_prePF
    elif pf =='Pass':
        df_stream_train = df_stream_train_prePF[df_stream_train_prePF.IsFailure == 0]
    elif pf =='Fail':
        df_stream_train = df_stream_train_prePF[df_stream_train_prePF.IsFailure == 1]

    #create pie chart using prePF since pie chart needs class variation
    sizes = df_stream_train_prePF['IsFailure'].value_counts()
    labels = 'Passes', 'Fails'
    explode = (0, 0.1)
    
    #plot pie chart
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90, textprops={'fontsize': 32})
    ax1.axis('equal')
    
    #drop TTF since we don't need it for Vis
    df_stream_train = df_stream_train.drop('TTF_FlowCool Pressure Dropped Below Limit', axis = 1)

    #tab per important column
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10= st.tabs(['IONGAUGEPRESSURE','ETCHBEAMVOLTAGE','FLOWCOOLFLOWRATE','FLOWCOOLPRESSURE','ETCHGASCHANNEL1READBACK','ETCHPBNGASREADBACK','FIXTURETILTANGLE','ACTUALROTATIONANGLE','ETCHSOURCEUSAGE','ACTUALSTEPDURATION'])
        
    #Make line graphs and plot pie charts and histograms per tab
    with tab1: #IONGAUGEPRESSURE
        left2, right2 = st.columns([3, 1])
        df_plot_1 = df_stream_train[['IONGAUGEPRESSURE', 'IsFailure']]
        df_plot_1 = pd.DataFrame(df_plot_1)
        with left2:
            st.line_chart(data = df_plot_1, width = 500, height = 400)
        fig, ax = plt.subplots()
        ax.hist(df_stream_train['IONGAUGEPRESSURE'], bins=20)
        with right2:
            st.pyplot(fig)
            st.pyplot(fig1)
    with tab2: #ETCHBEAMVOLTAGE
        left2, right2 = st.columns([3, 1])
        df_plot_2 = df_stream_train[['ETCHBEAMVOLTAGE', 'IsFailure']]
        df_plot_2 = pd.DataFrame(df_plot_2)
        with left2:
            st.line_chart(data = df_plot_2, width = 500, height = 400)
        fig, ax = plt.subplots()
        ax.hist(df_stream_train['ETCHBEAMVOLTAGE'], bins=20)
        with right2:
            st.pyplot(fig)
            st.pyplot(fig1)
    with tab3: #FLOWCOOLFLOWRATE
        left2, right2 = st.columns([3, 1])
        df_plot_3 = df_stream_train[['FLOWCOOLFLOWRATE', 'IsFailure']]
        df_plot_3 = pd.DataFrame(df_plot_3)
        with left2:
            st.line_chart(data = df_plot_3, width = 500, height = 400)
        fig, ax = plt.subplots()
        ax.hist(df_stream_train['FLOWCOOLFLOWRATE'], bins=20)
        with right2:
            st.pyplot(fig)
            st.pyplot(fig1)
    with tab4: #FLOWCOOLPRESSURE
        left2, right2 = st.columns([3, 1])
        df_plot_4 = df_stream_train[['FLOWCOOLPRESSURE', 'IsFailure']]
        df_plot_4 = pd.DataFrame(df_plot_4)
        with left2:
            st.line_chart(data = df_plot_4, width = 500, height = 400)
        fig, ax = plt.subplots()
        ax.hist(df_stream_train['FLOWCOOLPRESSURE'], bins=20)
        with right2:
            st.pyplot(fig)
            st.pyplot(fig1)
    with tab5: #ETCHGASCHANNEL1READBACK
        left2, right2 = st.columns([3, 1])
        df_plot_5 = df_stream_train[['ETCHGASCHANNEL1READBACK', 'IsFailure']]
        df_plot_5 = pd.DataFrame(df_plot_5)
        with left2:
            st.line_chart(data = df_plot_5, width = 500, height = 400)
        fig, ax = plt.subplots()
        ax.hist(df_stream_train['ETCHGASCHANNEL1READBACK'], bins=20)
        with right2:
            st.pyplot(fig)
            st.pyplot(fig1)
    with tab6: #ETCHPBNGASREADBACK
        left2, right2 = st.columns([3, 1])
        df_plot_6 = df_stream_train[['ETCHPBNGASREADBACK', 'IsFailure']]
        df_plot_6 = pd.DataFrame(df_plot_6)
        with left2:
            st.line_chart(data = df_plot_6, width = 500, height = 400)
        fig, ax = plt.subplots()
        ax.hist(df_stream_train['ETCHPBNGASREADBACK'], bins=20)
        with right2:
            st.pyplot(fig)
            st.pyplot(fig1)
    with tab7: #FIXTURETILTANGLE
        left2, right2 = st.columns([3, 1])
        df_plot_7 = df_stream_train[['FIXTURETILTANGLE', 'IsFailure']]
        df_plot_7 = pd.DataFrame(df_plot_7)
        with left2:
            st.line_chart(data = df_plot_7, width = 500, height = 400)
        fig, ax = plt.subplots()
        ax.hist(df_stream_train['FIXTURETILTANGLE'], bins=20)
        with right2:
            st.pyplot(fig)
            st.pyplot(fig1)
    with tab8: #ACTUALROTATIONANGLE
        left2, right2 = st.columns([3, 1])
        df_plot_8 = df_stream_train[['ACTUALROTATIONANGLE', 'IsFailure']]
        df_plot_8 = pd.DataFrame(df_plot_8)
        with left2:
            st.line_chart(data = df_plot_8, width = 500, height = 400)
        fig, ax = plt.subplots()
        ax.hist(df_stream_train['ACTUALROTATIONANGLE'], bins=20)
        with right2:
            st.pyplot(fig)
            st.pyplot(fig1)
    with tab9: #ETCHSOURCEUSAGE
        left2, right2 = st.columns([3, 1])
        df_plot_9 = df_stream_train[['ETCHSOURCEUSAGE', 'IsFailure']]
        df_plot_9 = pd.DataFrame(df_plot_9)
        with left2:
            st.line_chart(data = df_plot_9, width = 500, height = 400)
        fig, ax = plt.subplots()
        ax.hist(df_stream_train['ETCHSOURCEUSAGE'], bins=20)
        with right2:
            st.pyplot(fig)
            st.pyplot(fig1)
    with tab10: #ACTUALSTEPDURATION
        left2, right2 = st.columns([3, 1])
        df_plot_10 = df_stream_train[['ACTUALSTEPDURATION', 'IsFailure']]
        df_plot_10 = pd.DataFrame(df_plot_10)
        with left2:
            st.line_chart(data = df_plot_10, width = 500, height = 400)
        fig, ax = plt.subplots()
        ax.hist(df_stream_train['ACTUALSTEPDURATION'], bins=20)
        with right2:
            st.pyplot(fig)
            st.pyplot(fig1)

if side == "Data Exploration":
    tab1, tab2= st.tabs(['Live Data','Historical Data'])
    with tab1:
        if 'data' in st.session_state:
            st.subheader("Click Rows to Select Them!")
            data = st.session_state.data
            gb = GridOptionsBuilder.from_dataframe(data)
            gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
            gb.configure_side_bar() #Add a sidebar
            gb.configure_selection(selection_mode = 'multiple', use_checkbox=False) #Enable multi-row selection
            gridOptions = gb.build()
            
            grid_response = AgGrid(
                data,
                gridOptions=gridOptions,
                fit_columns_on_grid_load=False,
                height=550, 
                width='100%',
            )
            
            st.subheader("Selected Rows")
            selected = grid_response['selected_rows'] 
            df = pd.DataFrame(selected)
            df = df.iloc[: , 1:]
            st.dataframe(df)
            
            now = datetime.now()
            current_time = now.strftime("%Y_%m_%d__%H_%M_%S")
            
            st.download_button(
               "Save Selected Data",
               df.to_csv(),
               'live_' + current_time + '.csv',
               "text/csv",
               key='download-csv-live'
            )
        else:
            st.write("Insert data using the Live Section")
    with tab2:
        df_stream_train_raw = pd.read_csv(r'https://raw.githubusercontent.com/JacobShaw98/PHM_RUL/main/Streamlit/690_fault_1_df_train.csv', delimiter=',', engine = 'python', encoding = 'utf8')
        df_stream_train_raw.columns = ['TIME','IONGAUGEPRESSURE','ETCHBEAMVOLTAGE','FLOWCOOLFLOWRATE','FLOWCOOLPRESSURE','ETCHGASCHANNEL1READBACK','ETCHPBNGASREADBACK','FIXTURETILTANGLE','ACTUALROTATIONANGLE','ETCHSOURCEUSAGE','ACTUALSTEPDURATION','TTF_FlowCool Pressure Dropped Below Limit','IsFailure']
        
        if 'data' in st.session_state:
            test = st.session_state.data
            test = test.astype(np.float64)
            test = test.astype({"TIME": np.int64})
            df_stream_train_raw = pd.concat([df_stream_train_raw, test])
            
        st.subheader("Click Rows to Select Them!")
        data = df_stream_train_raw
        gb = GridOptionsBuilder.from_dataframe(data)
        gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
        gb.configure_side_bar() #Add a sidebar
        gb.configure_selection(selection_mode = 'multiple', use_checkbox=False) #Enable multi-row selection
        gridOptions = gb.build()
        
        grid_response = AgGrid(
            data,
            gridOptions=gridOptions,
            fit_columns_on_grid_load=False,
            height=550, 
            width='100%',
        )
        
        st.subheader("Selected Rows")
        selected = grid_response['selected_rows'] 
        df = pd.DataFrame(selected)
        df = df.iloc[: , 1:]
        st.dataframe(df)
        
        now = datetime.now()
        current_time = now.strftime("%Y_%m_%d__%H_%M_%S")
        
        st.download_button(
           "Save Selected Data",
           df.to_csv(),
           'historical_' + current_time + '.csv',
           "text/csv",
           key='download-csv-hist'
        )