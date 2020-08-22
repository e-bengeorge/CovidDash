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
    latest=covid[covid["Date"] == "2020-07-31"]
    return covid,latest
covid,latest= load_data()

st.title('Covid-19 Dashborad')

st.sidebar.markdown(''' 
The main aim of this app is to give insights about Covid-19 Infections around the world.

The data considerd for this analysis is from 01-02-2020 to 31-07-2020

Select the different options to vary the Visualization

All the Charts are interactive. 

Scroll the mouse over the Charts to feel the interactiveness like Tool tip, Zoom, Pan
                    

Designed by: 
**Ben George**  ''')  
    
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
  

confirm = latest.sort_values("Confirmed",ascending=False)[["Country","Confirmed"]].head()

confirm.reset_index(inplace = True,drop = True)

bar2 = alt.Chart(confirm).mark_bar().encode(
    x="Confirmed",
    y=alt.Y("Country",sort="-x"),
    color=alt.Color("Country",legend=None),
    tooltip = "Confirmed"
).interactive()


death = latest.sort_values("Deaths",ascending=False)[["Country","Deaths"]].head()

death.reset_index(inplace = True,drop = True)

bar3 = alt.Chart(death).mark_bar().encode(
    x="Deaths",
    y=alt.Y("Country",sort="-x"),
    color=alt.Color("Country",legend=None),
    tooltip = "Deaths"
).interactive()



deathper=latest["Deaths"] / latest["Confirmed"] * 100
lat = latest.copy()
lat["Death Percentage"] = deathper
deathp = lat.sort_values("Death Percentage",ascending=False)[["Country","Death Percentage"]].head()

deathp.reset_index(inplace = True,drop = True)

bar4 = alt.Chart(deathp).mark_bar().encode(
    x="Death Percentage",
    y=alt.Y("Country",sort="-x"),
    color=alt.Color("Country",legend=None),
    tooltip = "Death Percentage"
).interactive()


recover = latest.sort_values("Recovered",ascending=False)[["Country","Recovered"]].head()

recover.reset_index(inplace = True,drop = True)

bar5 = alt.Chart(recover).mark_bar().encode(
    x="Recovered",
    y=alt.Y("Country",sort="-x"),
    color=alt.Color("Country",legend=None),
    tooltip = "Recovered"
).interactive()


recper=latest["Recovered"] / latest["Confirmed"] * 100
lat = latest.copy()
lat["Recovered Percentage"] = recper
recp = lat.sort_values("Recovered Percentage",ascending=False)[["Country","Recovered Percentage"]].head()

recp.reset_index(inplace = True,drop = True)

bar6 = alt.Chart(recp).mark_bar().encode(
    x="Recovered Percentage",
    y=alt.Y("Country",sort="-x"),
    color=alt.Color("Country",legend=None),
    tooltip = "Recovered Percentage"
).interactive()


st.header(f"Do you want to know the Top 5 countries")
top = st.selectbox("Select your option",["Confirmed Cases","Deaths","Death Percentage","Recovered","Recovered Percentage"])
if top == "Confirmed Cases":
    st.altair_chart(bar2)
elif top == "Deaths":
    st.altair_chart(bar3)
elif top == "Death Percentage":
    st.altair_chart(bar4)
elif top == "Recovered":
    st.altair_chart(bar5)
else:
    st.altair_chart(bar6)
    
if st.checkbox("Click to View the Dataset",False):
    "Select the Month from Slider"
    nc = st.slider("Month",2,7,2,1)
    covid = covid[covid["Date"].dt.month ==nc]
    "data", covid


    

