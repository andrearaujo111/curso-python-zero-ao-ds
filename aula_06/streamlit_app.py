# IMPORTS
import pandas as pd
import streamlit as st
import folium
import geopandas
import plotly.express as px
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

# set the default float format
pd.options.display.float_format = '{:,.2f}'.format

# set visualization objects in page wider
st.set_page_config(layout='wide')

# FUNCTIONS

def convert_to_m2(data, col=None):
    '''
    :param data: DataFrame or Series
    :param col: The Column of the DataFrame to be converted. If Series, no need to be declared
    :return: Series with converted values
    '''
    m2 = round(data[col] * 0.092903, 2)
    return m2


### DATA EXTRACTION ###
######################################

# Geodata extract function
@st.cache(allow_output_mutation=True)
def get_geofile(path):
    '''
    :param path: Path file that constains geo space information
    :return: DataFrame
    '''
    geofile = geopandas.read_file(path)

    return geofile

# Data extraction function
@st.cache(allow_output_mutation=True)
def get_data(path):
    '''
    :param path: Path of csv file to be read
    :return: DataFrame
    '''
    data = pd.read_csv(path)

    return data


# DATA PREPARATION

# Data preparation function
def data_preparing(data):
    '''
    :param data: DataFrame that will be changed
    :return: Changed DataFrame
    '''
    # casts the sqft lot to square meter
    data['m2_lot'] = convert_to_m2(data, 'sqft_lot')

    # sets the price of m2 per property
    data['m2_lot_price'] = data['price']/data['m2_lot']

    # casts date column to datetime format
    data['date'] = pd.to_datetime(data['date']).dt.strftime('%d-%m-%Y')

    # swith waterfront types of data fromm 0/1 to yes/no
    data['waterfront'] = data['waterfront'].apply(lambda x: 'yes' if x == 1 else
                                                            'no' if x == 0 else 'NA')
    return data

# DATA EXECUTION

# still executes what's previous this block of code, but it will show only what's past the block
if __name__ == '__main__':

    # extract Data
    df_raw = get_data(r'C:\Users\andre\repos\python-zero-ao-ds\datasets\kc_house_data.csv')

    # prepare data
    df = data_preparing(df_raw)

    # Dashboard

    # attributes filters
    f_attributes = st.sidebar.multiselect('Select Columns', df.columns)
    f_zip = st.sidebar.multiselect('Select Zipcode', df['zipcode'].unique())

    # Overview Title
    st.title('1. House Rocket Data Overview')

    # Set the visualization according to the selected filter
    if (f_zip != []) and (f_attributes != []):
        df_ov = df.loc[df['zipcode'].isin(f_zip), f_attributes]

    elif (f_zip != []) and (f_attributes == []):
        df_ov = df.loc[df['zipcode'].isin(f_zip), :]

    elif (f_zip == []) and (f_attributes != []):
        df_ov = df.loc[:, f_attributes]

    else:
        df_ov = df.copy()

    # shows the dataframe resultant of filtering
    st.dataframe(df_ov, height=300)

    # set title of second block
    st.title('2. Average Metrics')

    # Making another check within the filters so attributes filter don't change the rest of code
    if f_zip != []:
        df = df.loc[df['zipcode'].isin(f_zip), :]

    else:
        df = df.copy()

    # set config to put tables side by side
    c1, c2 = st.columns((1, 1))

    # set title for first table
    c1.subheader('2.1 By zipcode')

    # count of properties by zipcode
    df1 = df[['zipcode', 'id']].groupby('zipcode').count().reset_index()
    # mean price by zipcode
    df2 = df[['zipcode', 'price']].groupby('zipcode').mean().reset_index()
    # mean living room area by zipcode
    df3 = df[['zipcode', 'sqft_living']].groupby('zipcode').mean().reset_index()
    # mean square meter price by zipcode
    df4 = df[['zipcode', 'm2_lot_price']].groupby('zipcode').mean().reset_index()

    # merging DataFrames
    m1 = pd.merge(df1, df2, on='zipcode', how='inner')
    m2 = pd.merge(m1, df3, on='zipcode', how='inner')
    zipcode_attributes = pd.merge(m2, df4, on='zipcode', how='inner').reset_index(drop=True)

    # rename average metrics dataframe
    zipcode_attributes.rename(columns={'id': 'properties',
                                       'price': 'mean_price',
                                       'sqft_living': 'mean_living_area',
                                       'm2_lot_price': 'mean_m2_price'}, inplace=True)

    # set average metrics dataframe in column one
    c1.dataframe(zipcode_attributes, height=400)

    c2.subheader('2.2 By attribute')

    # select only numeric attributes
    num_attributes = df.select_dtypes(include=['int64', 'float64'])
    # get descriptive data and transpose dataframe to better view
    des_attributes = num_attributes.describe().transpose()
    # drop columns that don't make sense
    des_attributes.drop(['id', 'yr_built', 'yr_renovated',
                         'lat', 'long', 'zipcode', 'view',
                         'condition', 'grade'], axis=0, inplace=True)

    # set average metrics attibute dataframe in column twow
    c2.dataframe(des_attributes, height=400)

    st.title('3. Region Overview')
    c1, c2 = st.columns((1, 1))

    # create basemap
    density_map = folium.Map(location=[df['lat'].mean(), df['long'].mean()],
                             default_zoom_start=15)

    # add marker clusters to a map using in-browser rendering.
    marker_cluster = MarkerCluster().add_to(density_map)

    # temporary
    # df = df.sample(100)

    # iterate over the whole DataFrame, parsing the data to plot the map
    for name, row in df.iterrows():
        folium.Marker([row['lat'], row['long']],
                      popup='Sold for ${0} on {1}'.format(row['price'],
                                                          row['date'])).add_to(marker_cluster)
    # sets map title
    st.subheader('3.1 Portfolio Density')

    # plots map
    folium_static(density_map)

    # sets map title
    st.subheader('3.2 Price Density')

    # collected needed data to plot price density
    price_density = df[['price', 'zipcode']].groupby('zipcode').mean().reset_index()

    # pushed geojson file from web
    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'

    # apply geofile function with the path we just declared
    geofile = get_geofile(url)

    # overwrite geofile with lat and long info
    geofile = geofile[geofile['ZIP'].isin(price_density['zipcode'].to_list())]

    # creating map object
    region_price_map = folium.Map(location=[df['lat'].mean(), df['long'].mean()],
                                  default_zoom_start=15)

    # coloring quantitative data with choropleth
    region_price_map.choropleth(
        data=price_density,
        geo_data=geofile,
        columns=['zipcode', 'price'],
        key_on='feature.properties.ZIP',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='AVG PRICE'
    )

    # plots map
    folium_static(region_price_map)

    # properties distribution by commercial category
    st.title('4. Commercial Attributes')

    st.subheader('4.1 Mean Price By Year of Construction')

    # set mean price by year built
    avg_yr_built = df[['yr_built', 'date', 'price']].groupby('yr_built').mean().reset_index()
    # plot line map and save it on a variable
    fig = px.line(avg_yr_built, x='yr_built', y='price')

    st.plotly_chart(fig, use_container_width=True)

    st.subheader('4.2 Mean Price By Date of Availability to Buy')

    # set mean price by date of availability to buy
    avg_date = df[['date', 'price']].groupby('date').mean().reset_index()
    # plot line map and save it on a variable
    fig = px.line(avg_date, x='date', y='price')

    st.plotly_chart(fig, use_container_width=True)

    # title of histogrqams section
    st.title('5. Distribution by Attributes')

    st.subheader('5.1 By Price ')

    hist_df = df.copy()

    fig = px.histogram(hist_df, x='price', nbins=15)
    st.plotly_chart(fig, use_container_width=300)

    st.subheader('5.2 By Number of Bedrooms')
    fig = px.histogram(hist_df, x='bedrooms', nbins=15)
    st.plotly_chart(fig, use_container_width=300)

    st.subheader('5.3 By Number of Bathrooms')
    fig = px.histogram(hist_df, x='bathrooms', nbins=15)
    st.plotly_chart(fig, use_container_width=300)

    st.subheader('5.4 By Number of Floors')
    fig = px.histogram(hist_df, x='floors', nbins=15)
    st.plotly_chart(fig, use_container_width=300)

    st.subheader('5.5 Waterview Distribution')
    fig = px.histogram(hist_df, x='waterfront', nbins=3)
    st.plotly_chart(fig, use_container_width=300)