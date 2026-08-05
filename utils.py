import numpy as np


def convert_to_phasor(magnitudes, angles):
    phasor = magnitudes * np.exp(1j * angles)
    return phasor


def percent_error_per_point(calculated, verified):
    return (np.array(verified) - np.array(calculated)) / np.array(verified) * 100

def absolute_error_per_point(calculated, verified):
    return np.array(calculated) - np.array(verified)

def nrmse(calculated, verified, nominal):
    calculated, verified = np.array(calculated), np.array(verified)
    rmse = np.sqrt(np.mean((calculated - verified)**2))
    return rmse / nominal * 100

def rmse_angle_deg(calculated, verified):
    diff = (np.array(calculated) - np.array(verified) + 180) % 360 - 180
    return np.sqrt(np.mean(diff**2))

def mape(true, estimated):
    true, estimated = np.array(true), np.array(estimated)
    return np.mean(np.abs((true - estimated) / true)) * 100