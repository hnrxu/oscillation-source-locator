import io
import numpy as np
import pandas as pd

from exceptions import ValidationError


def write_excel(times, magnitudes_v, angles_v, magnitudes_i, angles_i):
    #using temp var names, prob change later
    df = pd.DataFrame({
        'Time': times,
        'MVa': magnitudes_v,
        'MIa': magnitudes_i,
        'AVa': np.degrees(angles_v),
        'AIa': np.degrees(angles_i)
    })

    df.to_excel('test_input.xlsx', index=False)

def write_excel_power(s1, p1, sih1, pih1, sih2, pih2):
    #using temp var names, prob change later
    df = pd.DataFrame({
        'S1': s1,
        'Sih1': sih1,
        'Sih2': sih2,
        'P1': p1,
        'Pih1': pih1,
        'Pih2': pih2,
    })

    df.to_excel('power_output.xlsx', index=False)


# def read_excel(file_name):
#     #using temp var names, prob change later
#     df = pd.read_excel(file_name)
#     #drop nan rows
#     df = df.dropna()
#     magnitudes_v = df['MVa'].to_numpy()
#     magnitudes_i = df['MIa'].to_numpy()
#     angles_v = np.radians(df['AVa'].to_numpy())
#     angles_i = np.radians(df['AIa'].to_numpy())
#     times = df['Time'].to_numpy()
#     return magnitudes_v, magnitudes_i, angles_v, angles_i, times



def read_locations(df):

    locations = df.iloc[0]
    locations = locations.dropna().unique()
    locations = [l for l in locations if l != 'Time']  
    return locations

def read_excel(df, start, t_start = 0, t_end = None):

    df_data = df.iloc[4:]
    df_data = df_data.dropna()
    
    # get correct block of time
    times = df_data.iloc[:, 0].astype(float).to_numpy()
    t_start_idx = np.argmin(np.abs(times - t_start))
    if t_end is not None:
        t_end_idx = np.argmin(np.abs(times - t_end))
        times = times[t_start_idx:t_end_idx+1]
        data = df_data.iloc[t_start_idx:t_end_idx+1, start:start+5]
    else:
        times = times[t_start_idx:]
        data = df_data.iloc[t_start_idx:, start:start+5]


    f1_col = data.iloc[:, 0].astype(float).to_numpy()
    magnitudes_v = data.iloc[:, 1].astype(float).to_numpy()
    angles_v = data.iloc[:, 2].astype(float).to_numpy()
    magnitudes_i = data.iloc[:, 3].astype(float).to_numpy()
    angles_i = data.iloc[:, 4].astype(float).to_numpy()
    if len(f1_col) == 0 or len(magnitudes_v) == 0 or len(angles_v) == 0 or len(magnitudes_i) == 0 or len(angles_i) == 0:
        raise ValidationError("No valid rows after cleaning data. Please check that data has no extra columns/unusual structure.")
    
    return f1_col, magnitudes_v, magnitudes_i, angles_v, angles_i, times

def write_output_excel(output_dict, filename):
    columns = []
    data_columns = []
    for location, data_dict in output_dict.items():
        for key, values in data_dict.items():
            columns.append((location, key))
            data_columns.append(values)

    header = pd.MultiIndex.from_tuples(columns, names=['Location', 'Signal'])
    df = pd.DataFrame(np.array(data_columns).T, columns=header)
    df.to_excel(filename, index=True)


def validate_structure(df):
    if df.shape[0] < 5:
        raise ValidationError("File has too few rows.")
    if df.shape[1] < 6:
        raise ValidationError("File has too few columns.")
    
    # verify column 0 is Time column
    time_header = df.iloc[0, 0]
    if pd.isna(time_header) or 'time' not in str(time_header).lower():
        raise ValidationError(f"Missing time column as column 1. Please check guidelines for supported data structure.")

    # checks if signals are correct
    signal_row = df.iloc[1]
    expected_signals = {'F', 'VM', 'VA', 'IM', 'IA'}
    actual_signals = set(signal_row.dropna().astype(str).unique())
    if not expected_signals.issubset(actual_signals):
        raise ValidationError(f"Unexpected column structure in row 2. Please check guidelines for supported data structure.")

    data_cols = df.shape[1] - 1  # checks if data comes in sets of 5exluding time
    if data_cols % 5 != 0:
        raise ValidationError(f"Column count doesn't follow structure requirements. Please check guidelines for supported data structure.")
    
    # check that data values are numeric
    data_rows = df.iloc[4:] 
    for col in range(df.shape[1]): 
        col_values = data_rows.iloc[:, col].dropna()
        if len(col_values) == 0:
            continue
        try:
            pd.to_numeric(col_values)
        except (ValueError, TypeError):
            raise ValidationError(f"Column {col} contains non-numeric values in its data rows. Please check guidelines for supported data structure.")

    

def dict_to_df(output_dict):
    header_data = []
    column_data = []
    for location, data_dict in output_dict.items():
        for label, data in data_dict.items():
            header_data.append((location, label))
            column_data.append(data)
    
    headers = pd.MultiIndex.from_tuples(header_data, names = ['Location', 'Signal'])
    columns = np.array(column_data).T
    df = pd.DataFrame(columns, columns=headers)

    return df

def params_to_df(params):
    return pd.DataFrame(list(params.items()), columns=['Parameter', 'Value'])

def write_output(output_v, output_i, output_s, params):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        dict_to_df(output_v).to_excel(writer, sheet_name='Voltage', index=True)
        dict_to_df(output_i).to_excel(writer, sheet_name='Current', index=True)
        dict_to_df(output_s).to_excel(writer, sheet_name='Power', index=True)
        params_to_df(params).to_excel(writer, sheet_name='Params', index=False)
    buffer.seek(0)
    return buffer

