import numpy as np


def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC','Games','Year','Season','City','Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending =False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] +  medal_tally['Silver'] +  medal_tally['Bronze']
    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years, country 

def medals_analysis(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC','Games','Year','Season','City','Sport', 'Event', 'Medal'])
    flag = 0    
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1 
        temp_df = medal_df[medal_df['region'] == country]     
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == year]      
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year']==year) & (medal_df['region']==country)]

    if flag == 1:
        medals = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        medals = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending =False).reset_index()
        
    medals['total'] = medals['Gold'] +  medals['Silver'] +  medals['Bronze']
    return medals

def data_over_time(df,col):
    data_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    data_over_time.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)
    return data_over_time

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])
    
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Get the top 15 successful athletes based on the number of medals won
    top_athletes = temp_df['Name'].value_counts().reset_index().head(15)
    top_athletes.columns = ['Name', 'Medal Count']  

    # Merge to get additional athlete details from the original dataframe
    result = top_athletes.merge(df, on='Name', how='left')[['Name','Medal Count','Sport','region']].drop_duplicates('Name')
    return result

def yearwise_medal_analysis(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def countrywise_gender_participation(df, country):
    gender = df[df['region'] == country].groupby(['Year', 'Sex']).count()['Name'].reset_index()
    gender['Sex'] = gender['Sex'].replace({'M': 'Male', 'F': 'Female'})
    return gender


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    top_athletes = temp_df['Name'].value_counts().reset_index().head(10)
    top_athletes.columns = ['Name', 'Medal Count']  
    result = top_athletes.merge(df, on='Name', how='left')[['Name','Medal Count','Sport']].drop_duplicates('Name')
    return result

def weight_vs_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df
    
def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()  
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x':'Male', 'Name_y':'Female'}, inplace=True)
    final.fillna(0,inplace=True)
    return final