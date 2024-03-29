"""
This function is used to acquire daily weather data.
@author: bartulem
"""

import configparser
import datetime
import json
import pandas as pd
import requests


def get_daily_weather_data():

    # locate yourself on earth
    config = configparser.ConfigParser()
    config.read('.../config.ini')
    location_api_key = config['ipstack']['api']
    ipstack_url = f'http://api.ipstack.com/check?access_key={location_api_key}'
    geo_req = requests.get(ipstack_url)
    geo_json = json.loads(geo_req.text)
    if True:
        current_location = geo_json['location']['geoname_id']
        current_city = geo_json['city']
    # else:
    #     current_location = '5391959'  # '5102922' '5134086' '5085222' '5090189' '5102922' '3190261'
    #     current_city = 'San Francisco'  # 'Princeton' 'Rochester' 'Danbury' 'New London' 'Princeton' 'Split'

    current_latitude = geo_json['latitude']
    current_longitude = geo_json['longitude']

    # get weather data
    config_2 = configparser.ConfigParser()
    config_2.read('.../config.ini')
    owm_api_key = config_2['openweathermap']['api']
    owm_url = f'https://api.openweathermap.org/data/2.5/weather?id={current_location}&units=metric&appid={owm_api_key}'
    daily_weather_data = requests.get(owm_url).json()
    current_country = daily_weather_data['sys']['country']

    # get time
    now = datetime.datetime.now()
    print(f"It is {now.day:02d}.{now.month:02d}.{now.year} at {now.hour:02d}:{now.minute:02d} and you find yourself in {current_city}, "
          f"{current_country} (lat: {current_latitude}, lon: {current_longitude}).")

    # fil in dataframe with new data
    headache_csv = '.../daily_weather_data.csv'
    csv_df = pd.read_csv(headache_csv)
    new_row = csv_df.shape[0]
    csv_df.loc[new_row, 'Year'] = now.year
    csv_df.loc[new_row, 'Month'] = now.month
    csv_df.loc[new_row, 'Day'] = now.day
    csv_df.loc[new_row, 'Hour'] = now.hour
    csv_df.loc[new_row, 'Minute'] = now.minute

    if 'name' in daily_weather_data.keys():
        csv_df.loc[new_row, 'Location'] = daily_weather_data['name']
    if 'id' in daily_weather_data.keys():
        csv_df.loc[new_row, 'Location_ID'] = daily_weather_data['id']
    if 'country' in daily_weather_data['sys'].keys():
        csv_df.loc[new_row, 'Country'] = daily_weather_data['sys']['country']
    if 'lat' in daily_weather_data['coord'].keys():
        csv_df.loc[new_row, 'Latitude (°)'] = daily_weather_data['coord']['lat']
    if 'lon' in daily_weather_data['coord'].keys():
        csv_df.loc[new_row, 'Longitude (°)'] = daily_weather_data['coord']['lon']
    if 'temp_min' in daily_weather_data['main'].keys():
        csv_df.loc[new_row, 'Min_temp (°C)'] = daily_weather_data['main']['temp_min']
    if 'temp_max' in daily_weather_data['main'].keys():
        csv_df.loc[new_row, 'Max_temp (°C)'] = daily_weather_data['main']['temp_max']
    if 'temp' in daily_weather_data['main'].keys():
        csv_df.loc[new_row, 'Mean_temp (°C)'] = daily_weather_data['main']['temp']
    if 'feels_like' in daily_weather_data['main'].keys():
        csv_df.loc[new_row, 'Feel_temp (°C)'] = daily_weather_data['main']['feels_like']
    if 'pressure' in daily_weather_data['main'].keys():
        csv_df.loc[new_row, 'Pressure (hPa)'] = daily_weather_data['main']['pressure']
    if 'humidity' in daily_weather_data['main'].keys():
        csv_df.loc[new_row, 'Humidity (%)'] = daily_weather_data['main']['humidity']
    if 'visibility' in daily_weather_data.keys():
        csv_df.loc[new_row, 'Visibility (m)'] = daily_weather_data['visibility']
    if 'speed' in daily_weather_data['wind'].keys():
        csv_df.loc[new_row, 'Wind_speed (m/s)'] = daily_weather_data['wind']['speed']
    if 'deg' in daily_weather_data['wind'].keys():
        csv_df.loc[new_row, 'Wind_deg (°)'] = daily_weather_data['wind']['deg']
    if 'gust' in daily_weather_data['wind'].keys():
        csv_df.loc[new_row, 'Wind_gust (m/s)'] = daily_weather_data['wind']['gust']
    if 'all' in daily_weather_data['clouds'].keys():
        csv_df.loc[new_row, 'Clouds (%)'] = daily_weather_data['clouds']['all']

    # save data to file
    csv_df.to_csv(path_or_buf=headache_csv, index=False)


get_daily_weather_data()
