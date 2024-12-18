import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def get_count_by_hour_df(hour_df):
    hour_count_df = hour_df.groupby(by="hours").agg({"count_cr": ["sum"]})
    return hour_count_df

def get_count_by_day_df(day_df):
    day_df_count = day_df.query(str('dateday >= "2011-01-01" and dateday < "2012-12-31"'))
    return day_df_count

def total_registered_df(day_df):
    reg_df = day_df.groupby(by="dateday").agg({
        "registered": "sum"
    })
    reg_df = reg_df.reset_index()
    reg_df.rename(columns={
        "registered": "registered_sum"
    }, inplace=True)
    return reg_df

def total_casual_df(day_df):
   cas_df =  day_df.groupby(by="dateday").agg({
      "casual": ["sum"]
    })
   cas_df = cas_df.reset_index()
   cas_df.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return cas_df

def sum_order (hour_df):
    sum_order_items_df = hour_df.groupby("hours").count_cr.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def season_info (day_df): 
    season_df = day_df.groupby(by="season").count_cr.sum().reset_index() 
    return season_df

days_df = pd.read_csv("day_new.csv")
hours_df = pd.read_csv("hour_new.csv")

datetime_columns = ["dateday"]
days_df.sort_values(by="dateday", inplace=True)
days_df.reset_index(inplace=True)   

hours_df.sort_values(by="dateday", inplace=True)
hours_df.reset_index(inplace=True)

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

min_date_days = days_df["dateday"].min()
max_date_days = days_df["dateday"].max()

min_date_hour = hours_df["dateday"].min()
max_date_hour = hours_df["dateday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://img.freepik.com/free-vector/flat-design-teamwork-concept_23-2149163763.jpg?w=900&t=st=1728059463~exp=1728060063~hmac=4bff9e713a40ce1080f690b214af17a9ba162010e5089054b9e96e355c111704")
    
        # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Time Frame',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_df_days = days_df[(days_df["dateday"] >= str(start_date)) & 
                       (days_df["dateday"] <= str(end_date))]

main_df_hour = hours_df[(hours_df["dateday"] >= str(start_date)) & 
                        (hours_df["dateday"] <= str(end_date))]

hour_count_df = get_count_by_hour_df(main_df_hour)
day_df_count_2011 = get_count_by_day_df(main_df_days)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
sum_order_items_df = sum_order(main_df_hour)
season_df = season_info(main_df_hour)

#Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('BIKE SHARING DASHBOARD')

st.subheader('Sharing Recap')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = day_df_count_2011.count_cr.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = reg_df.registered_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)

st.subheader("Tren Pengguna Sharing Beberapa Bulan Terakhir")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    days_df["dateday"],
    days_df["count_cr"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader("Musim Favorit Pengguna Persewaan Sepeda")

colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9"]
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
        y="count_cr", 
        x="season",
        data=season_df.sort_values(by="season", ascending=False),
        palette=colors,
        ax=ax
    )
ax.set_title("Grafik Antar Musim", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
 
st.pyplot(fig)

st.subheader("Jam Padat Penyewa Sepeda")

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(35, 15))
 
# membuat barplot untuk penyewa sepeda terbanyak 
sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.head(24), palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", 
                                                                                "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3", 
                                                                                "#D3D3D3", "#0339FC", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"], ax=ax)

# mengatur label dan judul untuk subplot pertama
ax.set_ylabel("Banyak Pelanggan", fontsize=30)
ax.set_xlabel("Hours", fontsize=30)
ax.set_title("Jam dengan banyak penyewa sepeda", loc="center", fontsize=30)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.subheader("Perbandingan Customer Registered dengan Customer Casual")

labels = 'casual', 'registered'
sizes = [18.8, 81.2]
explode = (0, 0.1) 

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',colors=["#D3D3D3", "#90CAF9"],
        shadow=True, startangle=90)
ax1.axis('equal')  

st.pyplot(fig1)