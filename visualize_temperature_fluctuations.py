"""
This script contains the function for visualizing temperature fluctuations.
@author: bartulem
"""

import json
import os
import matplotlib.pyplot as plt
import numpy as np
from helper_functions import get_cumulative_days_for_period, get_temperature
from pandas_loader import data_load

plt.style.use('./headache_tracker.mplstyle')


def temperature_oscillations(input_parameter_dict=None):
    """
    Parameters
    ----------
    input_parameter_dict : dict
        Contains the following set of parameters
            start_period : str
                The starting month-year of the analyzed period; defaults to '1-2021'.
            end_period : str
                The last month-year of the analyzed period; defaults to '12-2021'.
            save_fig : boolean
                To save or not to save; defaults to False.
            save_dir : str
                Directory to save the figure in.
            fig_format : str
                Format to save the figure in; defaults to 'png'.
            pos_temp_color : str
                Color for the positive temperatures; defaults to '#EE5C42'
            neg_temp_color : str
                Color for the negative temperatures; defaults to '#1E90FF'
            headache_color : str
                Color for the negative temperatures; defaults to '#2E2E2E'
    ----------
    """

    if input_parameter_dict is None:
        with open('input_parameters.json', 'r') as json_file:
            input_parameter_dict = json.load(json_file)

    # load the .csv file with the data
    data = data_load(file_loc=input_parameter_dict['pandas_loader']['data_load']['file_loc'],
                     file_separator=input_parameter_dict['pandas_loader']['data_load']['file_separator'],
                     der_variables=input_parameter_dict['pandas_loader']['data_load']['der_variables'])

    # get cumulated number of days in a given period (*end* includes that month as well!), the month IDs for plotting & start and end days
    months_cumulated, month_IDs, start_and_end_dates = \
        get_cumulative_days_for_period(start=input_parameter_dict['visualize_temperature_fluctuations']['temperature_oscillations']['start_period'],
                                       end=input_parameter_dict['visualize_temperature_fluctuations']['temperature_oscillations']['end_period'])

    # get centers of months in terms of cumulated days (important for plotting)
    month_centers = [(x + months_cumulated[xnd + 1]) / 2. for xnd, x in enumerate(months_cumulated) if xnd < len(months_cumulated) - 1]

    # convert date form into that found in CSV file
    start_date = [int(item) for item in start_and_end_dates[0].split('/')]
    end_date = [int(item) for item in start_and_end_dates[1].split('/')]
    start_row = data.index[(data['Year'] == start_date[2]) & (data['Month'] == start_date[0]) & (data['Day'] == start_date[1])].tolist()[0]
    end_row = data.index[(data['Year'] == end_date[2]) & (data['Month'] == end_date[0]) & (data['Day'] == end_date[1])].tolist()[0]

    # get all the variables for the designated period
    headaches = np.ravel(np.nonzero((np.array(data.iloc[start_row:end_row, data.columns.get_loc('Headache')]))))
    pos_ind, pos_temp, neg_ind, neg_temp = get_temperature(data.iloc[start_row:end_row, data.columns.get_loc('Mean_temp (°C)')])
    temp_min = np.array(data.iloc[start_row:end_row, data.columns.get_loc('Min_temp (°C)')])
    temp_max = np.array(data.iloc[start_row:end_row, data.columns.get_loc('Max_temp (°C)')])

    # plot the figures
    fig, ax = plt.subplots(1, 1, figsize=(20, 5))
    ax = plt.subplot(111)
    ax.plot(pos_ind, pos_temp, color=input_parameter_dict['visualize_temperature_fluctuations']['temperature_oscillations']['pos_temp_color'], lw=2)
    ax.plot(neg_ind, neg_temp, color=input_parameter_dict['visualize_temperature_fluctuations']['temperature_oscillations']['neg_temp_color'], lw=2)
    for one_month in months_cumulated:
        ax.axvline(one_month, color='#000000', lw=.25)
    for one_day_idx, oneday in enumerate(headaches):
        if one_day_idx == 0:
            ax.plot(oneday, data.iloc[start_row+oneday, data.columns.get_loc('Mean_temp (°C)')], 'o',
                    color=input_parameter_dict['visualize_temperature_fluctuations']['temperature_oscillations']['headache_color'], ms=5, label='Headache')
        else:
            ax.plot(oneday, data.iloc[start_row+oneday, data.columns.get_loc('Mean_temp (°C)')], 'o',
                    color=input_parameter_dict['visualize_temperature_fluctuations']['temperature_oscillations']['headache_color'], ms=5)
    for elem_idx, elem in enumerate(temp_min):
        if not np.isnan(elem) and not np.isnan(temp_max[elem_idx]):
            if elem >= 0 and temp_max[elem_idx] > 0:
                ax.bar(x=elem_idx, height=(temp_max[elem_idx] - elem), width=1, bottom=elem, align='center',
                       color=input_parameter_dict['visualize_temperature_fluctuations']['temperature_oscillations']['pos_temp_color'], alpha=.3)
            elif elem < 0 and temp_max[elem_idx] <= 0:
                ax.bar(x=elem_idx, height=(abs(elem) - abs(temp_max[elem_idx])), width=1, bottom=elem, align='center',
                       color=input_parameter_dict['visualize_temperature_fluctuations']['temperature_oscillations']['neg_temp_color'], alpha=.3)
            else:
                ax.bar(x=elem_idx, height=temp_max[elem_idx], width=1, bottom=0, align='center',
                       color=input_parameter_dict['visualize_temperature_fluctuations']['temperature_oscillations']['pos_temp_color'], alpha=.3)
                ax.bar(x=elem_idx, height=abs(elem), width=1, bottom=elem, align='center',
                       color=input_parameter_dict['visualize_temperature_fluctuations']['temperature_oscillations']['neg_temp_color'], alpha=.3)
    ax.set_title('Temperature oscillations and headaches {} to {}'.format(month_IDs[0], month_IDs[-1]), fontsize=20, pad=20)
    ax.legend(loc='upper left', prop={'size': 10})
    ax.set_xlim(0, len(temp_min))
    ax.set_xticks(month_centers)
    ax.set_xticklabels(month_IDs, fontsize=15)
    ax.set_xlabel('Month', fontsize=20)
    ax.set_yticks(np.arange(-15, 35, 5.))
    ax.set_yticklabels([int(num) for num in np.arange(-15, 35, 5.)], fontsize=10)
    ax.set_ylabel(u'Temperature (℃)', fontsize=15)
    ax.tick_params(axis='both', which='both', length=0)
    ax.text(315, 37, 'data source: OpenWeather', fontsize=10, fontweight='bold')

    plt.show()
    if input_parameter_dict['visualize_temperature_fluctuations']['temperature_oscillations']['save_fig']:
        fig.savefig(f"{input_parameter_dict['visualize_temperature_fluctuations']['temperature_oscillations']['save_dir']}{os.sep}temperature oscillations and headaches {month_IDs[0]} "
                    f"to {month_IDs[-1]}.{input_parameter_dict['visualize_temperature_fluctuations']['temperature_oscillations']['fig_format']}", bbox_inches='tight')
