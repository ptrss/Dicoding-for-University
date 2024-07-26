import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def create_avg_user_month(df):
    rename_month = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    avg_user_month = df.groupby(['mnth']).agg({'cnt': 'sum'}).reset_index()
    avg_user_month['mnth'] = avg_user_month['mnth'].map(rename_month)
    avg_user_month['cnt'] = (avg_user_month['cnt']/2).astype(int)
    
    return avg_user_month

def create_avg_user_day(df):
    avg_user_day = df.groupby(['weekday']).agg({'cnt': 'mean'}).reset_index()
    avg_user_day['cnt'] = avg_user_day['cnt'].astype(int)
    avg_user_day['weekday'] = avg_user_day['weekday'].map({0:'Sun', 1:'Mon', 2:'Tue', 3:'Wed', 4:'Thu', 5:'Fri', 6:'Sat'})
    
    return avg_user_day
    
def create_sum_user_day(df):
    sum_user_day = df.groupby(['dteday'])['cnt'].sum().reset_index()
    sum_user_day['cnt'] = sum_user_day['cnt'].astype(int)
    sum_user_day['dteday'] = pd.to_datetime(sum_user_day['dteday']).dt.strftime('%Y-%m-%d')
    sum_user_day.sort_values('cnt', ascending=False, inplace=True)
    sum_user_day.reset_index()
    
    return sum_user_day
    
def create_avg_hr_days(df):
    avg_hr_days = df.groupby(['hr', 'weekday']).agg({'cnt': 'mean'}).reset_index()
    avg_hr_days['cnt'] = avg_hr_days['cnt'].astype(int)
    avg_hr_days['weekday'] = avg_hr_days['weekday'].map({0:'Sunday', 1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday', 7:'Sunday', 8:'Monday', 9:'Tuesday', 10:'Wednesday', 11:'Thursday', 12:'Friday', 13:'Saturday', 14:'Sunday', 15:'Monday', 16:'Tuesday', 17:'Wednesday', 18:'Thursday', 19:'Friday', 20:'Saturday', 21:'Sunday', 22:'Monday', 23:'Tuesday'})
    
    return avg_hr_days
    
def create_sum_user_season(df):
    sum_user_season = df.groupby(['season']).agg({'cnt': 'sum'}).reset_index()
    sum_user_season['season'] = sum_user_season['season'].map({1:'Winter', 2:'Spring', 3:'Summer', 4:'Fall'})
    
    return sum_user_season
    
def create_avg_user_season(df):
    avg_user_season = df.groupby(['hr', 'season']).agg({'cnt': 'mean'}).reset_index()
    avg_user_season['cnt'] = avg_user_season['cnt'].astype(int)
    avg_user_season['season'] = avg_user_season['season'].map({1:'Winter', 2:'Spring', 3:'Summer', 4:'Fall'})
    
    return avg_user_season
    
def create_avg_user_reg(df):
    avg_user_reg = df.groupby(['workingday', 'hr'])['registered'].sum().reset_index()
    
    return avg_user_reg

def create_avg_user_cas(df):
    avg_user_cas = df.groupby(['workingday', 'hr'])['casual'].sum().reset_index()
    
    return avg_user_cas

def create_monthly_user(df):
    df['year_month'] = df['dteday'].dt.to_period('M')
    monthly_user = df.groupby('year_month').agg({'cnt': 'sum'}).reset_index()
    monthly_user['dteday'] = monthly_user['year_month'].dt.to_timestamp()
    
    return monthly_user

st.set_page_config(layout="wide")

# Import Dataset
df_hour = pd.read_csv('https://raw.githubusercontent.com/ptrss/Dicoding-for-University/main/Bike-sharing-dataset/hour.csv')
df_day = pd.read_csv('https://raw.githubusercontent.com/ptrss/Dicoding-for-University/main/Bike-sharing-dataset/day.csv')
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

# Create Data
avg_user_month = create_avg_user_month(df_day)
avg_user_day = create_avg_user_day(df_day)
sum_user_day = create_sum_user_day(df_day)
avg_hr_days = create_avg_hr_days(df_hour)
sum_user_season = create_sum_user_season(df_day)
avg_user_season = create_avg_user_season(df_hour)
avg_user_reg = create_avg_user_reg(df_hour)
avg_user_cas = create_avg_user_cas(df_hour)
monthly_user = create_monthly_user(df_day)

# Viz
st.image('capitalbikeshare.png')

st.header('Bike Sharing Demand Analysis 🚲')

col1, col2, col3 = st.columns(3)
with col1:
    total_users = df_day['cnt'].sum()
    st.metric('Total Users', f"{total_users:,}")
with col2:
    user_2011 = df_day[df_day['yr'] == 0]['cnt'].sum()
    st.metric('Users in 2011', f"{user_2011:,}")
with col3:
    user_2012 = df_day[df_day['yr'] == 1]['cnt'].sum()
    st.metric('Users in 2012', f"{user_2012:,}", '64.9%')

# Monthly Users
st.subheader('Monthly Users')

col1, col2 = st.columns(2)
with col1:
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=monthly_user, x='dteday', y='cnt', marker='o')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gcf().autofmt_xdate()
    plt.title('Monthly Users (2011-2012)', fontsize=18)
    plt.xlabel(None)
    plt.ylabel('Total Users', fontsize=12)
    st.pyplot(plt)
with col2:
    fig, ax = plt.subplots(figsize=(12, 7))
    my_palette = ['#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3', '#1F77B4', '#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3']
    sns.barplot(data=avg_user_month, x='mnth', y='cnt', palette=my_palette, errorbar=None, ax=ax)
    ax.set_title("Peak Usage Month", fontsize=18)
    ax.set_xlabel(None)
    ax.set_ylabel('Avg Users', fontsize=12)
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelsize=10)
    st.pyplot(fig)
   
# Daily Users 
st.subheader('Daily Users')

fig, ax = plt.subplots(figsize=(10, 4))
weekday_opt = ['All Days', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
option = st.selectbox('', weekday_opt, index=weekday_opt.index('All Days'))
if option == 'Sunday':
    sns.lineplot(data=avg_hr_days[avg_hr_days['weekday']=='Sunday'], x='hr', y='cnt', marker='o', errorbar=None, ax=ax)
    ax.set_title('Sunday Busy Hour', fontsize=10)
elif option == 'Monday':
    sns.lineplot(data=avg_hr_days[avg_hr_days['weekday']=='Monday'], x='hr', y='cnt', marker='o', errorbar=None, ax=ax)
    ax.set_title('Monday Busy Hour', fontsize=10)
elif option == 'Tuesday':
    sns.lineplot(data=avg_hr_days[avg_hr_days['weekday']=='Tuesday'], x='hr', y='cnt', marker='o', errorbar=None, ax=ax)
    ax.set_title('Tuesday Busy Hour', fontsize=10)
elif option == 'Wednesday':
    sns.lineplot(data=avg_hr_days[avg_hr_days['weekday']=='Wednesday'], x='hr', y='cnt', marker='o', errorbar=None, ax=ax)
    ax.set_title('Wednesday Busy Hour', fontsize=10)
elif option == 'Thursday':
    sns.lineplot(data=avg_hr_days[avg_hr_days['weekday']=='Thursday'], x='hr', y='cnt', marker='o', errorbar=None, ax=ax)
    ax.set_title('Thursday Busy Hour', fontsize=10)
elif option == 'Friday':
    sns.lineplot(data=avg_hr_days[avg_hr_days['weekday']=='Friday'], x='hr', y='cnt', marker='o', errorbar=None, ax=ax)
    ax.set_title('Friday Busy Hour', fontsize=10)
elif option == 'Saturday':
    sns.lineplot(data=avg_hr_days[avg_hr_days['weekday']=='Saturday'], x='hr', y='cnt', marker='o', errorbar=None, ax=ax)
    ax.set_title('Saturday Busy Hour', fontsize=10)
else:
    sns.lineplot(data=avg_hr_days, x='hr', y='cnt', marker='o', errorbar=None, ax=ax)
    ax.set_title('All Days Busy Hour', fontsize=10)
    
ax.set_xlabel(None)
ax.set_ylabel('Avg Users', fontsize=8)
ax.set_xticks(range(0, 24))
ax.set_ylim(avg_hr_days['cnt'].min() - 10, avg_hr_days['cnt'].max() + 10)
ax.tick_params(axis='y', labelsize=6)
ax.tick_params(axis='x', labelsize=6)
st.pyplot(fig)      
    
col1, col2 = st.columns(2)
with col1:
    my_palette = ['#1F77B4', "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(data=sum_user_day.head(5), x='dteday', y='cnt', palette=my_palette, errorbar=None, ax=ax)
    ax.set_title('Peak Usage Date', fontsize=18)
    ax.set_xlabel(None)
    ax.set_ylabel('Total Users', fontsize=12)
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelsize=10)
    st.pyplot(fig)
with col2:
    my_palette = ['#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3', '#1F77B4', '#D3D3D3']
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(data=avg_user_day, x='weekday', y='cnt', palette=my_palette, errorbar=None, order=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], ax=ax)
    ax.set_title('Buisest Day', fontsize=18)
    ax.set_xlabel(None)
    ax.set_ylabel('Avg Users', fontsize=12)
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelsize=10)
    st.pyplot(fig)
    
# Registered & Casual Users
st.subheader('Working Day vs Off Day Busy Hour')
col1, col2 = st.columns(2)
y_min_reg = avg_user_reg['registered'].min() - 10000; y_max_reg = avg_user_reg['registered'].max() + 10000
y_min_cas = avg_user_cas['casual'].min() - 10000; y_max_cas = avg_user_cas['casual'].max() + 10000
my_palette = ['#A0C6E5', '#1F77B4']
col1, col2 = st.columns(2)
with col1:
    col_1, col_2 = st.columns(2)
    with col_1:
        st.write('Member ⭐')
        st.metric('Peak Hour (Work Day)', f"{avg_user_reg[avg_user_reg['workingday']==1]['registered'].max():,}")
    with col_2:
        st.write('Member ⭐')
        st.metric('Peak Hour (Off Day)', f"{avg_user_reg[avg_user_reg['workingday']==0]['registered'].max():,}")
    registered_opt = ['All Days', 'Working Day', 'Off Day']
    option = st.selectbox('Registered Users', registered_opt, index=registered_opt.index('All Days'))
    fig, ax = plt.subplots(figsize=(12, 7))
    if option == 'Working Day':
        sns.lineplot(data=avg_user_reg[avg_user_reg['workingday']==1], x='hr', y='registered', marker='o', color='#1F77B4', errorbar=None, ax=ax)
        ax.set_title('Registered Users (Working Day)', fontsize=18)
    elif option == 'Off Day':
        sns.lineplot(data=avg_user_reg[avg_user_reg['workingday']==0], x='hr', y='registered', marker='o', color='#1F77B4', errorbar=None, ax=ax)
        ax.set_title('Registered Users (Off Day)', fontsize=18)
    else:
        sns.lineplot(data=avg_user_reg, x='hr', y='registered', hue='workingday', marker='o', palette=my_palette, errorbar=None, ax=ax)
        ax.set_title('Registered Users (All Days)', fontsize=18)
    ax.set_xlabel(None)
    ax.set_ylabel('Avg Users', fontsize=12)
    ax.set_ylim(y_min_cas, y_max_reg)
    ax.set_xticks(range(0, 24))
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelsize=10)
    st.pyplot(fig)
    
with col2:
    col_1, col_2 = st.columns(2)
    with col_1:
        st.write('Casual 🎭')
        st.metric('Peak Hour (Work Day)', f"{avg_user_cas[avg_user_cas['workingday']==1]['casual'].max():,}")
    with col_2:
        st.write('Casual 🎭')
        st.metric('Peak Hour (Off Day)', f"{avg_user_cas[avg_user_cas['workingday']==0]['casual'].max():,}")
    casual_opt = ['All Days', 'Working Day', 'Off Day']
    option = st.selectbox('Casual Users', casual_opt, index=casual_opt.index('All Days'))
    fig, ax = plt.subplots(figsize=(12, 7))
    if option == 'Working Day':
        sns.lineplot(data=avg_user_cas[avg_user_cas['workingday']==1], x='hr', y='casual', marker='o', color='#1F77B4', errorbar=None, ax=ax)
        ax.set_title('Casual Users (Working Day)', fontsize=18)
    elif option == 'Off Day':
        sns.lineplot(data=avg_user_cas[avg_user_cas['workingday']==0], x='hr', y='casual', marker='o', color='#1F77B4', errorbar=None, ax=ax)
        ax.set_title('Casual Users (Off Day)', fontsize=18)
    else:
        sns.lineplot(data=avg_user_cas, x='hr', y='casual', hue='workingday', marker='o', palette=my_palette, errorbar=None, ax=ax)
        ax.set_title('Casual Users (All Days)', fontsize=18)
    ax.set_xlabel(None)
    ax.set_ylabel('Avg Users', fontsize=12)
    ax.set_ylim(y_min_cas, y_max_reg)
    ax.set_xticks(range(0, 24))
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelsize=10)
    st.pyplot(fig)

# Seasonal Users
st.subheader('Seasonal Users')
col1, col2 = st.columns(2)
with col1:
    col_1, col_2 = st.columns(2)
    total_user_summer = df_day[df_day['season']==3]
    with col_1:
        reg_sum = total_user_summer['registered'].sum()
        st.metric('Member ⭐ (Summer)', f"{reg_sum:,}")
    with col_2:
        cas_sum = total_user_summer['casual'].sum()
        st.metric('Casual 🎭 (Summer)', f"{cas_sum:,}")
        
    
    my_palette = ['#D3D3D3', '#D3D3D3', '#1F77B4', '#D3D3D3']
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(data=sum_user_season, x='season', y='cnt', palette=my_palette, errorbar=None, ax=ax)
    ax.set_title(None)
    ax.set_xlabel(None)
    ax.set_ylabel('Total Users (x1,000,000)', fontsize=12)
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelsize=10)
    st.pyplot(fig)
with col2:
    season = ['All Seasons','Winter', 'Spring', 'Summer', 'Fall']
    option = st.selectbox('', season, index=season.index('Summer'))

    fig, ax = plt.subplots(figsize=(12, 7))

    if option == 'Winter':
        sns.lineplot(data=avg_user_season[avg_user_season['season'] == 'Winter'], x='hr', y='cnt', errorbar=None, color='#1F77B4', ax=ax)
        ax.set_title('Winter Busy Hour', fontsize=18)
    elif option == 'Spring':
        sns.lineplot(data=avg_user_season[avg_user_season['season'] == 'Spring'], x='hr', y='cnt', errorbar=None, color='#1F77B4', ax=ax)
        ax.set_title('Spring Busy Hour', fontsize=18)
    elif option == 'Summer':
        sns.lineplot(data=avg_user_season[avg_user_season['season'] == 'Summer'], x='hr', y='cnt', errorbar=None, color='#1F77B4', ax=ax)
        ax.set_title('Summer Busy Hour', fontsize=18)
    elif option == 'Fall':
        sns.lineplot(data=avg_user_season[avg_user_season['season'] == 'Fall'], x='hr', y='cnt', errorbar=None, color='#1F77B4', ax=ax)
        ax.set_title('Fall Busy Hour', fontsize=18)
    else:
        sns.lineplot(data=avg_user_season, x='hr', y='cnt', errorbar=None, hue='season', ax=ax)
        ax.set_title('All Seasons Busy Hour', fontsize=18)

    ax.set_xlabel(None)
    ax.set_ylabel('Avg Users', fontsize=12)
    ax.set_xticks(range(0, 24))
    ax.set_ylim(avg_user_season['cnt'].min() - 10, avg_user_season['cnt'].max() + 10)
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelsize=10)
    st.pyplot(fig)