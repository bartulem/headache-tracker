"""
This script enables the visualization of the weather & pain data.
@author: bartulem
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import calendar


def get_cumulative_days_for_period(**kwargs):
    """
    Parameters
    ----------
    **kwargs: dictionary
    start : str
        The start of the desired period; defaults to '1-2019'.
    end : str
        The end of the desired period; defaults to '12-2019'.
    ----------
    """

    start = [int(e) for e in [kwargs['start'] if 'start' in kwargs.keys() and type(kwargs['start']) == str else '1-2019'][0].split('-')]
    end = [int(e) for e in [kwargs['end'] if 'end' in kwargs.keys() and type(kwargs['end']) == str else '12-2019'][0].split('-')]

    # convert the start and end into specific dates that are indices in the df
    startandenddates = ['{}/{}/{}'.format(start[0], 1, start[1]), '{}/{}/{}'.format(end[0], calendar.monthrange(end[1], end[0])[1], end[1])]

    daysCumulative = []
    monthIDs = []
    if (start[1] != end[1]):
        # condition where the period starts in one year, but ends in another
        for amonth in range(start[0], 13):
            numofdays = calendar.monthrange(start[1], amonth)[1]
            monthIDs.append('{}-{}'.format(calendar.month_abbr[amonth], str(start[1])[-2:]))
            if (len(daysCumulative) == 0):
                daysCumulative.append(numofdays)
            else:
                daysCumulative.append(numofdays + daysCumulative[-1])
        for amonth in range(1, end[0] + 1):
            monthIDs.append('{}-{}'.format(calendar.month_abbr[amonth], str(end[1])[-2:]))
            numofdays = calendar.monthrange(end[1], amonth)[1]
            daysCumulative.append(numofdays + daysCumulative[-1])
    else:
        # condition when the start & end months belong to the same year
        for amonth in range(start[0], end[0] + 1):
            numofdays = calendar.monthrange(start[1], amonth)[1]
            monthIDs.append('{}-{}'.format(calendar.month_abbr[amonth], str(start[1])[-2:]))
            if (len(daysCumulative) == 0):
                daysCumulative.append(numofdays)
            else:
                daysCumulative.append(numofdays + daysCumulative[-1])

    return [0] + daysCumulative, monthIDs, startandenddates


def correct_edge_NANs(arrayToCorrect, fullArray):
    xplotIndices = np.arange(0, len(arrayToCorrect), 1.)
    nonNaNindices = [i for i in range(len(arrayToCorrect)) if i not in np.ravel(np.argwhere(np.isnan(arrayToCorrect)))]
    for aindx in nonNaNindices:
        if(aindx == 0):
            if(1 not in nonNaNindices):
                arrayToCorrect[1] = 0
                xplotIndices[1] = (aindx+1)-(abs(fullArray[aindx+1])/(abs(fullArray[aindx])+abs(fullArray[aindx+1])))
        elif(aindx == len(arrayToCorrect)-1):
            if(len(arrayToCorrect)-2 not in nonNaNindices):
                arrayToCorrect[len(arrayToCorrect)-2] = 0
                xplotIndices[len(arrayToCorrect)-2] = aindx-(abs(fullArray[aindx])/(abs(fullArray[aindx-1])+abs(fullArray[aindx])))
        else:
            if((aindx-1 not in nonNaNindices) and (aindx+1 not in nonNaNindices)):
                arrayToCorrect[aindx-1] = 0
                xplotIndices[aindx-1] = aindx-(abs(fullArray[aindx])/(abs(fullArray[aindx-1])+abs(fullArray[aindx])))
                arrayToCorrect[aindx+1] = 0
                xplotIndices[aindx+1] = (aindx+1)-(abs(fullArray[aindx+1])/(abs(fullArray[aindx])+abs(fullArray[aindx+1])))
            else:
                if(aindx-1 not in nonNaNindices):
                    arrayToCorrect[aindx-1] = 0
                    xplotIndices[aindx-1] = aindx-(abs(fullArray[aindx])/(abs(fullArray[aindx-1])+abs(fullArray[aindx])))
                elif(aindx+1 not in nonNaNindices):
                    arrayToCorrect[aindx+1] = 0
                    xplotIndices[aindx+1] = (aindx+1)-(abs(fullArray[aindx+1])/(abs(fullArray[aindx])+abs(fullArray[aindx+1])))
                else:
                    continue

    counter = 0
    problematicIndices = []
    for index, item in enumerate(arrayToCorrect):
        if(index <= len(arrayToCorrect)-2):
            if((item == 0) and (arrayToCorrect[index-1] != 0 and not np.isnan(arrayToCorrect[index-1])) and (arrayToCorrect[index+1]) != 0 and not np.isnan(arrayToCorrect[index+1])):
                counter += 1
                problematicIndices.append(index)
    # print(xplotIndices, arrayToCorrect, problematicIndices)
    if(counter > 0):
        arrayToCorrect = list(arrayToCorrect)
        xplotIndices = list(xplotIndices)
        count = 0
        for anindex in problematicIndices:
            arrayToCorrect.insert(anindex+count, 0)
            xplotIndices.insert(anindex+count, anindex-(abs(fullArray[anindex])/(abs(fullArray[anindex-1])+abs(fullArray[anindex]))))
            arrayToCorrect.insert(anindex+1+count, np.nan)
            xplotIndices.insert(anindex+1+count, np.nan)
            count += 2

        counter2 = 0
        problematicIndices2 = []
        for index2, item2 in enumerate(arrayToCorrect):
            if(index2 <= len(arrayToCorrect)-2):
                if((item2 == 0 and arrayToCorrect[index2+1] == 0) or (item2 == 0 and arrayToCorrect[index2-1] != 0 and not np.isnan(arrayToCorrect[index2-1]) and arrayToCorrect[index2+1] != 0 and not np.isnan(arrayToCorrect[index2+1]))):
                    counter2 += 1
                    problematicIndices2.append(index2)
        # print(xplotIndices, arrayToCorrect, problematicIndices)

        if(counter2 > 0):
            count2 = 0
            for anindex2 in problematicIndices2:
                arrayToCorrect.insert(anindex2+1+count2, np.nan)
                xplotIndices.insert(anindex2+1+count2, np.nan)
                count2 += 1

        arrayToCorrect = np.array(arrayToCorrect)
        xplotIndices = np.array(xplotIndices)
    # print(xplotIndices, arrayToCorrect)

    return xplotIndices, arrayToCorrect


def get_POS_and_NEG_temps(dfSeries):
    theArray = np.array(dfSeries.copy())
    plus_temp = dfSeries.copy()
    minus_temp = dfSeries.copy()
    plus_temp[plus_temp <= 0] = np.nan
    minus_temp[minus_temp > 0] = np.nan
    indices_plus, revised_plus = correct_edge_NANs(np.array(plus_temp), theArray)
    indices_minus, revised_minus = correct_edge_NANs(np.array(minus_temp), theArray)
    return indices_plus, revised_plus, indices_minus, revised_minus


class pain:
    """
    After the getWeatherData script gathers the weather data, I merged it with the information from the iMigraine ap, which included:
    Headache: 0 - None, 1 - Happened
    Severity: 0 - None, 1 - Low, 2 - Mild, 3 - Medium, 4 - High, 5 - Severe
    Medication: 0, 1, 2, etc. (number of painkillers taken)
    Relief: 0 - Not applicable, 1 - No relief, 2 - Little, 3 - Mild, 4 - Almost, 5 - Complete
    """

    # Initializer / Instance Attributes
    def __init__(self, csvfile):
        # check that the file is there
        if (not os.path.isfile(csvfile)):
            print('Could not find file {}, try again.'.format(csvfile))
            sys.exit()

        self.csvfile = csvfile

    def visualize_data(self, **kwargs):
        """
        Parameters
        ----------
        **kwargs: dictionary
        startperiod : str
            The starting month-year of the analyzed period; defaults to '1-2019'.
        endperiod : str
            The last month-year of the analyzed period; defaults to '12-2019'.
        savePlot : boolean (0/False or 1/True)
            To save or not to save; defaults to False.
        figFormat : str
            Format to save the figure in; defaults to 'png'.
        resolution : int / float
            Image resolution in dpi; defaults to 300.
        ----------
        """

        # valid values for Booleans
        validBools = [0, False, 1, True]

        startperiod = [kwargs['startperiod'] if 'startperiod' in kwargs.keys() and type(kwargs['startperiod']) == str else '1-2019'][0]
        endperiod = [kwargs['endperiod'] if 'endperiod' in kwargs.keys() and type(kwargs['endperiod']) == str else '12-2019'][0]
        savePlot = [kwargs['savePlot'] if 'savePlot' in kwargs.keys() and kwargs['savePlot'] in validBools else 0][0]
        figFormat = [kwargs['figFormat'] if 'figFormat' in kwargs.keys() and type(kwargs['figFormat']) == str else 'png'][0]
        resolution = [kwargs['resolution'] if 'resolution' in kwargs.keys() and type(kwargs['resolution']) == int else 300][0]

        # load the .csv file with the data
        data = pd.read_csv(self.csvfile, index_col=0, sep=',')

        # get cumulated number of days in a given period (*end* includes that month as well!), the month IDs for plotting & start and end days
        monthsCumulated, monthIDs, startandenddates = get_cumulative_days_for_period(start=startperiod, end=endperiod)

        # get centers of months in terms of cumulated days (important for plotting)
        monthCenters = [(x + monthsCumulated[xnd + 1]) / 2. for xnd, x in enumerate(monthsCumulated) if xnd < len(monthsCumulated) - 1]

        # get all the variables for the designated period
        headaches = np.ravel(np.nonzero((np.array(data.loc[startandenddates[0]:startandenddates[1], 'Headache']))))
        pos_ind, pos_temp, neg_ind, neg_temp = get_POS_and_NEG_temps(data.loc[startandenddates[0]:startandenddates[1], 'Mean_temperature'])
        tempMins = np.array(data.loc[startandenddates[0]:startandenddates[1], 'Min_temperature'])
        tempMaxs = np.array(data.loc[startandenddates[0]:startandenddates[1], 'Max_temperature'])
        windMean = np.array(data.loc[startandenddates[0]:startandenddates[1], 'Wind_meanSpeed'])
        windMax = np.array(data.loc[startandenddates[0]:startandenddates[1], 'Wind_maxSpeed'])
        precipitation = np.array(data.loc[startandenddates[0]:startandenddates[1], 'Precipitation'])

        # plot the figures
        fig, ax = plt.subplots(3, 1, figsize=(40, 30))
        ax = plt.subplot(311)
        ax.plot(pos_ind, pos_temp, color='#EE5C42', lw=2)
        ax.plot(neg_ind, neg_temp, color='#1E90FF', lw=2)
        for onemonth in monthsCumulated:
            ax.axvline(onemonth, color='#000000', lw=.25)
        for onedayindx, oneday in enumerate(headaches):
            if(onedayindx == 0):
                ax.plot(oneday, data.iloc[oneday, 2], 'o', color='#008B00', ms=10, label='Headache')
            else:
                ax.plot(oneday, data.iloc[oneday, 2], 'o', color='#008B00', ms=10)
        for eind, elem in enumerate(tempMins):
            if(not np.isnan(elem) and not np.isnan(tempMaxs[eind])):
                if(elem >= 0 and tempMaxs[eind] > 0):
                    ax.bar(x=eind, height=(tempMaxs[eind]-elem), width=1, bottom=elem, align='center', color='#EE5C42', alpha=.2)
                elif(elem < 0 and tempMaxs[eind] <= 0):
                    ax.bar(x=eind, height=(abs(elem)-abs(tempMaxs[eind])), width=1, bottom=elem, align='center', color='#1E90FF', alpha=.2)
                else:
                    ax.bar(x=eind, height=tempMaxs[eind], width=1, bottom=0, align='center', color='#EE5C42', alpha=.2)
                    ax.bar(x=eind, height=abs(elem), width=1, bottom=elem, align='center', color='#1E90FF', alpha=.2)
        ax.set_title('Weather-related headaches {} to {}'.format(monthIDs[0], monthIDs[-1]), fontsize=30, pad=20)
        ax.legend(loc='upper left', prop={'size': 15})
        ax.set_xlim(0, len(tempMins))
        ax.set_xticks(monthCenters)
        ax.set_xticklabels(monthIDs, fontsize=20)
        ax.set_yticks(np.arange(-15, 35, 5.))
        ax.set_yticklabels([int(num) for num in np.arange(-15, 35, 5.)], fontsize=20)
        ax.set_ylabel(u'Temperature (℃)', fontsize=25)
        ax.tick_params(axis='both', which='both', length=0)
        ax.text(310, 35, 'data source: yr.no', fontsize=15, fontweight='bold')

        ax2 = plt.subplot(312)
        ax2.plot(range(len(windMean)), windMean, color='#EEDC82', lw=3, label='Mean speed')
        ax2.plot(range(len(windMax)), windMax, color='#8B814C', lw=3, label='Max speed')
        for onemonth in monthsCumulated:
            ax2.axvline(onemonth, color='#000000', lw=.25)
        for onedayindx, oneday in enumerate(headaches):
            if(onedayindx == 0):
                ax2.plot(oneday, data.iloc[oneday, 3], 'o', color='#008B00', ms=10, label='Headache')
            else:
                ax2.plot(oneday, data.iloc[oneday, 3], 'o', color='#008B00', ms=10, )
        ax2.legend(loc='upper left', prop={'size': 15})
        ax2.set_xlim(0, len(windMax))
        ax2.set_xticks(monthCenters)
        ax2.set_xticklabels(monthIDs, fontsize=20)
        ax2.set_yticks(np.arange(0, 15, 2))
        ax2.set_yticklabels([int(num) for num in np.arange(0, 15, 2)], fontsize=20)
        ax2.set_ylabel('Wind speed (m/s)', fontsize=25)
        ax2.tick_params(axis='both', which='both', length=0)

        ax3 = plt.subplot(313)
        ax3.plot(range(len(precipitation)), precipitation, color='#104E8B', lw=3)
        for onemonth in monthsCumulated:
            ax3.axvline(onemonth, color='#000000', lw=.25)
        for onedayindx, oneday in enumerate(headaches):
            if(onedayindx == 0):
                ax3.plot(oneday, data.iloc[oneday, 5], 'o', color='#008B00', ms=10, label='Headache')
            else:
                ax3.plot(oneday, data.iloc[oneday, 5], 'o', color='#008B00', ms=10, )
        ax3.legend(loc='upper left', prop={'size': 15})
        ax3.set_xlim(0, len(precipitation))
        ax3.set_xticks(monthCenters)
        ax3.set_xticklabels(monthIDs, fontsize=20)
        ax3.set_ylim(0)
        ax3.set_yticks(np.arange(0, 40, 5))
        ax3.set_yticklabels([int(num) for num in np.arange(0, 40, 5)], fontsize=20)
        ax3.set_ylabel('Precipitation (mm)', fontsize=25)
        ax3.tick_params(axis='both', which='both', length=0)

        plt.show()
        if(savePlot):
            fig.savefig('Weather-related headaches {} to {}.{}'.format(monthIDs[0], monthIDs[-1], figFormat), bbox_inches='tight', dpi=resolution)


thecsvfile = '/home/bartulm/Insync/mimica.bartul@gmail.com/OneDrive/Work/Coding/Headache/weatherData_2019-2020.csv'
painClass = pain(thecsvfile)
painClass.visualize_data(startperiod='1-2019', endperiod='12-2019', savePlot=0)
