import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('./vehicles_us.csv')

# fill in missing values
df['paint_color'] = df['paint_color'].fillna('Unknown')
df['is_4wd'] = df['is_4wd'].fillna(0)

# fill out missing values under cylinders based on existing data
# assume if model and model year and cylinder data exist, it will be the median
grouped_medians = df.groupby(['model', 'model_year'])['cylinders'].median().reset_index()
grouped_medians.rename(columns={'cylinders': 'median_cylinders'}, inplace=True)

# merge new dataframe with median cylinder values back to main dataframe
df = pd.merge(df, grouped_medians, on=['model', 'model_year'], how='outer')
df['cylinders'] = df['cylinders'].fillna(df['median_cylinders'])

# convert to integer data type
df['is_4wd'] = df['is_4wd'].astype('int')

# extract manufacturer from model column
df['manufacturer'] = df['model'].str.split().str[0]

# remove the manufacture from model column
df['model'] = df['model'].str.split().str[1:].str.join(' ')

is_4wd_df = df[df['is_4wd'] == 1]
# is_not_4wd_df = df[df['is_4wd'] == 0]

# generate a list of types
vehicle_types = df['type'].unique()

# create plots
price_hist = px.histogram(df, x='price', nbins=40, title='Distribution of Vehicle Prices')
price_hist.update_xaxes(title_text='Price (in dollars)')
price_hist.update_yaxes(title_text='Number of Vehicles')

model_year_hist = px.histogram(df, x='model_year', title='Distribution of Vehicle Model Years')
model_year_hist.update_xaxes(title_text='Model Year')
model_year_hist.update_yaxes(title_text='Number of Vehicles')

condition_price_scatter = px.scatter(df, x='price', y ='condition', title='Scatterplot of Condition vs Vehicle Price')
condition_price_scatter.update_xaxes(title_text='Price (in dollars)')
condition_price_scatter.update_yaxes(title_text='Vehicle Condition')

condition_year_hist = px.histogram(df, x='model_year', color='condition', title='Histogram of Condition vs Model Year')
condition_year_hist.update_xaxes(title_text='Model Year')
condition_year_hist.update_yaxes(title_text='Number of Vehicles')

manufacturer_hist = px.histogram(df, x='manufacturer', color='type', title='Vehicle Types by Manufacturer')
manufacturer_hist.update_xaxes(title_text='Vehicle Manufacturer')
manufacturer_hist.update_yaxes(title_text='Number of Vehicles')

fuel_hist = px.histogram(df, x='fuel', title='Distribution of Vehicles by Fuel Type')
fuel_hist.update_xaxes(title_text='Fuel Type')
fuel_hist.update_yaxes(title_text='Number of Vehicles')

odometer_hist = px.histogram(df, x='odometer', nbins=40, title='Distribution of Vehicles Odometer Readings')
odometer_hist.update_xaxes(title_text='Mileage')
odometer_hist.update_yaxes(title_text='Number of Vehicles')

transmission_hist = px.histogram(df, x='transmission', nbins=40, title='Distribution of Vehicles by Transmission Type')
transmission_hist.update_xaxes(title_text='Transmission Type')
transmission_hist.update_yaxes(title_text='Number of Vehicles')

vehicle_type_hist = px.histogram(df, x='type', title='Distribution of Vehicle Types')
vehicle_type_hist.update_xaxes(title_text='Vehicle Type')
vehicle_type_hist.update_yaxes(title_text='Number of Vehicles')
vehicle_type_4wd_hist = px.histogram(is_4wd_df, x='type', title='Distribution of Vehicle Types')
vehicle_type_4wd_hist.update_xaxes(title_text='Vehicle Type')
vehicle_type_4wd_hist.update_yaxes(title_text='Number of Vehicles')

paint_color_hist = px.histogram(df, x='paint_color', title='Distribution of Vehicles by Paint Color')
paint_color_hist.update_xaxes(title_text='Paint Color')
paint_color_hist.update_yaxes(title_text='Number of Vehicles')

days_listed_hist = px.histogram(df, x='days_listed', color='type', nbins=30, title='Days Vehicle are Advertised')
days_listed_hist.update_xaxes(title_text='Number of Days on the Advertisement')
days_listed_hist.update_yaxes(title_text='Number of Vehicles')

# streamlit application layout
st.header("Car Sales from Advertisements")
st.plotly_chart(price_hist)
st.plotly_chart(model_year_hist)
st.plotly_chart(condition_price_scatter)
st.plotly_chart(condition_year_hist)

st.plotly_chart(manufacturer_hist)
selected_type = st.selectbox("Select Vehicle Type", vehicle_types)
manufacturer_filtered_df = df[df['type'] == selected_type]
manufacturer_filtered_hist = px.histogram(manufacturer_filtered_df, x='manufacturer', title=f'Vehicle Types by Manufacturer: {selected_type}', color='type')
st.plotly_chart(manufacturer_filtered_hist)

st.plotly_chart(fuel_hist)
st.plotly_chart(odometer_hist)
st.plotly_chart(transmission_hist)

show_4wd = st.checkbox('Show 4WD vehicles only')
if show_4wd:
    st.plotly_chart(vehicle_type_4wd_hist)
else:
    st.plotly_chart(vehicle_type_hist)

st.plotly_chart(paint_color_hist)
st.plotly_chart(days_listed_hist)