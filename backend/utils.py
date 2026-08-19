import numpy as np


def convert_to_phasor(magnitudes, angles):
    phasor = magnitudes * np.exp(1j * np.radians(angles))
    return phasor

def calculate_power(amps_f1_v, amps_f1_i, angs_f1_v, angs_f1_i, 
                    amps_ih1_v, amps_ih1_i, angs_ih1_v, angs_ih1_i,
                    amps_ih2_v, amps_ih2_i, angs_ih2_v, angs_ih2_i):
    sf1 = np.array(amps_f1_v) * np.array(amps_f1_i)
    angle_diff_rad = np.radians(np.array(angs_f1_v) - np.array(angs_f1_i))
    pf1 = sf1 * np.cos(angle_diff_rad)
    qf1 = sf1 * np.sin(angle_diff_rad)

    sih1 = np.array(amps_ih1_v) * np.array(amps_ih1_i)
    angle_diff_rad = np.radians(np.array(angs_ih1_v) - np.array(angs_ih1_i))
    pih1 = sih1 * np.cos(angle_diff_rad)
    qih1 = sih1 * np.sin(angle_diff_rad)

    sih2 = np.array(amps_ih2_v) * np.array(amps_ih2_i)
    angle_diff_rad = np.radians(np.array(angs_ih2_v) - np.array(angs_ih2_i))
    pih2 = sih2 * np.cos(angle_diff_rad)
    qih2 = sih2 * np.sin(angle_diff_rad)
    return sf1.tolist(), sih1.tolist(), sih2.tolist(), pf1.tolist(), pih1.tolist(), pih2.tolist(), qf1.tolist(), qih1.tolist(), qih2.tolist()


def percent_error_per_point(calculated, verified):
    return (np.array(verified) - np.array(calculated)) / np.array(verified) * 100

def absolute_error_per_point(calculated, verified):
    return np.array(calculated) - np.array(verified)

def nrmse(calculated, verified, nominal):
    calculated, verified = np.array(calculated), np.array(verified)
    rmse = np.sqrt(np.mean((calculated - verified)**2))
    return rmse / nominal * 100

def rmse_angle_percent(calculated, verified):
    diff = (np.array(calculated) - np.array(verified) + 180) % 360 - 180
    rmse = np.sqrt(np.mean(diff**2)) / 360
    return rmse * 100

def mape(true, estimated):
    true, estimated = np.array(true), np.array(estimated)
    return np.mean(np.abs((true - estimated) / true)) * 100


def safe_convert(value, converter, default):
    if value is None or value == '':
        return default
    return converter(value)
