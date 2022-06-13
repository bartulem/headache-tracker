"""
Loads CSV file as dataframe, and computes first & second derivatives for time series.
@author: bartulem
"""

import pandas as pd


def data_load(file_loc=None, file_separator=',',
              insert_derivatives=False, der_variables=None):
    """
    Parameters
    ----------
    file_loc : str
        Absolute location of the weather data CSV file; defaults to None.
    file_separator : str
        File delimiter of choice; defaults to ",".
    insert_derivatives : bool
        Yey or ney on the derivatives; defaults to False.
    der_variables : list
        Variables to calculate derivatives on; defaults to None.
    ----------

    Returns
    ----------
    augmented_csv_data : int64
        The loaded data with all the calculated derivatives.
    ----------
    """

    csv_data = pd.read_csv(filepath_or_buffer=file_loc, sep=file_separator)

    if insert_derivatives:
        if der_variables is None:
            der_variables = ['Min_temp (°C)', 'Max_temp (°C)',
                             'Mean_temp (°C)', 'Pressure (hPa)',
                             'Humidity (%)', 'Wind_speed (m/s)',
                             'Wind_deg (°)', 'Clouds (%)']

        first_der_names = [f'{var.split(" ")[0]}_1st_der' for var in der_variables]
        second_der_names = [f'{var.split(" ")[0]}_2nd_der' for var in der_variables]

        for idx, var in enumerate(der_variables):
            var_position = csv_data.columns.get_loc(var)
            csv_data.insert(loc=var_position+1,
                            column=first_der_names[idx],
                            value=csv_data.loc[:, var].diff())
            csv_data.insert(loc=var_position + 2,
                            column=second_der_names[idx],
                            value=csv_data.loc[:, first_der_names[idx]].diff())

    return csv_data
