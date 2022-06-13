"""
This script contains several helper functions for visualizing temperature data.
@author: bartulem
"""

import numpy as np
import calendar


def get_cumulative_days_for_period(start='1-2019', end='12-2019'):
    """
    Parameters
    ----------
    start : str
        The start of the desired period; defaults to '1-2019'.
    end : str
        The end of the desired period; defaults to '12-2019'.
    ----------
    """

    start = [int(e) for e in start.split('-')]
    end = [int(e) for e in end.split('-')]

    # convert the start and end into specific dates that are indices in the df
    start_and_end_dates = ['{}/{}/{}'.format(start[0], 1, start[1]), '{}/{}/{}'.format(end[0], calendar.monthrange(end[1], end[0])[1], end[1])]

    days_cumulative = [0]
    month_ID = []
    if start[1] != end[1]:
        month_range = range(start[0], 13)
    else:
        month_range = range(start[0], end[0] + 1)

    for one_month in month_range:
        num_of_days = calendar.monthrange(start[1], one_month)[1]
        month_ID.append('{}-{}'.format(calendar.month_abbr[one_month], str(start[1])[-2:]))
        if len(days_cumulative) == 0:
            days_cumulative.append(num_of_days)
        else:
            days_cumulative.append(num_of_days + days_cumulative[-1])

    if start[1] != end[1]:
        # condition where the period starts in one year, but ends in another
        for one_month in range(1, end[0] + 1):
            month_ID.append('{}-{}'.format(calendar.month_abbr[one_month], str(end[1])[-2:]))
            num_of_days = calendar.monthrange(end[1], one_month)[1]
            days_cumulative.append(num_of_days + days_cumulative[-1])

    return days_cumulative, month_ID, start_and_end_dates


def correct_edge_nan(array_to_correct, full_array):
    x_indices = np.arange(0, len(array_to_correct), 1.)
    non_nan_indices = [i for i in range(len(array_to_correct)) if i not in np.ravel(np.argwhere(np.isnan(array_to_correct)))]
    for one_idx in non_nan_indices:
        if one_idx == 0:
            if 1 not in non_nan_indices:
                array_to_correct[1] = 0
                x_indices[1] = (one_idx+1)-(abs(full_array[one_idx + 1]) / (abs(full_array[one_idx]) + abs(full_array[one_idx + 1])))
        elif one_idx == len(array_to_correct) - 1:
            if len(array_to_correct)-2 not in non_nan_indices:
                array_to_correct[len(array_to_correct) - 2] = 0
                x_indices[len(array_to_correct) - 2] = one_idx - (abs(full_array[one_idx]) / (abs(full_array[one_idx - 1]) + abs(full_array[one_idx])))
        else:
            if (one_idx - 1 not in non_nan_indices) and (one_idx + 1 not in non_nan_indices):
                array_to_correct[one_idx - 1] = 0
                x_indices[one_idx-1] = one_idx-(abs(full_array[one_idx]) / (abs(full_array[one_idx - 1]) + abs(full_array[one_idx])))
                array_to_correct[one_idx + 1] = 0
                x_indices[one_idx+1] = (one_idx+1)-(abs(full_array[one_idx + 1]) / (abs(full_array[one_idx]) + abs(full_array[one_idx + 1])))
            else:
                if one_idx-1 not in non_nan_indices:
                    array_to_correct[one_idx - 1] = 0
                    x_indices[one_idx-1] = one_idx-(abs(full_array[one_idx]) / (abs(full_array[one_idx - 1]) + abs(full_array[one_idx])))
                elif one_idx+1 not in non_nan_indices:
                    array_to_correct[one_idx + 1] = 0
                    x_indices[one_idx+1] = (one_idx+1)-(abs(full_array[one_idx + 1]) / (abs(full_array[one_idx]) + abs(full_array[one_idx + 1])))
                else:
                    continue

    counter = 0
    problematic_indices = []
    for index, item in enumerate(array_to_correct):
        if index <= len(array_to_correct)-2:
            if (item == 0) and (array_to_correct[index - 1] != 0
                                and not np.isnan(array_to_correct[index - 1])) \
                    and (array_to_correct[index + 1]) != 0 \
                    and not np.isnan(array_to_correct[index + 1]):
                counter += 1
                problematic_indices.append(index)

    if counter > 0:
        array_to_correct = list(array_to_correct)
        x_indices = list(x_indices)
        count = 0
        for an_index in problematic_indices:
            array_to_correct.insert(an_index + count, 0)
            x_indices.insert(an_index + count, an_index - (abs(full_array[an_index]) / (abs(full_array[an_index - 1]) + abs(full_array[an_index]))))
            array_to_correct.insert(an_index + 1 + count, np.nan)
            x_indices.insert(an_index+1+count, np.nan)
            count += 2

        counter2 = 0
        problematicIndices2 = []
        for index2, item2 in enumerate(array_to_correct):
            if index2 <= len(array_to_correct)-2:
                if (item2 == 0 and array_to_correct[index2 + 1] == 0) \
                        or (item2 == 0 and array_to_correct[index2 - 1] != 0
                            and not np.isnan(array_to_correct[index2 - 1])
                            and array_to_correct[index2 + 1] != 0
                            and not np.isnan(array_to_correct[index2 + 1])):
                    counter2 += 1
                    problematicIndices2.append(index2)

        if counter2 > 0:
            count2 = 0
            for an_index_2 in problematicIndices2:
                array_to_correct.insert(an_index_2 + 1 + count2, np.nan)
                x_indices.insert(an_index_2+1+count2, np.nan)
                count2 += 1

        array_to_correct = np.array(array_to_correct)
        x_indices = np.array(x_indices)

    return x_indices, array_to_correct


def get_temperature(df_series):
    the_array = np.array(df_series.copy())
    plus_temp = df_series.copy()
    minus_temp = df_series.copy()
    plus_temp[plus_temp <= 0] = np.nan
    minus_temp[minus_temp > 0] = np.nan
    indices_plus, revised_plus = correct_edge_nan(np.array(plus_temp), the_array)
    indices_minus, revised_minus = correct_edge_nan(np.array(minus_temp), the_array)
    return indices_plus, revised_plus, indices_minus, revised_minus
