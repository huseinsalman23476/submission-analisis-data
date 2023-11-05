import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_daily_bike_rentals_df(df):
    daily_bike_rentals_df = df.resample(rule='D', on='dteday').agg({
        "instant_x": "nunique",
        "casual_x" : "sum",
        "registered_x" : "sum",
        "cnt_x": "sum"
    }).reset_index()
    daily_bike_rentals_df["dteday"] = pd.to_datetime(daily_bike_rentals_df["dteday"]) 
    daily_bike_rentals_df.rename(columns={
        "casual_x" : "casual",
        "registered_x" : "registered",
        "cnt_x": "count"
    }, inplace=True)   
    return daily_bike_rentals_df

def create_byseason_df(df):
    byseason_df = df.groupby(by="season_label_x").agg({
        "casual_x": "sum",
        "registered_x": "sum",
        "cnt_x": "sum"
        }).sort_values(by="cnt_x", ascending=False).reset_index()
    byseason_df.rename(columns={
        "season_label_x" : "season",
        "casual_x" : "casual",
        "registered_x" : "registered",
        "cnt_x": "count"
        }, inplace=True)
    return byseason_df

def create_byweekday_df(df):
    byweekday_df = df.groupby(by="weekday_label_x").agg({
        "casual_x" : "sum",
        "registered_x" : "sum",
        "cnt_x": "sum"
    }).sort_values(by="cnt_x", ascending=False).reset_index()
    byweekday_df.rename(columns={
        "weekday_label_x": "weekday",
        "casual_x" : "casual",
        "registered_x" : "registered",
        "cnt_x": "count"
    }, inplace=True)
    return byweekday_df

def create_byhour_df(df):
    byhour_df = df.groupby(by="hr").agg({
        "casual_x" : "sum",
        "registered_x" : "sum",
        "cnt_x": "sum"
    }).sort_values(by="cnt_x", ascending=False).reset_index()
    byhour_df.rename(columns={
        "hr": "hour",
        "casual_x" : "casual",
        "registered_x" : "registered",
        "cnt_x": "count"
    }, inplace=True)
    byhour_df["hour"]= byhour_df["hour"].astype(str)
    return byhour_df

def create_byholiday_df(df):
    byholiday_df = df.groupby(by="holiday_label_x").agg({
        "casual_x" : "sum",
        "registered_x" : "sum",
        "cnt_x": "sum"
    }).sort_values(by="cnt_x", ascending=False).reset_index()
    byholiday_df.rename(columns={
        "holiday_label_x": "holiday",
        "casual_x" : "casual",
        "registered_x" : "registered",
        "cnt_x": "count"
    }, inplace=True)
    return byholiday_df

def create_byworkingday_df(df):
    byworkingday_df = df.groupby(by="workingday_label_x").agg({
        "casual_x" : "sum",
        "registered_x" : "sum",
        "cnt_x": "sum"
    }).sort_values(by="cnt_x", ascending=False).reset_index()
    byworkingday_df.rename(columns={
        "workingday_label_x": "workingday",
        "casual_x" : "casual",
        "registered_x" : "registered",
        "cnt_x": "count"
    }, inplace=True)
    return byworkingday_df

def create_byweathersit_df(df):
    byweathersit_df = df.groupby(by="weathersit_label_x").agg({
        "casual_x" : "sum",
        "registered_x" : "sum",
        "cnt_x": "sum"
    }).sort_values(by="cnt_x", ascending=False).reset_index()
    byweathersit_df.rename(columns={
        "weathersit_label_x": "weathersit",
        "casual_x" : "casual",
        "registered_x" : "registered",
        "cnt_x": "count"
    }, inplace=True)
    return byweathersit_df

def create_cluster_thw_df(df):
    cluster_thw_df = df.groupby(by="cluster_label").agg({
        "dteday" : "nunique",
        "temp_x" : "mean",
        "hum_x" : "mean",
        "windspeed_x" : "mean",
        "casual_x" : "sum",
        "registered_x" : "sum",
        "cnt_x": "sum"}).sort_values(by="cnt_x", ascending=False)

    cluster_thw_df.rename(columns={
        "temp_x" : "temp",
        "hum_x" : "hum",
        "windspeed_x" : "windspeed",
        "casual_x" : "casual",
        "registered_x" : "registered",
        "cnt_x": "count"
    }, inplace=True)
    
    return cluster_thw_df

# Load cleaned data
all_df = pd.read_csv("main_data.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()


with st.sidebar:
    # Menambahkan logo
    st.image("https://github.com/huseinsalman23476/submission-analisis-data/raw/main/assets/logo-bike-sharing.png")
    st.title("Date range")
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Pick a date :',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

# st.dataframe(main_df)

# # Menyiapkan berbagai dataframe
daily_bike_rentals_df = create_daily_bike_rentals_df(main_df)
byseason_df = create_byseason_df(main_df)
byweekday_df = create_byweekday_df(main_df)
byhour_df = create_byhour_df(main_df)
byholiday_df = create_byholiday_df(main_df)
byworkingday_df = create_byworkingday_df(main_df)
byweathersit_df = create_byweathersit_df(main_df)
cluster_thw_df = create_cluster_thw_df(main_df)


# plot number of daily bike rentals (2011-2012)

st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 24px;
    }
    </style>
    """,
        unsafe_allow_html=True,
)

st.header('Bike Sharing Dashboard :sparkles:')
st.subheader('Daily Bike Rentals')

col1, col2, col3 = st.columns(3)

with col1:
    total_bike_rentals = "{:,}".format(daily_bike_rentals_df["count"].sum())
    st.metric("Number of Bike Rentals", value=total_bike_rentals)

with col2:
    total_casual_bike_rentals = "{:,}".format(daily_bike_rentals_df["casual"].sum())
    st.metric("Number of Casual Bike Rentals", value=total_casual_bike_rentals)

with col3:
    total_registered_bike_rentals = "{:,}".format(daily_bike_rentals_df["registered"].sum())
    st.metric("Number of Registered Bike Rentals", value=total_registered_bike_rentals)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_bike_rentals_df["dteday"],
    daily_bike_rentals_df["count"],
    marker='o', 
    linewidth=2,
    color="#72BCD4",
    label="Total"
)
ax.plot(
    daily_bike_rentals_df["dteday"],
    daily_bike_rentals_df["casual"],
    marker='o', 
    linewidth=2,
    color="pink",
    label="Casual"
)
ax.plot(
    daily_bike_rentals_df["dteday"],
    daily_bike_rentals_df["registered"],
    marker='o', 
    linewidth=2,
    color="salmon",
    label="Registered"
)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
ax.legend(fontsize=14, loc="upper right")
st.pyplot(fig)

# by season
st.subheader("Bike Rentals by Season")
fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(20, 18))

sns.barplot(
    x="count", 
    y="season",
    hue="season",
    legend=False,
    data=byseason_df.sort_values(by="count", ascending=False),
    palette=["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"],
    ax=ax[0]
)
ax[0].set_title("Number of Bike Rentals", loc="center", fontsize=24)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].tick_params(axis='x', labelsize=20)
ax[0].tick_params(axis='y', labelsize=20)

byseason_df= byseason_df.sort_values(by="count", ascending=True)
byseason_df = byseason_df.loc[:, ["season", "casual", "registered"]]
byseason_df.plot.barh(x='season', stacked=True, color=['pink', 'salmon'], ax=ax[1])
ax[1].set_title("Number of Casual and Registered Bike Rentals", loc="center", fontsize=24)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].tick_params(axis='x', labelsize=20, rotation=0)
ax[1].tick_params(axis='y', labelsize=20, rotation=0)
ax[1].legend(fontsize=18, loc="lower right")
st.pyplot(fig)

# by weekday
st.subheader("Bike Rentals by Weekday")

fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(20, 18))

sns.barplot(
    x="count", 
    y="weekday",
    hue="weekday",
    legend=False,
    data=byweekday_df.sort_values(by="count", ascending=False),
    palette=["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"],
    ax=ax[0]
)
ax[0].set_title("Number of Bike Rentals", loc="center", fontsize=24)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].tick_params(axis='x', labelsize=18)
ax[0].tick_params(axis='y', labelsize=20)

byweekday_df= byweekday_df.sort_values(by="count", ascending=True)
byweekday_df = byweekday_df.loc[:, ["weekday", "casual", "registered"]]
byweekday_df.plot.barh(x='weekday', stacked=True, color=['pink', 'salmon'], ax=ax[1])
ax[1].set_title("Number of Casual and Registered Bike Rentals", loc="center", fontsize=24)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].tick_params(axis='x', labelsize=18, rotation=0)
ax[1].tick_params(axis='y', labelsize=20, rotation=0)
ax[1].legend(fontsize=18, loc="lower right")
st.pyplot(fig)

# by hour
st.subheader("Bike Rentals by Hour")

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(20, 28))

sns.barplot(
    x="count", 
    y="hour",
    hue="hour",
    legend=False,
    data=byhour_df.sort_values(by="count", ascending=False).head(12),
    palette=["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"],
    ax=ax[0,0]
)
ax[0,0].set_title("Best Number of Bike Rentals", loc="center", fontsize=20)
ax[0,0].set_ylabel(None)
ax[0,0].set_xlabel(None)
ax[0,0].tick_params(axis='x', labelsize=16)
ax[0,0].tick_params(axis='y', labelsize=20)

sns.barplot(
    x="count", 
    y="hour",
    hue="hour",
    legend=False,
    data=byhour_df.sort_values(by="count", ascending=True).head(12),
    palette=["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"],
    ax=ax[0,1]
)
ax[0,1].set_title("Worst Number of Bike Rentals", loc="center", fontsize=20)
ax[0,1].set_ylabel(None)
ax[0,1].set_xlabel(None)
ax[0,1].invert_xaxis()
ax[0,1].yaxis.set_label_position("right")
ax[0,1].yaxis.tick_right()
ax[0,1].tick_params(axis='x', labelsize=16)
ax[0,1].tick_params(axis='y', labelsize=20)

byhour_1_df = byhour_df.sort_values(by="count", ascending=False).head(12)
byhour_1_df = byhour_1_df.sort_values(by="count", ascending=True)
byhour_1_df = byhour_1_df.loc[:, ["hour", "casual", "registered"]]
byhour_1_df.plot.barh(x='hour', stacked=True, color=['pink', 'salmon'], ax=ax[1,0])
ax[1,0].set_title("Best Number of Casual and Registered Bike Rentals", loc="center", fontsize=20)
ax[1,0].set_ylabel(None)
ax[1,0].set_xlabel(None)
ax[1,0].tick_params(axis='x', labelsize=16, rotation=0)
ax[1,0].tick_params(axis='y', labelsize=20, rotation=0)
ax[1,0].legend(fontsize=18, loc="lower right")

byhour_2_df = byhour_df.sort_values(by="count", ascending=True).head(12)
byhour_2_df = byhour_2_df.sort_values(by="count", ascending=False)
byhour_2_df = byhour_2_df.loc[:, ["hour", "casual", "registered"]]
byhour_2_df.plot.barh(x='hour', stacked=True, color=['pink', 'salmon'], ax=ax[1,1])
ax[1,1].set_title("Worst Number of Casual and Registered Bike Rentals", loc="center", fontsize=20)
ax[1,1].set_ylabel(None)
ax[1,1].set_xlabel(None)
ax[1,1].invert_xaxis()
ax[1,1].yaxis.set_label_position("right")
ax[1,1].yaxis.tick_right()
ax[1,1].tick_params(axis='x', labelsize=16, rotation=0)
ax[1,1].tick_params(axis='y', labelsize=20, rotation=0)
ax[1,1].legend(fontsize=18, loc="upper left")

st.pyplot(fig)

# by holiday
st.subheader("Bike Rentals by Holiday")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))

sns.barplot(
    y="count", 
    x="holiday",
    hue="holiday",
    legend=False,
    data=byholiday_df.sort_values(by="count", ascending=False),
    palette=["#72BCD4", "#D3D3D3"],
    ax=ax[0]
)
ax[0].set_title("Number of Bike Rentals", loc="center", fontsize=22)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].tick_params(axis='x', labelsize=20, rotation=0)
ax[0].tick_params(axis='y', labelsize=18, rotation=0)

byholiday_df = byholiday_df.sort_values(by="count", ascending=False)
byholiday_df = byholiday_df.loc[:, ["holiday", "casual", "registered"]]
byholiday_df.plot.bar(x='holiday', stacked=True, color=['pink', 'salmon'], ax=ax[1])
ax[1].set_title("Number of Casual and Registered Bike Rentals", loc="center", fontsize=22)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].tick_params(axis='x', labelsize=20, rotation=0)
ax[1].tick_params(axis='y', labelsize=18, rotation=0)
ax[1].legend(fontsize=20, loc="upper right")
st.pyplot(fig)

# by working day
st.subheader("Bike Rentals by Working Day")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))

sns.barplot(
    y="count", 
    x="workingday",
    hue="workingday",
    legend=False,
    data=byworkingday_df.sort_values(by="count", ascending=False),
    palette=["#72BCD4", "#D3D3D3"],
    ax=ax[0]
)
ax[0].set_title("Number of Bike Rentals", loc="center", fontsize=22)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].tick_params(axis='x', labelsize=20, rotation=0)
ax[0].tick_params(axis='y', labelsize=18, rotation=0)


byworkingday_df = byworkingday_df.sort_values(by="count", ascending=False)
byworkingday_df = byworkingday_df.loc[:, ["workingday", "casual", "registered"]]
byworkingday_df.plot.bar(x='workingday', stacked=True, color=['pink', 'salmon'], ax=ax[1])
ax[1].set_title("Number of Casual and Registered Bike Rentals", loc="center", fontsize=22)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].tick_params(axis='x', labelsize=20, rotation=0)
ax[1].tick_params(axis='y', labelsize=18, rotation=0)
ax[1].legend(fontsize=20, loc="upper right")
st.pyplot(fig)

# by weather condition
st.subheader("Bike Rentals by Weather Condition")

fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(20, 18))

sns.barplot(
    x="count",
    y="weathersit", 
    hue="weathersit",
    legend=False,
    data=byweathersit_df.sort_values(by="count", ascending=False),
    palette=["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"],
    ax=ax[0]
)
ax[0].set_title("Number of Bike Rentals", loc="center", fontsize=30)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].tick_params(axis='x', labelsize=24, rotation=0)
ax[0].tick_params(axis='y', labelsize=24, rotation=0)

byweathersit_df = byweathersit_df.sort_values(by="count", ascending=True)
byweathersit_df = byweathersit_df.loc[:, ["weathersit", "casual", "registered"]]
byweathersit_df.plot.barh(x="weathersit", stacked=True, color=['pink', 'salmon'], ax=ax[1])
ax[1].set_title("Number of Casual and Registered Bike Rentals", loc="center", fontsize=30)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].tick_params(axis='x', labelsize=24, rotation=0)
ax[1].tick_params(axis='y', labelsize=24, rotation=0)
ax[1].legend(fontsize=24, loc="lower right")

st.pyplot(fig)


# clustering based on temperature, humadity, windspeed
st.subheader("Bike Rentals Based on Temperature (T), Humadity (H), Wind Speed (W)")

# cluster 1
st.caption("> High Temperature, Middle Humidity, Middle Wind Speed")
col1, col2, col3, col4 = st.columns(4)
with col1:
    avg_temp_c1 = str((cluster_thw_df["temp"]["High-T, Mid-H, Mid-W"] * 41).round(2)) + " °C"
    st.metric("Average of Temperature", value=avg_temp_c1)
with col2:
    avg_hum_c1 = str((cluster_thw_df["hum"]["High-T, Mid-H, Mid-W"] * 100).round(2)) + " %"
    st.metric("Average of Humidity", value=avg_hum_c1)
with col3:
    avg_windspeed_c1 = str((cluster_thw_df["windspeed"]["High-T, Mid-H, Mid-W"] * 67).round(2)) + " mph"
    st.metric("Average of Wind Speed", value=avg_windspeed_c1)

# cluster 3
st.caption("> Low Temperature, Low Humidity, High Wind Speed")
col1, col2, col3 = st.columns(3)
with col1:
    avg_temp_c3 = str((cluster_thw_df["temp"]["Low-T, Low-H, High-W"] * 41).round(2)) + " °C"
    st.metric("Average of Temperature", value=avg_temp_c3)
with col2:
    avg_hum_c3 = str((cluster_thw_df["hum"]["Low-T, Low-H, High-W"] * 100).round(2)) + " %"
    st.metric("Average of Humidity", value=avg_hum_c3)
with col3:
    avg_windspeed_c3 = str((cluster_thw_df["windspeed"]["Low-T, Low-H, High-W"] * 67).round(2)) + " mph"
    st.metric("Average of Wind Speed", value=avg_windspeed_c3)

# cluster 2
st.caption("> Middle Temperature, High Humidity, Low Wind Speed")
col1, col2, col3 = st.columns(3)
with col1:
    avg_temp_c2 = str((cluster_thw_df["temp"]["Mid-T, High-H, Low-W"] * 41).round(2)) + " °C"
    st.metric("Average of Temperature", value=avg_temp_c2)
with col2:
    avg_hum_c2 = str((cluster_thw_df["hum"]["Mid-T, High-H, Low-W"] * 100).round(2)) + " %"
    st.metric("Average of Humidity", value=avg_hum_c2)
with col3:
    avg_windspeed_c2 = str((cluster_thw_df["windspeed"]["Mid-T, High-H, Low-W"] * 67).round(2)) + " mph"
    st.metric("Average of Wind Speed", value=avg_windspeed_c2)

st.header('')

fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(20, 16))

cluster_thw_df = cluster_thw_df.reset_index()

sns.barplot(
    x="count", 
    y="cluster_label",
    hue="cluster_label",
    legend=False,
    data=cluster_thw_df.sort_values(by="count", ascending=False),
    palette=["#72BCD4", "#D3D3D3", "#D3D3D3"],
    ax=ax[0]
)
ax[0].set_title("Number of Bike Rentals", loc="center", fontsize=30)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].tick_params(axis='x', labelsize=24, rotation=0)
ax[0].tick_params(axis='y', labelsize=24, rotation=0)

cluster_thw_df = cluster_thw_df.sort_values(by="count", ascending=True)
cluster_thw_df = cluster_thw_df.loc[:, ["cluster_label", "casual", "registered"]]
cluster_thw_df.plot.barh(x='cluster_label', stacked=True, color=['pink', 'salmon'], ax=ax[1])
ax[1].set_title("Number of Casual and Registered Bike Rentals", loc="center", fontsize=30)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].tick_params(axis='x', labelsize=24, rotation=0)
ax[1].tick_params(axis='y', labelsize=24, rotation=0)
ax[1].legend(fontsize=24, loc="lower right")
st.pyplot(fig)

st.caption('Copyright © Dicoding 2023')