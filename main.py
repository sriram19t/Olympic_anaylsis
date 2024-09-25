import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
st.set_page_config(page_title='Olympic_anaylsis',layout='wide',page_icon="🏅")
option=st.sidebar.radio(
    ':red[navigate]',
    ('Medal_Tally','Overall_anaylsis','Country_wise_anaylsis','Season_anaylsis','Sport_wise anaylsis','Athelete_anaylsis')

)

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df=df.merge(df_region,on='NOC',how='left')
df['Medal'].fillna('No_medal',inplace=True)
df['region']=df['region'].fillna(df['Team'])
df1new=df.copy()
df.drop_duplicates(['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)

def country_anaylsis(region_name):
    fig1,(ax1,ax4)=plt.subplots(1,2,figsize=(10,6))
    fig2,ax2=plt.subplots(figsize=(10,10))
    
    data=df[df['region']==region_name]
  

    name_wise=data[data['Medal']!='No_medal'].groupby('Name')['Medal'].value_counts().unstack(level=1).fillna(0).astype('int32')
    name_wise['total']=name_wise.sum(axis=1)
    st.subheader(f':red[Pie chart of the differnt medals and heat map of medals in the basis of gender of {region_name}]')
    ax1.pie(data['Medal'][data['Medal']!='No_medal'].value_counts(),labels=data['Medal'][data['Medal']!='No_medal'].value_counts().index,autopct='%.1f%%')
    ax1.set_xlabel(region_name)
    ax1.set_title("Overall percentage")
    # Add debugging statements to check the condition and filtered data
    print("Filtered data shape:", data[data['Medal']=='No_medal'].shape[0])
    # print("Filtered data sample:", data[data['Medal'] != 'No_medal'].head())

    
    # female and male percentage
    if data[data['Medal']!='No_medal'].shape[0]<1:
        st.write(f'Country {region_name} did not won any olympic medal yet hoping they will soon')
        st.stop()
    else:
        sns.heatmap(data[data['Medal']!='No_medal'].groupby('Sex')['Medal'].value_counts().unstack(level=1),annot=True,fmt='.0f',ax=ax4)
        st.pyplot(fig1)

    st.header(f'{region_name} heatmap of differnt sports')
    
    sns.heatmap((data[data['Medal']!='No_medal'].groupby('Sport')['Medal'].value_counts().unstack(level=1)),ax=ax2,annot=True,fmt='.0f')
    st.pyplot(fig2)
    st.header(f'{region_name}''s top 10 athelts')

    athelete_data=data[data['Medal']!='No_medal'].groupby('Name')['Medal'].value_counts().unstack(level=1).fillna(0)
    print(athelete_data)
    athelete_data['Total']=athelete_data.sum(axis=1)
    athelete_data.sort_values(['Total','Gold','Silver','Bronze'],ascending=False,inplace=True)
    athelete_data=athelete_data[['Gold','Silver','Bronze','Total']]
    st.dataframe(athelete_data.head(10),width=1000,height=400)


    st.write(data['Medal'].value_counts())


def Season_anaylsis(Season):
    st.write(f'Anyalsis of Olympics of year {Season}')
    data=df[(df['Year']==Season) & (df['Medal']!='No_medal')]
    st.header(f'Top 10 countries in the Olympics of {Season}')
    top_10_countries=data.groupby('region')['Medal'].value_counts().unstack(level=1)
    top_10_countries['Total']=top_10_countries.sum(axis=1)
    top_10_countries.sort_values(['Total','Gold','Silver','Bronze'],ascending=False,inplace=True)
    st.dataframe(top_10_countries,width=1000,height=400)
    st.write("Heat map of top countries in that season")
    fig1,ax1=plt.subplots(figsize=(10,10))
    sns.heatmap(top_10_countries.head(10),ax=ax1,annot=True,fmt='.0f')
    st.pyplot(fig1)


def medaltally(year,country):
            



    if year!='Overall':
        
        year=np.int64(year)
        medal_country_wise=df[(df['Medal']!='No_medal') & (df['Year']==year)].groupby(['region'])['Medal'].value_counts().unstack(level=1)
        medal_country_wise.fillna(0,inplace=True)
        medal_country_wise['Total_medals']=medal_country_wise.fillna(0).sum(axis=1)
        medal_country_wise.sort_values(['Total_medals','Gold','Silver','Bronze'],ascending=False,inplace=True)
        medal_country_wise.reset_index(inplace=True)
        medal_country_wise['all_time_rank']=np.arange(1,len(medal_country_wise)+1)
        medal_country_wise=medal_country_wise[['all_time_rank','region','Gold','Silver','Bronze','Total_medals']]
        medal_country_wise.index=medal_country_wise['all_time_rank']
        medal_country_wise.drop(['all_time_rank'],inplace=True,axis=1)
        if country!='Overall':
            st.dataframe(medal_country_wise[medal_country_wise['region']==country],height=len(medal_country_wise),width=1000)
        else:
            st.dataframe(medal_country_wise,height=len(medal_country_wise),width=1000)

    else:
        st.write(':blue[All time medal tally of all countries]')
        medal_country_wise=df[df['Medal']!='No_medal'].groupby(['region'])['Medal'].value_counts().unstack(level=1)
        medal_country_wise.fillna(0,inplace=True)
        medal_country_wise['Total_medals']=medal_country_wise.fillna(0).sum(axis=1)
        medal_country_wise.sort_values(['Total_medals','Gold','Silver','Bronze'],ascending=False,inplace=True)
        medal_country_wise.reset_index(inplace=True)
        medal_country_wise['all_time_rank']=np.arange(1,len(medal_country_wise)+1)
        print(medal_country_wise.columns)
        medal_country_wise=medal_country_wise[['all_time_rank','region','Gold','Silver','Bronze','Total_medals']]
        medal_country_wise.index=medal_country_wise['all_time_rank']
        medal_country_wise.drop(['all_time_rank'],inplace=True,axis=1)
        if country!='Overall':
            st.dataframe(medal_country_wise[medal_country_wise['region']==country],height=len(medal_country_wise),width=1000)
        else:
            st.dataframe(medal_country_wise,height=len(medal_country_wise)*10,width=1000)   


def Overall_anaylsis():
    regions=df1new['region'].unique().shape[0]
    sports=df1new['Sport'].unique().shape[0]
    cities=df1new['City'].unique().shape[0]
    seasons=df1new['Year'].unique().shape[0]-1
    Events=df1new['Event'].unique().shape[0] 
    athelets=df1new['Name'].unique().shape[0]
    col1,col2,col3=st.columns([1,2,3])
    with col1:
        st.subheader('Total Editions')
        st.title(seasons)
        st.subheader('Total Countries')
        st.title(regions) 
    with col2:
        st.subheader('Total Citis participated')
        st.title(cities)
        st.subheader('Total Events',)
        st.title(Events)
    with col3:
        st.subheader('sports count')
        st.title(sports)
        st.subheader('athelete count')
        st.title(athelets)
    st.subheader('Chart of no_of_participating_countries over the years for summer olympics')
    k=df[df['Year']%4==0].groupby('Year')['region'].unique().str.len().sort_index().reset_index()
    k.rename(columns={
        'region':'no_of_participating_countries',
        'Year':'Season'}
        ,inplace=True)
    fig=px.line(k,x='Season',y='no_of_participating_countries')
    fig.update_layout(width=800, height=600)

    st.plotly_chart(fig)
    st.subheader('Chart of no_of_participating_countries over the years for winter olympics')
    k=df[(df['Year']%4!=0)].groupby('Year')['region'].unique().str.len().sort_index().reset_index()
    k.rename(columns={
        'region':'no_of_participating_countries',
        'Year':'Season'}
        ,inplace=True)
    fig=px.line(k,x='Season',y='no_of_participating_countries')
    fig.update_layout(width=800, height=600)
    st.plotly_chart(fig)

    st.subheader('Chart of no_of_events over the years for summer olympics')
    k=df[df['Year']%4==0].groupby('Year')['Event'].unique().str.len().sort_index().reset_index()
    k.rename(columns={
        'Event':'no_of_Events',
        'Year':'Season'}
        ,inplace=True)
    fig=px.line(k,x='Season',y='no_of_Events')
    fig.update_layout(width=800, height=600)

    st.plotly_chart(fig)
    st.subheader('Chart of no_of_events over the years for winter olympics')
    k=df[(df['Year']%4!=0)].groupby('Year')['Event'].unique().str.len().sort_index().reset_index()
    k.rename(columns={
        'Event':'no_of_Events',
        'Year':'Season'}
        ,inplace=True)
    fig=px.line(k,x='Season',y='no_of_Events')
    fig.update_layout(width=800, height=600)
    st.plotly_chart(fig)
    
    st.title('Count of events over the years')
    fig1,ax1=plt.subplots(figsize=(30,30))
    x=df.drop_duplicates(['Year','Event','Sport'])
    sns.heatmap(x.groupby('Sport')['Year'].value_counts().unstack(level=1).fillna(0).astype('int32'),annot=True,ax=ax1,fmt='.0f')
    st.pyplot(fig1)

    st.write(':Blue[Top 10 athelets of all time]')
    athelet_top10=df1new[df1new['Medal']!='No_medal']
    athelet_top10=athelet_top10.groupby('Name')['Medal'].value_counts().unstack(level=1).fillna(0).astype('int32')
    athelet_top10['Total']=athelet_top10.sum(axis=1)
    athelet_top10=athelet_top10.astype('int32').sort_values(['Total','Gold','Silver','Bronze'],ascending=False).head(10)
    st.dataframe(athelet_top10)




    










    
    





    
    

    

if option=='Country_wise_anaylsis':

    st.subheader('Country_wise_Anaylsis')
    country=st.selectbox(
        'Select Country',
        df['region'].unique()
    )
    st.write(country)
    st.write(f'Anyalsis of the respective country {country}')
    country_anaylsis(country)
elif option=='Season_anaylsis':
    st.subheader('Season anaylsis')

    Year=st.selectbox(
        'Select Year',
        np.sort(df['Year'].unique())[::-1]
    )
    Season_anaylsis(Year)

elif option=='Medal_Tally':
    st.subheader('MedalTally')
    Year=st.sidebar.selectbox(
        'Select Year',
        np.append(['Overall'],np.sort(df['Year'].unique()))
    )

    country=st.sidebar.selectbox(
        'Select Country',
        np.append(['Overall'],np.sort(df['region'].unique()))
    )
    medaltally(Year,country)

elif option=='Overall_anaylsis':
    st.header('Top Statstics')
    Overall_anaylsis()