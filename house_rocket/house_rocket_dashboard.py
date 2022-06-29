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
@st.cache(allow_output_mutation=True)
def convert_to_m2(data, col=None):
    """
    :param data: DataFrame or Series
    :param col: The Column of the DataFrame to be converted. If Series, no need to be declared
    :return: Series with converted values
    """
    m2 = round(data[col] * 0.092903, 2)

    return m2


def get_data(path):
    """
    :param path: Path of csv file to be read
    :return: DataFrame
    """
    data = pd.read_csv(path)

    return data


def get_geofile(path):
    """
    :param path: Path file that constains geo space information
    :return: DataFrame
    """
    geofile = geopandas.read_file(path)

    return geofile


def data_preparing(data):
    """
    :param data: DataFrame that will be changed
    :return: Changed DataFrame
    """
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


def data_overview(data):

    # Set the visualization according to the selected filter
    if (f_zip != []) and (f_attributes != []):
        data = data.loc[data['zipcode'].isin(f_zip), f_attributes]

    elif (f_zip != []) and (f_attributes == []):
        data = data.loc[data['zipcode'].isin(f_zip), :]

    elif (f_zip == []) and (f_attributes != []):
        data = data.loc[:, f_attributes]

    else:
        data = data.copy()

    return data


def average_metrics_zipcode(data):

    # Making another check within the filters so attributes filter don't change the rest of code
    if f_zip:
        data = data.loc[data['zipcode'].isin(f_zip), :]

    else:
        data = data.copy()

    # count of properties by zipcode
    df1 = data[['zipcode', 'id']].groupby('zipcode').count().reset_index()
    # mean price by zipcode
    df2 = data[['zipcode', 'price']].groupby('zipcode').mean().reset_index()
    # mean living room area by zipcode
    df3 = data[['zipcode', 'sqft_living']].groupby('zipcode').mean().reset_index()
    # mean square meter price by zipcode
    df4 = data[['zipcode', 'm2_lot_price']].groupby('zipcode').mean().reset_index()

    # merging DataFrames
    m1 = pd.merge(df1, df2, on='zipcode', how='inner')
    m2 = pd.merge(m1, df3, on='zipcode', how='inner')
    data = pd.merge(m2, df4, on='zipcode', how='inner').reset_index(drop=True)

    # rename average metrics dataframe
    data.rename(columns={'id': 'properties',
                         'price': 'mean_price',
                         'sqft_living': 'mean_living_area',
                         'm2_lot_price': 'mean_m2_price'}, inplace=True)

    return data


def average_metrics_attribute(data):

    # Making another check within the filters so attributes filter don't change the rest of code
    if f_zip:
        data = data.loc[data['zipcode'].isin(f_zip), :]

    else:
        data = data.copy()

    # select only numeric attributes
    num_attributes = data.select_dtypes(include=['int64', 'float64'])
    # get descriptive data and transpose dataframe to better view
    des_attributes = num_attributes.describe().transpose()
    # drop columns that don't make sense
    des_attributes.drop(['id', 'yr_built', 'yr_renovated',
                         'lat', 'long', 'zipcode', 'view',
                         'condition', 'grade'], axis=0, inplace=True)

    return des_attributes


def properties_density(data):
    # create basemap
    density_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()],
                             default_zoom_start=15)

    # add marker clusters to a map using in-browser rendering.
    marker_cluster = MarkerCluster().add_to(density_map)

    # iterate over the whole DataFrame, parsing the data to plot the map
    for name, row in data.iterrows():
        folium.Marker([row['lat'], row['long']],
                      popup='Sold for ${0} on {1}'.format(row['price'],
                                                          row['date'])).add_to(marker_cluster)

    folium_static(density_map)

    return None


def price_density(data):

    # collected needed data to plot price density
    pricedensity = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()

    # pushed geojson file from web
    path = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'

    # apply geofile function with the path we just declared
    file = get_geofile(path)

    # overwrite geofile with lat and long info
    geofile = file[file['ZIP'].isin(pricedensity['zipcode'].to_list())]

    # creating map object
    region_price_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()],
                                  default_zoom_start=15)

    # coloring quantitative data with choropleth
    region_price_map.choropleth(
        data=pricedensity,
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

    return None


def avg_price_yr_built(data):
    # set mean price by year built
    avg_yr_built = data[['yr_built', 'date', 'price']].groupby('yr_built').mean().reset_index()
    fig = px.line(avg_yr_built, x='yr_built', y='price')
    st.plotly_chart(fig, use_container_width=True)

    return None


def avg_price_date(data):
    # set mean price by date of availability to buy
    avg_date = data[['date', 'price']].groupby('date').mean().reset_index()
    fig = px.line(avg_date, x='date', y='price')
    st.plotly_chart(fig, use_container_width=True)

    return None


def histogram(data: object, col: object, bins: object) -> object:
    """
    :param data: DataFrame or Series
    :param col: Which column will be ploted
    :param bins: The number of intervals on histogram
    :return:
    """
    fig = px.histogram(data, x=col, nbins=bins)
    st.plotly_chart(fig, use_container_width=300)

    return None


# Indicates main function of the script
if __name__ == '__main__':

    # extraction
    df_raw = get_data('house_rocket/kc_house_data.csv')

    # transformation
    df = data_preparing(df_raw)

    # DASHBOARD CONSTRUCTION

    # filters
    f_zip = st.sidebar.multiselect('Select Zipcode', df['zipcode'].unique())
    f_attributes = st.sidebar.multiselect('Select Columns', df.columns)

    # overview title
    st.title('1. House Rocket Data Overview')
    fig1 = data_overview(df)
    st.dataframe(fig1, height=300)

    # avg metrics title
    st.title('2. Average Metrics')

    # set config to put tables side by side
    c1, c2 = st.columns((1, 1))

    # set subtitle title
    c1.subheader('2.1 By zipcode')
    c2.subheader('2.2 By attribute')

    # execute functions
    fig2 = average_metrics_zipcode(df)
    fig3 = average_metrics_attribute(df)

    # set average metrics dataframe by zipcode
    c1.dataframe(fig2, height=400)
    c2.dataframe(fig3, height=400)

    # section three title
    st.title('3. Region Overview')

    st.subheader('3.1 Portfolio Density')
    properties_density(df)

    st.subheader('3.2 Price Density')
    price_density(df)

    # section four title
    st.title('4. Commercial Attributes')

    st.subheader('4.1 Mean Price By Year of Construction')
    avg_price_yr_built(df)
    st.subheader('4.2 Mean Price By Date of Availability to Buy')
    avg_price_date(df)

    # section five title
    st.title('5. Distribution by Attributes')

    st.subheader('5.1 By Price ')
    histogram(df, 'price', 20)

    st.subheader('5.2 By Number of Bedrooms')
    histogram(df, 'bedrooms', 20)

    st.subheader('5.3 By Number of Bathrooms')
    histogram(df, 'bathrooms', 20)

    st.subheader('5.4 By Number of Floors')
    histogram(df, 'floors', 20)

    st.subheader('5.5 Waterview Distribution')
    histogram(df, 'waterfront', 2)
