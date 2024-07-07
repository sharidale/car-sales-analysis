import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('./vehicles_us.csv')

# fill in missing values
df['paint_color'] = df['paint_color'].fillna('Unknown')
df['is_4wd'] = df['is_4wd'].fillna(0)

# convert to integer data type
df['is_4wd'] = df['is_4wd'].astype('int')

# extract manufacturer from model column
df['manufacturer'] = df['model'].str.split().str[0]

# remove the manufacture from model column
df['model'] = df['model'].str.split().str[1:].str.join(' ')

is_4wd_df = df[df['is_4wd'] == 1]
# is_not_4wd_df = df[df['is_4wd'] == 0]

# plots
price_hist = px.histogram(df, x='price', nbins=40, title='Distribution of Vehicle Prices')
model_year_hist = px.histogram(df, x='model_year', title='Distribution of Vehicle Model Years')
condition_price_scatter = px.scatter(df, x='price', y ='condition', title='Scatterplot of Condition vs Vehicle Price')
condition_year_hist = px.histogram(df, x='model_year', color='condition', title='Histogram of Condition vs Model Year')
manufacturer_hist = px.histogram(df, x='manufacturer', color='type', title='Vehicle Types by Manufacturer')
fuel_hist = px.histogram(df, x='fuel', title='Distribution of Vehicles by Fuel Type')
odometer_hist = px.histogram(df, x='odometer', nbins=40, title='Distribution of Vehicles Odometer Readings')
transmission_hist = px.histogram(df, x='transmission', nbins=40, title='Distribution of Vehicles by Transmission Type')
vehicle_type_hist = px.histogram(df, x='type', title='Distribution of Vehicle Types')
vehicle_type_4wd_hist = px.histogram(is_4wd_df, x='type', title='Distribution of Vehicle Types')
paint_color_hist = px.histogram(df, x='paint_color', title='Distribution of Vehicles by Paint Color')

# streamlit
st.header("Car Sale Advertisements")
st.plotly_chart(price_hist)
st.plotly_chart(model_year_hist)
st.plotly_chart(condition_price_scatter)
st.plotly_chart(condition_year_hist)
st.plotly_chart(manufacturer_hist)
st.plotly_chart(fuel_hist)
st.plotly_chart(odometer_hist)
st.plotly_chart(transmission_hist)
show_4wd = st.checkbox('Show 4WD vehicles only')
if show_4wd:
    st.plotly_chart(vehicle_type_4wd_hist)
else:
    st.plotly_chart(vehicle_type_hist)
st.plotly_chart(paint_color_hist)
