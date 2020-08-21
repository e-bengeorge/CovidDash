# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 13:29:38 2020

@author: Ben George
"""

import streamlit as st
import altair as alt
import pandas as pd 



st.cache(persist=True)
def load_data():
    covid=pd.read_csv("data.csv")
    covid["Date"]=pd.to_datetime(covid["Date"],format="%d-%m-%Y")
    return covid
covid= load_data()

st.title('Covid-19 Dashborad')
"Scroll the mouse over the Charts to feel the interactiveness of the Charts"
"The data considerd for this analysis is from 01-02-2020 to 31-07-2020"


cty = st.selectbox("Select country",covid["Country"][:186])

death= alt.Chart(covid[covid["Country"]==cty]).mark_circle(color='green').encode(
    x="Date",
    y="New cases",
    tooltip=["Date","Country","New deaths"]
).interactive()

st.header(f"View Daily Cases for {cty}")

st.altair_chart(death)

a= alt.Chart(covid[covid["Country"]==cty],width=500,height=400).mark_bar().encode(
    x="day(Date):O",
    y="month(Date):O",
    color="sum(New deaths)",
    tooltip="sum(New deaths)"
)

b=alt.Chart(covid[covid["Country"]==cty],width=500,height=400).mark_text().encode(
    x="day(Date):O",
    y="month(Date):O",
    text="sum(New deaths)" 
)

c= alt.Chart(covid[covid["Country"]==cty],width=500,height=100).mark_bar().encode(
    x="day(Date):O",
   # y="month(Date):O",
    color="sum(New deaths)",
    tooltip="sum(New deaths)"
)

d=alt.Chart(covid[covid["Country"]==cty],width=500,height=100).mark_text().encode(
    x="day(Date):O",
    #y="month(Date):O",
    text="sum(New deaths)" 
)
st.header(f"View deaths for {cty} by Day/Month")

op = st.radio(
     "Select the option",
     ('Day and Month', 'Day'))

if op == 'Day and Month':
     st.altair_chart(a+b)
else:
     st.altair_chart(c+d)
tot = covid[covid["Country"]==cty]['New deaths'].sum()

st.subheader(f"Total Deaths for {cty} = {tot}")

st.header(f"View Total Confirmed vs Total Recovered for {cty}")

con=alt.Chart(covid[covid["Country"]==cty]).mark_area(color="purple").encode(
    x="Date",
    y="Confirmed",
    tooltip=["Date","Confirmed"]
    
).interactive()

rec=alt.Chart(covid[covid["Country"]==cty]).mark_area(color="green").encode(
    x="Date",
    y="Recovered",
    tooltip=["Date","Recovered"]
    
).interactive()

opt = st.radio(
     "Select the option",
     ('Confirmed', 'Recovered','Confirmed and Recovered'))

if opt == 'Confirmed':
     st.altair_chart(con)
elif opt == 'Recovered':
    st.altair_chart(rec)
else:
     st.altair_chart(con+rec)

st.header(f"Daily New Cases and Total Cases for Selected Countries")

options = st.multiselect(
        'Select Multiple Countries',
        covid["Country"][:186])
 


fire=alt.Chart(covid[covid["Country"].isin(options)],width=500,height=300).mark_circle().encode(
    x="Date",
    y="Country",
    tooltip=["Date","Country","New cases"],
    color="Country",
    size="New cases"
).interactive()

bar1 = alt.Chart(covid[covid["Country"].isin(options)]).mark_bar().encode(
    y="sum(New cases)",
    x=alt.X("Country",sort="-y"),
    color="Country",
    tooltip = "sum(New cases)"
).interactive()

st.altair_chart(fire | bar1)

if st.checkbox("Click to View the Dataset",False):
    "Select the Month from Slider"
    nc = st.slider("Month",2,7,2,1)
    covid = covid[covid["Date"].dt.month ==nc]
    "data", covid
    




    
