# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 13:29:38 2020

@author: Ben George
"""

import streamlit as st
import altair as alt
import pandas as pd 
import numpy as np

# py lib for 3D map viz from uber

st.cache(persist=True)
def load_data():
    covid=pd.read_csv("data.csv")
    covid["Date"]=pd.to_datetime(covid["Date"],format="%d-%m-%Y")
    top5 = ["US","Brazil","India","Russia","South Africa"]
    top = covid[covid["Country"].isin(top5)]
    return covid, top
covid,top = load_data()

st.title('Covid-19 Dashborad')

#cty = st.selectbox("Select country",covid["Country"])
cty = st.selectbox("Select country",covid["Country"][:186])
#top = top[top["Country"]==cty]
#n= st.number_input("Num")
death= alt.Chart(covid[covid["Country"]==cty]).mark_circle().encode(
    x="Date",
    y="New deaths",
    tooltip=["Date","Country","New deaths"]
).interactive()

st.header(f"View scatter plot for {cty}")

st.altair_chart(death)
st.balloons()
# Find the details of death
a= alt.Chart(covid[covid["Country"]==cty],width=500,height=400).mark_bar().encode(
    x="day(Date):O",
    y="month(Date):O",
    color="sum(New deaths)",
    tooltip="sum(New deaths)"
)

b=alt.Chart(covid[covid["Country"]==cty],width=500,height=400).mark_text().encode(
    x="day(Date):O",
    y="month(Date):O",
    #color="sum(New deaths)",
    text="sum(New deaths)"
   
)

st.header(f"View deaths for {cty}")

st.altair_chart(a+b)

st.header(f"Daily new cases for top countries")
fire=alt.Chart(top,width=500,height=300).mark_circle().encode(
    x="Date",
    y="Country",
    tooltip=["Date","Country","New cases"],
    color="Country",
    size="New cases"
).interactive()

st.altair_chart(fire)

st.header(f"View the Dataset")
nc = st.slider("Month",2,7)
covid = covid[covid["Date"].dt.month ==nc]
"data", covid

"## Map Data"
if st.checkbox('Show dataframe'):
    st.line_chart(covid["Confirmed"])
    
"## selectbox"
option = st.selectbox(
    'Which number do you like best?',
    covid['Date'][:186])

'You selected: ', option

status_text.text('Done!')
st.balloons()
