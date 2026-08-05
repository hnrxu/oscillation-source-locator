import numpy as np
import pandas as pd


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


def read_locations(file_name):
    df = pd.read_excel(file_name, header=None)
    locations = df.iloc[0]
    locations = locations.dropna().unique()
    locations = [l for l in locations if l != 'Time']  
    return locations

def read_excel(file_name, start):
    #using temp var names, prob change later
    df = pd.read_excel(file_name, header=None)

    times = df.iloc[5:, 0].to_numpy() 

    data = df.iloc[5:, start:start+5].dropna()

    f1_col = data.iloc[:, 0].to_numpy()
    magnitudes_v = data.iloc[:, 1].to_numpy()
    angles_v = data.iloc[:, 2].to_numpy()
    magnitudes_i = data.iloc[:, 3].to_numpy()
    angles_i = data.iloc[:, 4].to_numpy()
    return f1_col, magnitudes_v, magnitudes_i, angles_v, angles_i, times
