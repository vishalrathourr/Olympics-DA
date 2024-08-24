import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy

df = pd.read_csv('athlete_events.csv')
region = pd.read_csv('noc_regions.csv')

st.sidebar.title('Olympics Data Analysis')

rings= 'https://upload.wikimedia.org/wikipedia/en/b/b1/Olympic_Rings.svg'
st.sidebar.image(rings)


df = preprocessor.preprocess(df, region)


user_menu  = st.sidebar.radio(' ☰  Select an Option:',
                              ['📈 Overall Analysis', '🏅 Medal Analysis','🌎 Country wise Analysis','🤾 Athlete wise Analysis'])



if user_menu == '📈 Overall Analysis':
    st.title('📊 Top Statistics')

    editions = df['Year'].nunique()-1
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)

    with col2:
        st.header('Cities')
        st.title(cities)

    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)

    with col2:
        st.header('Nations')
        st.title(nations)

    with col3:
        st.header('Athletes')
        st.title(athletes)

    st.divider()

    nations_over_time = helper.data_over_time(df, 'region')
    st.header('Participating Nations over the years')
    fig = px.line(nations_over_time,  x="Edition", y="region")
    fig.update_layout(
        xaxis_title="Year",  
        yaxis_title="No. of Countries")
    st.plotly_chart(fig)

    st.divider()


    events_over_time = helper.data_over_time(df, 'Event')
    st.header('Events over the years')
    fig = px.line(events_over_time,  x="Edition", y="Event")
    fig.update_layout(
        xaxis_title="Year",  
        yaxis_title="No. of Events")
    fig.update_traces(line=dict(color='red'))  
    st.plotly_chart(fig)

    st.divider()


    athlete_over_time = helper.data_over_time(df, 'Name')
    st.header('Athletes over the years')
    fig = px.line(athlete_over_time,  x="Edition", y="Name")
    fig.update_layout(xaxis_title="Year", yaxis_title="No. of Athletes")
    fig.update_traces(line=dict(color='green'))  
    st.plotly_chart(fig)
    st.divider()


    st.header('No. of events over time')
    fig, ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0),
                     annot=True, cmap='Blues')
    st.pyplot(fig)
    st.divider()


    st.header('Most Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    'You selected: ', selected_sport
    x = helper.most_successful(df,selected_sport)
    x = x.reset_index(drop=True)
    st.table(x)
    st.divider()


#-------MEDAL ANALYSIS--------------

if user_menu == '🏅 Medal Analysis':
    st.sidebar.header('Medal Analysis')
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = helper.medals_analysis(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.header('🏅 Overall Analysis')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.header('🏅 Medal Analysis in ' + str(selected_year) + ' Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.header('🏅'+ selected_country + ' overall performance')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.header('🏅' + selected_country + ' performance in ' + str(selected_year) + ' Olympics') 
    
    medal_tally = medal_tally.reset_index(drop=True)
    st.table(medal_tally)


#-------COUNTRYWISE ANALYSIS-----------

if user_menu == '🌎 Country wise Analysis':
    st.sidebar.title('Country wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select the Country', country_list)
    
    st.header(selected_country + ' Male vs Female participation')
    gender = helper.countrywise_gender_participation(df, selected_country)
    fig = px.bar(gender, x='Year', y='Name', color='Sex', barmode='group',  color_discrete_map={'Male': 'orangered', 'Female': 'green'})
    fig.update_layout(xaxis_title="Year",  yaxis_title="Number of Participants",autosize=False, width=1200, height=400)
    st.plotly_chart(fig)
    st.divider()

    
    st.header(selected_country + ' Medal Analysis over the years')
    country_df = helper.yearwise_medal_analysis(df, selected_country)
    fig = px.line(country_df,  x='Year', y='Medal')
    st.plotly_chart(fig)
    st.divider()


    st.header(selected_country + ' Excels in the following sport')
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt, annot=True, cmap='Greens')
    st.pyplot(fig)
    st.divider()

    st.header("Top 10 athletes of "+ selected_country)
    top10 = helper.most_successful_countrywise(df, selected_country)
    top10 = top10.reset_index(drop=True)
    st.table(top10)
    st.divider()


#------ATHLETE WISE ANALYSIS---------------

if user_menu == '🤾 Athlete wise Analysis':
    st.header('Age distribution of Athletes')

    athlete_df = df.drop_duplicates(subset=['Name','region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(width=1200, height=500,margin=dict(l=50, r=50, t=50, b=50) )
    st.plotly_chart(fig)
    st.divider()



    st.header("Age distribution of Gold medalists")
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
    st.divider()

    st.header('Height vs Weight')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_vs_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x='Height', y='Weight', data=temp_df, hue='Medal', style='Sex', s=50)
    st.pyplot(fig)
    st.divider()


    st.header('Men vs Women participation over the years')
    final_df = helper.men_vs_women(df)
    fig = px.line(final_df, x='Year', y=['Male', 'Female'])
    fig.update_traces(line=dict(color='blue'), selector=dict(name='Male'))  
    fig.update_traces(line=dict(color='red'), selector=dict(name='Female'))  
    fig.update_layout(autosize=False, width=1000, height=500)    
    st.plotly_chart(fig)
    st.divider()



