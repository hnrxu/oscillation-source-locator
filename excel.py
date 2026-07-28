import numpy as np
import pandas as pd


def write_excel(magnitudes_v, angles_v, magnitudes_i, angles_i):
    #using temp var names, prob change later
    df = pd.DataFrame({
        'MVa': magnitudes_v,
        'MIa': magnitudes_i,
        'AVa': angles_v,
        'AIa': angles_i
    })

    df.to_excel('test_input.xlsx', index=False)

def read_excel(file_name):
    #using temp var names, prob change later
    df = pd.read_excel(file_name)
    magnitudes_v = df['MVa'].to_numpy()
    magnitudes_i = df['MIa'].to_numpy()
    angles_v = np.radians(df['AVa'].to_numpy())
    angles_i = np.radians(df['AIa'].to_numpy())
    return magnitudes_v, magnitudes_i, angles_v, angles_i