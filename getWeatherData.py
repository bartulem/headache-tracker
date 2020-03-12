"""
This script acquires the weather data.
@author: bartulem
"""

import datetime
import pandas as pd
import urllib.request as request
import json


class weather:

    # Initializer / Instance Attributes
    def __init__(self, startdate, enddate):
        self.startdate = [int(sd) for sd in startdate.split('-')]
        self.enddate = [int(ed) for ed in enddate.split('-')]

    def get_weather_data(self, **kwargs):

        """
        Parameters
        ----------
        **kwargs: dictionary
        weatherVars : list
            The available or desired weather variables; defaults to ['Min_temperature', 'Max_temperature', 'Mean_temperature', 'Wind_meanSpeed', 'Wind_maxSpeed', 'Precipitation'].
        weatherWeb : str
            The json file site which contains the weather data; defaults to the Trondheim one.
        saveFile : str
            The path and name of the .csv file to save the data in; defaults to 'weatherData_2019-2020'.
        ----------
        """

        weatherVars = [kwargs['weatherVars'] if 'weatherVars' in kwargs.keys() and type(kwargs['weatherVars']) == list else ['Min_temperature', 'Max_temperature', 'Mean_temperature', 'Wind_meanSpeed', 'Wind_maxSpeed', 'Precipitation']][0]
        weatherWeb = [kwargs['weatherWeb'] if 'weatherWeb' in kwargs.keys() and type(kwargs['weatherWeb']) == str else 'https://www.yr.no/api/v0/locations/1-211102/observations/year'][0]
        saveFile = [kwargs['saveFile'] if 'saveFile' in kwargs.keys() and type(kwargs['saveFile']) == str else 'weatherData_2019-2020'][0]

        # get all the dates in the designated period
        dates = []
        start = datetime.datetime(self.startdate[2], self.startdate[0], self.startdate[1])
        end = datetime.datetime(self.enddate[2], self.enddate[0], self.enddate[1])
        delta = end - start
        for i in range(delta.days + 1):
            dates.append(str(start + datetime.timedelta(days=i))[:10])

        # create df to store the data
        weatherData = pd.DataFrame(index=dates, columns=weatherVars, dtype=float)

        # fetch the Tromdheim weather data from the web (need internet connection!)
        with request.urlopen(weatherWeb) as response:
            dataOnline = json.loads(response.read())
            # # # the following dict structure changed before, so inspect it if errors occur
            # iterate through the last 13 months & get temperature, wind and precipitation data
            for amonth in range(len(dataOnline['historical']['months'])):
                for aday in range(len(dataOnline['historical']['months'][amonth]['days'])):
                    specificDate = dataOnline['historical']['months'][amonth]['days'][aday]['time'][:10]
                    for avar in dataOnline['historical']['months'][amonth]['days'][aday].keys():
                        if(avar == 'temperature'):
                            for atempkey in dataOnline['historical']['months'][amonth]['days'][aday][avar].keys():
                                if(atempkey == 'min'):
                                    weatherData.loc[specificDate, 'Min_temperature'] = dataOnline['historical']['months'][amonth]['days'][aday][avar][atempkey]
                                elif(atempkey == 'max'):
                                    weatherData.loc[specificDate, 'Max_temperature'] = dataOnline['historical']['months'][amonth]['days'][aday][avar][atempkey]
                                elif(atempkey == 'mean'):
                                    weatherData.loc[specificDate, 'Mean_temperature'] = dataOnline['historical']['months'][amonth]['days'][aday][avar][atempkey]
                        elif(avar == 'wind'):
                            for awindkey in dataOnline['historical']['months'][amonth]['days'][aday][avar].keys():
                                if(awindkey == 'meanSpeed'):
                                    weatherData.loc[specificDate, 'Wind_meanSpeed'] = dataOnline['historical']['months'][amonth]['days'][aday][avar][awindkey]
                                elif(awindkey == 'maxSpeed'):
                                    weatherData.loc[specificDate, 'Wind_maxSpeed'] = dataOnline['historical']['months'][amonth]['days'][aday][avar][awindkey]
                        elif(avar == 'precipitation'):
                            weatherData.loc[specificDate, 'Precipitation'] = dataOnline['historical']['months'][amonth]['days'][aday][avar]['total']

        # save weather data to .csv file
        weatherData.to_csv('{}.csv'.format(saveFile), header=True, index=True, sep=';')


weatherClass = weather('1-1-2019', '2-28-2020')
weatherClass.get_weather_data()
