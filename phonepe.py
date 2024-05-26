import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import psycopg2
import plotly.express as px
import requests
import json
from PIL import Image


#Dataframe creation

#sql connection
mydb = psycopg2.connect(
                        host="localhost",
                        user="postgres",
                        password="Kiprthmass2170.",
                        port="5432",
                        database="phonepe_data"
                    )

cursor=mydb.cursor()

#aggre_transaction_df
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2= cursor.fetchall()

Aggre_transaction= pd.DataFrame(table2, columns=("States", "Years", "Quater", "Transaction_type",
                                               "Transaction_count", "Transaction_amount"))

#aggre_user_df
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3= cursor.fetchall()

Aggre_user= pd.DataFrame(table3, columns=("States", "Years", "Quater", "Brands",
                                               "Transaction_count", "Percentage"))

#map_transaction
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5= cursor.fetchall()

map_transaction= pd.DataFrame(table5, columns=("States", "Years", "Quater", "Districts",
                                                    "Transaction_count", "Transaction_amount"))

#map_user
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6= cursor.fetchall()

map_user= pd.DataFrame(table6, columns=("States", "Years", "Quater", "Districts",
                                               "RegisteredUser", "AppOpens"))

#top_transaction
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8= cursor.fetchall()

top_transaction= pd.DataFrame(table8, columns=("States", "Years", "Quater", "Pincodes",
                                               "Transaction_count", "Transaction_amount"))

#top_user
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9= cursor.fetchall()

top_user= pd.DataFrame(table9, columns=("States", "Years", "Quater", "Pincodes",
                                               "RegisteredUsers"))

# function to get Transaction_amount_count_Y

def Transaction_amount_count_Year(df,year):

    tacy=df[df["Years"] == year]
    tacy.reset_index(drop=True, inplace=True)

    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(tacyg, x= "States" , y="Transaction_amount",title=f"{year}'S   TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=550, width=550)
        st.plotly_chart(fig_amount)

    with col2:

        fig_count= px.bar(tacyg, x= "States" , y="Transaction_count",title=f"{year}'S  TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=550, width=550)
        
        st.plotly_chart(fig_count)
    
    col1,col2= st.columns(2)
    with col1:
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_amount", color_continuous_scale= "turbo",
                                    range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                    hover_name= "States", title= f"{year}'S   TRANSACTION AMOUNT", fitbounds= "locations",
                                    height= 600,width= 600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)  

    with col2:   
        fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale= "turbo",
                                range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "States", title= f"{year}'S   TRANSACTION COUNT", fitbounds= "locations",
                                height= 600,width= 600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tacy


def Transaction_amount_count_Year_Quater(df,quater):

    tacy=df[df["Quater"] == quater]
    tacy.reset_index(drop=True, inplace=True)

    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(tacyg, x= "States" , y="Transaction_amount",title=f"{tacy['Years'].min()} YEAR {quater}  QUATER'S   TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_amount)

    
    with col2:

        fig_count= px.bar(tacyg, x= "States" , y="Transaction_count",title=f"{tacy['Years'].min()} YEAR {quater} QUATER'S   TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale= "turbo",
                                range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name= "States", title= f"{tacy['Years'].min()} YEAR {quater} QUATER'S   TRANSACTION AMOUNT", fitbounds= "locations",
                                height= 600,width= 600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1) 

    
    with col2:
        fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale= "turbo",
                                range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "States", title= f"{tacy['Years'].min()} YEAR {quater} QUATER'S   TRANSACTION COUNT", fitbounds= "locations",
                                height= 600,width= 600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)       

        return tacy        

def Aggre_Trans_type(df,state):

    tacy= df[df["States"] == state]
    tacy.reset_index(drop=True, inplace=True)

    tacyg= tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_pie_chart1= px.pie(data_frame= tacyg, names="Transaction_type", values="Transaction_amount", width=600, title=f"{state.upper()}'S   TRANSACTION AMOUNT")
        st.plotly_chart(fig_pie_chart1)
        
    with col2:
        fig_pie_chart2= px.pie(data_frame= tacyg, names="Transaction_type", values="Transaction_count", width=600, title=f"{state.upper()}'S   TRANSACTION COUNT")
        st.plotly_chart(fig_pie_chart2)

#Aggre_user_analysis1
def Aggre_user_plot1(df,year):
    auy =df[df["Years"] ==year]
    auy.reset_index(drop=True, inplace=True)

    auyg= pd.DataFrame(auy.groupby("Brands")["Transaction_count"].sum())
    auyg.reset_index(inplace=True)

    fig_bar_1=px.bar(auyg, x= "Brands" , y= "Transaction_count", title=f"{year}'S    BRANDS AND TRANSACTION COUNT",
                        width=1000, color_discrete_sequence= px.colors.sequential.haline, hover_name="Brands")

    st.plotly_chart(fig_bar_1)

    return auy

#Aggre_user_analysis2
def Aggre_user_plot2(df,quater):
    auy_quater =df[df["Quater"] ==quater]
    auy_quater.reset_index(drop=True, inplace=True)

    auy_quater_g= pd.DataFrame(auy_quater.groupby("Brands")["Transaction_count"].sum())
    auy_quater_g.reset_index(inplace=True)

    fig_bar_2=px.bar(auy_quater_g, x= "Brands" , y= "Transaction_count", title=f"{quater}'S   BRANDS AND TRANSACTION COUNT",
                        width=1000, color_discrete_sequence= px.colors.sequential.Plasma_r)

    st.plotly_chart(fig_bar_2)

    return auy_quater

#Aggre_user_analysis3
def Aggre_user_plot3(df, state):
    aupqs = df[df["States"] == state]
    aupqs.reset_index(drop=True, inplace=True)

    aupqsg= pd.DataFrame(aupqs.groupby("Brands")["Transaction_count"].sum())
    aupqsg.reset_index(inplace=True)

    fig_pie_3=px.pie(data_frame= aupqs ,names= "Brands", values= "Transaction_count", hover_data = "Percentage",
                        title= f"{state.upper()}'S   BRANDS BY TRANSACTION COUNT AND PERCENTAGE", height=600, width=850,
                        color_discrete_sequence= px.colors.sequential.Plasma_r)

    st.plotly_chart(fig_pie_3)

    return aupqs

#Map Transaction Type
def Map_Tran_state(df,state):

    tacy= df[df["States"] == state]
    tacy.reset_index(drop=True, inplace=True)
    
    tacyg= tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_bar_chart1= px.bar(tacyg, x="Transaction_amount", y="Districts",orientation="h",height=400, width=500, title="DISTRICT AND TRANSACTION AMOUNT",color_discrete_sequence= px.colors.sequential.Mint_r )
        st.plotly_chart(fig_bar_chart1)

    with col2:

        fig_bar_chart2= px.bar(tacyg, x="Transaction_count", y="Districts",orientation="h",height=400, width=500, title="DISTRICT AND TRANSACTION COUNT",color_discrete_sequence= px.colors.sequential.Bluered )
        st.plotly_chart(fig_bar_chart2)

    return tacy

# Map User Plot 1
def Map_user_plot1(df,year):
    muy =df[df["Years"] ==year]
    muy.reset_index(drop=True, inplace=True)

    muyg= pd.DataFrame(muy.groupby("States")[["RegisteredUser","AppOpens"]].sum())
    muyg.reset_index(inplace=True)

    fig_line_1=px.line(data_frame= muyg ,x= "States", y= ["RegisteredUser","AppOpens"],
                        title= f"{year}'S    REGISTERED USER AND APPOPENS", height=600, width=850, markers= True)
                        

    st.plotly_chart(fig_line_1)
    return muy


# Map User Plot 2
def Map_user_plot2(df,quater):
    muyq =df[df["Quater"] == quater]
    muyq.reset_index(drop=True, inplace=True)

    muyqg= pd.DataFrame(muyq.groupby("States")[["RegisteredUser","AppOpens"]].sum())
    muyqg.reset_index(inplace=True)

    fig_line_1=px.line(data_frame= muyqg ,x= "States", y= ["RegisteredUser","AppOpens"],
                        title= f"{df['Years'].min()}'S  {quater}  QUATER'S  REGISTERED USER AND APPOPENS", height=600, width=850, markers= True,
                        color_discrete_sequence=px.colors.sequential.Rainbow_r)
                        

    st.plotly_chart(fig_line_1)
    return muyq

# Map User Plot 3
def Map_user_plot3(df,state):

    muyqs =df[df["States"] == state]
    muyqs.reset_index(drop=True, inplace=True)

    fig_map_bar_1 = px.bar(muyqs , x= "RegisteredUser", y= "Districts" , orientation="h",
                            title=f"{state.upper()}'S  REGISTERED USER", height=800, color_discrete_sequence=px.colors.sequential.Rainbow_r)

    st.plotly_chart(fig_map_bar_1)

    fig_map_bar_2 = px.bar(muyqs , x= "AppOpens", y= "Districts" , orientation="h",
                            title=f"{state.upper()}'S  APPOPENS", height=800, color_discrete_sequence=px.colors.sequential.Rainbow)

    st.plotly_chart(fig_map_bar_2)


# top_trans_plot_1

def Top_trans_plot_1(df, state):
    
    tiy= df[df["States"]== state]
    tiy.reset_index(drop= True, inplace= True)


    fig_top_insur_bar_1= px.bar(tiy, x= "Quater", y= "Transaction_amount", hover_data= "Pincodes",
                            title= "TRANSACTION AMOUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.GnBu_r)

    st.plotly_chart(fig_top_insur_bar_1)


    fig_top_insur_bar_2= px.bar(tiy, x= "Quater", y= "Transaction_count", hover_data= "Pincodes",
                            title= "TRANSACTION COUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.Rainbow)

    st.plotly_chart(fig_top_insur_bar_2)

# top user plot 1

def Top_user_plot_1(df, year):
    Tuy= df[df["Years"]== year]
    Tuy.reset_index(drop= True, inplace= True)

    Tuyg= pd.DataFrame(Tuy.groupby(["States", "Quater"])["RegisteredUsers"].sum())
    Tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(Tuyg, x= "States", y= "RegisteredUsers", color= "Quater", width= 1000, height= 800,
                        color_discrete_sequence= px.colors.sequential.Burgyl_r, hover_name= "States",
                        title= f"{year}'S   REGISTERED USERS")

    st.plotly_chart(fig_top_plot_1)

    return Tuy

# top user plot 2
def top_user_plot_2(df, state):

    tuys =df[df["States"] == state]
    tuys.reset_index(drop=True, inplace=True)

    fig_top_plot_2= px.bar(tuys, x= "Quater", y= "RegisteredUsers", title= "REGISTERED USERS, PINCODES, QUATER",
                        width= 1000, height= 800, color= "RegisteredUsers", hover_data= "Pincodes",
                        color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)


# top trans count 
def top_chart_tttc(table_name):

    #sql connection
    mydb = psycopg2.connect(
                            host="localhost",
                            user="postgres",
                            password="Kiprthmass2170.",
                            port="5432",
                            database="phonepe_data"
                        )

    cursor=mydb.cursor()

    #plot_1
    query1= f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "transaction_count"))

    fig_amount= px.bar(df_1, x="states", y="transaction_count", title="TOP 10 OF TRANSACTION COUNT", hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
    st.plotly_chart(fig_amount)

# lowest trans count 
def top_chart_lttc(table_name):

    #sql connection
    mydb = psycopg2.connect(
                            host="localhost",
                            user="postgres",
                            password="Kiprthmass2170.",
                            port="5432",
                            database="phonepe_data"
                        )

    cursor=mydb.cursor()

    query2= f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "transaction_count"))

    fig_amount_2= px.bar(df_2, x="states", y="transaction_count", title="LAST 10 OF TRANSACTION COUNT", hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.algae_r, height= 650,width= 600)
    st.plotly_chart(fig_amount_2)

#avg transaction count   

def top_chart_avgtc(table_name):

    #sql connection
    mydb = psycopg2.connect(
                            host="localhost",
                            user="postgres",
                            password="Kiprthmass2170.",
                            port="5432",
                            database="phonepe_data"
                        )

    cursor=mydb.cursor()
    #avg transaction count
    query3= f'''SELECT states, AVG(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "transaction_count"))

    fig_amount_3= px.bar(df_3, y="states", x="transaction_count", title="AVERAGE OF TRANSACTION COUNT", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

# top trans amt

def top_chart_ttta(table_name):

    #sql connection
    mydb = psycopg2.connect(
                            host="localhost",
                            user="postgres",
                            password="Kiprthmass2170.",
                            port="5432",
                            database="phonepe_data"
                        )

    cursor=mydb.cursor()

    
    query1= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "transaction_amount"))

    fig_amount= px.bar(df_1, x="states", y="transaction_amount", title="TOP 10 OF TRANSACTION AMOUNT", hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
    st.plotly_chart(fig_amount)

#low trans amt

def top_chart_ltta(table_name):

    #sql connection
    mydb = psycopg2.connect(
                            host="localhost",
                            user="postgres",
                            password="Kiprthmass2170.",
                            port="5432",
                            database="phonepe_data"
                        )

    cursor=mydb.cursor()

    #plot_2
    query2= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "transaction_amount"))

    fig_amount_2= px.bar(df_2, x="states", y="transaction_amount", title="LAST 10 OF TRANSACTION AMOUNT", hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.amp_r, height= 650,width= 600)
    st.plotly_chart(fig_amount_2)

#avg trans amt
def top_chart_avgta(table_name):

    #sql connection
    mydb = psycopg2.connect(
                            host="localhost",
                            user="postgres",
                            password="Kiprthmass2170.",
                            port="5432",
                            database="phonepe_data"
                        )

    cursor=mydb.cursor()
    
    #plot_3
    query3= f'''SELECT states, AVG(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "transaction_amount"))

    fig_amount_3= px.bar(df_3, y="states", x="transaction_amount", title="AVERAGE OF TRANSACTION AMOUNT", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

#function for top RU 

def top_chart_ru(table_name,state):

    #sql connection
    mydb = psycopg2.connect(
                            host="localhost",
                            user="postgres",
                            password="Kiprthmass2170.",
                            port="5432",
                            database="phonepe_data"
                        )

    cursor=mydb.cursor()

    #plot_1
    query1= f'''SELECT districts ,SUM(registeredusers) AS registeredusers
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY districts
                ORDER BY registeredusers DESC
                LIMIT 10 ;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("districts", "registeredusers"))

  
    fig_amount= px.bar(df_1, x="districts", y="registeredusers", title="FIRST 10 TOTAL REGISTERED USERS", hover_name= "districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
    st.plotly_chart(fig_amount)

#low RU 

    query2= f'''SELECT districts ,SUM(registeredusers) AS registeredusers
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY districts
                ORDER BY registeredusers 
                LIMIT 10 ;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("districts", "registeredusers"))


    fig_amount_2= px.bar(df_2, x="districts", y="registeredusers", title="LAST 10 TOTAL REGISTERED USERS", hover_name= "districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
    st.plotly_chart(fig_amount_2)
    
    
    #plot_3
    query3= f'''SELECT districts ,AVG(registeredusers) AS registeredusers
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY districts
                ORDER BY registeredusers 
                LIMIT 10 ;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("districts", "registeredusers"))

    fig_amount_3= px.bar(df_3, y="districts", x="registeredusers", title="AVERAGE OF REGISTERED USERS", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)


def top_chart_RU(table_name):
    #sql connection
    mydb = psycopg2.connect(
                            host="localhost",
                            user="postgres",
                            password="Kiprthmass2170.",
                            port="5432",
                            database="phonepe_data"
                        )

    cursor=mydb.cursor()

    #plot_1
    query1= f'''SELECT states, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "registeredusers"))

    fig_amount= px.bar(df_1, x="states", y="registeredusers", title="TOP 10 OF REGISTERED USERS", hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
    st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT states, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "registeredusers"))

    

    fig_amount_2= px.bar(df_2, x="states", y="registeredusers", title="LAST 10 REGISTERED USERS", hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
    st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT states, AVG(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "registeredusers"))

    fig_amount_3= px.bar(df_3, y="states", x="registeredusers", title="AVERAGE OF REGISTERED USERS", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

def top_chart_appopens(table_name, state):
    #sql connection
    mydb = psycopg2.connect(
                            host="localhost",
                            user="postgres",
                            password="Kiprthmass2170.",
                            port="5432",
                            database="phonepe_data"
                        )

    cursor=mydb.cursor()

    #plot_1
    query1= f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("districts", "appopens"))

    fig_amount= px.bar(df_1, x="districts", y="appopens", title="TOP 10 OF APPOPENS", hover_name= "districts",
                        color_discrete_sequence=px.colors.sequential.Agsunset, height= 650,width= 600)
    st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("districts", "appopens"))

    fig_amount_2= px.bar(df_2, x="districts", y="appopens", title="LAST 10 APPOPENS", hover_name= "districts",
                        color_discrete_sequence=px.colors.sequential.Agsunset_r, height= 650,width= 600)
    st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT districts, AVG(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("districts", "appopens"))

    fig_amount_3= px.bar(df_3, y="districts", x="appopens", title="AVERAGE OF APPOPENS", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

#streamlit part

st.set_page_config(layout= "wide")
st.markdown("# *PHONEPE DATA VISUALIZATION AND EXPLORATION*")

with st.sidebar:
    
    select= option_menu("Main Menu",["HOME", "DATA EXPLORATION", "TOP CHARTS"])

if select == "HOME":
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        video_file = open("C:\\Users\\manoj\\OneDrive\\Desktop\\Phonepe\\WhatsApp Video 2024-05-25 at 14.55.13.mp4", "rb")
        video_bytes = video_file.read()
        st.video(video_bytes)



    col3,col4= st.columns(2)
    
    with col3:
        st.image(Image.open(r"C:\Users\manoj\OneDrive\Desktop\Phonepe\download-phonepe-app-for-pc-mac.jpg"),width=450)

    with col4:
        st.write("********Easy Transactions********")
        st.write("********One App For All Your Payments********")
        st.write("********Your Bank Account Is All You Need********")
        st.write("********Multiple Payment Modes********")
        st.write("********PhonePe Merchants********")
        st.write("********Multiple Ways To Pay********")
        st.write("********1.Direct Transfer & More********")
        st.write("********2.QR Code********")
        st.write("********Earn Great Rewards********")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(Image.open(r"C:\Users\manoj\OneDrive\Desktop\Phonepe\Phonepe neew.webp"),width= 450)


elif select == "DATA EXPLORATION":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:

        method = st.radio("Select The Method",["Aggregated Transaction", "Aggregated User"])

        if method == "Aggregated Transaction":

            col1,col2= st.columns(2)
            with col1:

                years = st.slider("select the year",Aggre_transaction['Years'].min(),Aggre_transaction['Years'].max(),Aggre_transaction['Years'].min())
            tac_Y= Transaction_amount_count_Year(Aggre_transaction, years)


            col1,col2= st.columns(2)
            with col1:
                states=st.selectbox("select the state",tac_Y["States"].unique())
            Aggre_Trans_type(tac_Y,states)


            col1,col2= st.columns(2)           
            with col1:
                quaters = st.slider("select the quater",tac_Y['Quater'].min(),tac_Y['Quater'].max(),tac_Y['Quater'].min())
            Tacyq=Transaction_amount_count_Year_Quater(tac_Y,quaters)


            col1,col2= st.columns(2)
            with col1:
                states=st.selectbox("select the state_by_type",tac_Y["States"].unique())
            Aggre_Trans_type(Tacyq,states)


        elif method == "Aggregated User":

            col1,col2= st.columns(2)
            with col1:

                years = st.slider("select the year",Aggre_user['Years'].min(),Aggre_user['Years'].max(),Aggre_user['Years'].min())
            Aggre_u_p= Aggre_user_plot1(Aggre_user,years)

            col1,col2= st.columns(2)
            with col1: 

                 quaters = st.slider("select the quater",Aggre_u_p['Quater'].min(),Aggre_u_p['Quater'].max(),Aggre_u_p['Quater'].min())
            Aggre_u_p_Q =Aggre_user_plot2(Aggre_u_p,quaters)

            col1,col2= st.columns(2)
            with col1:
                states=st.selectbox("select the state",Aggre_u_p_Q["States"].unique())
            Aggre_user_plot3(Aggre_u_p_Q,states)

    with tab2:

        method2 = st.radio("Select The Method",["Map Transaction", "Map User"])

        if method2 == "Map Transaction":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("select the year MT",map_transaction['Years'].min(),map_transaction['Years'].max(),map_transaction['Years'].min())
            Map_tran_ac_year = Transaction_amount_count_Year(map_transaction, years)

            col1,col2= st.columns(2)
            with col1:

                states= st.selectbox("select the state MT",Map_tran_ac_year["States"].unique())
            Map_Tran_state(Map_tran_ac_year,states)

            col1,col2= st.columns(2)           
            with col1:

                quaters = st.slider("select the quater MT",Map_tran_ac_year['Quater'].min(),Map_tran_ac_year['Quater'].max(),Map_tran_ac_year['Quater'].min())
            Map_Tacyq=Transaction_amount_count_Year_Quater(Map_tran_ac_year,quaters)


            col1,col2= st.columns(2)
            with col1:

                states=st.selectbox("select the state quater MT",Map_Tacyq["States"].unique())
            Map_Tran_state(Map_Tacyq,states)


        elif method2 == "Map User":

            col1,col2= st.columns(2)
            with col1:

                years = st.slider("select the year MU",map_user['Years'].min(),map_user['Years'].max(),map_user['Years'].min())
            Map_user_Year= Map_user_plot1(map_user,years)

            col1,col2= st.columns(2)
            with col1:

                quaters = st.slider("select the quater_MU",Map_user_Year['Quater'].min(),Map_user_Year['Quater'].max(),Map_user_Year['Quater'].min())
            Map_user_Year_Q = Map_user_plot2(Map_user_Year,quaters)

            col1,col2= st.columns(2)
            with col1:

                states=st.selectbox("select the state MU",Map_user_Year_Q["States"].unique())
            Map_user_plot3(Map_user_Year_Q,states)

      

    with tab3:

        method3 = st.radio("Select The Method",["Top Transaction", "Top User"])

        if method3 == "Top Transaction":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("select the year TT",top_transaction['Years'].min(),top_transaction['Years'].max(),top_transaction['Years'].min())
            Top_tran_ac_year = Transaction_amount_count_Year(top_transaction, years)

            col1,col2= st.columns(2)
            with col1:

                states= st.selectbox("select the state_TT",Top_tran_ac_year["States"].unique())
            Top_trans_plot_1(Top_tran_ac_year,states)

            col1,col2= st.columns(2)           
            with col1:

                quaters = st.slider("select the quater_TT",Top_tran_ac_year['Quater'].min(),Top_tran_ac_year['Quater'].max(),Top_tran_ac_year['Quater'].min())
            Top_Tacyq=Transaction_amount_count_Year_Quater(Top_tran_ac_year,quaters)


        elif method3 == "Top User":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("select the year TU",top_user['Years'].min(),top_user['Years'].max(),top_user['Years'].min())
            Tups =Top_user_plot_1(top_user, years)    

            with col1:

                states= st.selectbox("select the state_TU",Tups["States"].unique())
            top_user_plot_2(Tups,states)

elif select == "TOP CHARTS":

    question= st.selectbox("Select the Question",["1. Which states have the highest total transaction amount and transaction count in Aggregated Transaction?",
                                                    "2. Which states have the lowest total transaction amount and transaction count in Aggregated Transaction?",
                                                    "3. What is Average of Transaction Amount and Count of Aggregated Transaction?",
                                                    "4. What are the top 10 transactions with the highest transaction amount?",
                                                    "5. What are the top 10 transactions with the lowest transaction amount?",
                                                    "6. What is Average of Transaction Amount and Count of Map Transaction?",
                                                    "7. What is the Transaction Count of Aggregated User?",
                                                    "8. What are the Highest, Lowest and Average Registered users of Map User?",
                                                    "9. What are the Highest, Lowest and Average Registered users of Top User?",
                                                    "10. What is the AppOpens of Map User?",
                                                    ])

    if question == "1. Which states have the highest total transaction amount and transaction count in Aggregated Transaction?":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_ttta("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_tttc("aggregated_transaction")

    elif question == "2. Which states have the lowest total transaction amount and transaction count in Aggregated Transaction?":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_ltta("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_lttc("aggregated_transaction")

    elif question == "3. What is Average of Transaction Amount and Count of Aggregated Transaction?":

        st.subheader("AVG OF TRANSACTION COUNT AND TRANSACTION AMOUNT")
        top_chart_avgta("aggregated_transaction")

        top_chart_avgtc("aggregated_transaction")

    elif question == "4. What are the top 10 transactions with the highest transaction amount?":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_ttta("map_transaction")

    elif question == "5. What are the top 10 transactions with the lowest transaction amount?":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_ltta("map_transaction")

    elif question == "6. What is Average of Transaction Amount and Count of Map Transaction?":

        st.subheader("AVG OF TRANSACTION COUNT AND TRANSACTION AMOUNT")
        top_chart_avgta("map_transaction")

        top_chart_avgtc("map_transaction")

    elif question == "7. What is the Transaction Count of Aggregated User?":

        st.subheader("TRANSACTION COUNT")
        top_chart_tttc("aggregated_user")

    elif question == "8. What are the Highest, Lowest and Average Registered users of Map User?":
        
        states= st.selectbox("Select the State ", map_user["States"].unique())   
        st.subheader("REGISTERED USERS")
        top_chart_ru("map_user", states)

    elif question == "9. What are the Highest, Lowest and Average Registered users of Top User?":
        
        st.subheader("REGISTERED USERS")
        top_chart_RU("top_user")

    elif question == "10. What is the AppOpens of Map User?":
          
        states= st.selectbox("Select the State", map_user["States"].unique())   
        st.subheader("APPOPENS")
        top_chart_appopens("map_user", states)



    




