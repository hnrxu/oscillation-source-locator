from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from excel import read_excel
from test_setup import generate_times
from scipy.signal import find_peaks
from scipy.signal import detrend
import config 

# def detect_beat_cycles(column):
#     segment = column - column.mean()

#     # autocorrelation
#     autocorr = np.correlate(segment, segment, mode='full')
#     autocorr = autocorr[len(autocorr)//2:]
#     peaks, _ = find_peaks(autocorr)
#     period_autocorr = peaks[0] if len(peaks) > 0 else None

#     # fft
#     fft = np.fft.rfft(segment)
#     freqs = np.fft.rfftfreq(len(segment), d=1)  # d=1 since data is 1 sample/cycle
#     mags = np.abs(fft)
#     idx = np.argmax(mags[1:]) + 1
#     period_fft = 1/freqs[idx]

    
#     return round((period_autocorr + period_fft) / 2)

def detect_fos(column, location, times):
    segment = detrend(column) - np.mean(detrend(column))
    fft = np.fft.rfft(segment)
    delta_t = np.median(np.diff(times))

    freqs = np.fft.rfftfreq(len(segment), d=delta_t)
    raw_mags = np.abs(fft) / np.mean(column)

    cutoff_index = np.argmin(np.abs(freqs - config.SPECTRAL_CUTOFF_HZ))
    idx = np.argmax(raw_mags[cutoff_index:]) + cutoff_index

    max_mag = raw_mags[idx]   # actual comparable metric

    # normalization only for charting
    mags = raw_mags / raw_mags[idx] * 100

    period = 1/freqs[idx]
    f_period = 1/60
    num_cycles = period/f_period

    return (max_mag, num_cycles, period, mags, freqs)

def detect_max_fos(locations, cached_data):
    max_mag = -np.inf
    best_num_cycles = None
    best_period = None
    best_mags = []
    best_freqs = []
    best_location = None
    for i in range(len(locations)):
        start = i*5 + 1
        f1_freqs, phasor_mags_v, phasor_mags_i, phasor_angs_v, phasor_angs_i, times = cached_data[i]
        phasor_mags_v = phasor_mags_v.astype(float)
        mag, num_cycles, period, fft_mags, fft_freqs = detect_fos(phasor_mags_v, locations[i], times)
      
        if mag > max_mag:
            max_mag = mag
            best_num_cycles = num_cycles
            best_period = period
            best_mags = fft_mags
            best_freqs = fft_freqs
            best_location = locations[i]


    if best_num_cycles is None or best_period is None:
        raise ValueError("No valid oscillation detected in any location")

    return round(best_num_cycles), best_period, best_mags, best_freqs, best_location





# def solve_b(f1, fos, phasor, samples_per_cycle, num_cycles, skip_rows = False):
#     freqs = [f1, f1-fos, f1+fos]
#     times = generate_times(f1, samples_per_cycle, num_cycles)
#     weights = np.ones(len(times))

#     # making the eq matrix
#     columns = []
#     for f in freqs:
#         column_cos = []
#         column_sin = []
#         for k in range(len(phasor)):
#             #k is the "block" num
 
#             sum_cos = 0
#             sum_sin = 0
#             gain = sum(weights[k*samples_per_cycle:k*samples_per_cycle+samples_per_cycle])
#             for i in range(samples_per_cycle):
#                 index = k*samples_per_cycle + i
#                 sum_cos += weights[index] * np.cos(2*np.pi*f*times[index]) * np.exp(-1j*times[index]*2*np.pi*f1)
#                 sum_sin += weights[index] * np.sin(2*np.pi*f*times[index]) * np.exp(-1j*times[index]*2*np.pi*f1)   
#             column_cos.append((2/gain)*sum_cos)
#             column_sin.append((2/gain)*sum_sin)

#         columns.append(column_cos)
#         columns.append(column_sin)

#     m = np.column_stack(columns)

#     # testing every other row
#     if skip_rows:
#         m = m[::2]
#         phasor = phasor[::2]
#     print(m.shape)

#     m_real = np.vstack((m.real, m.imag))
#     phasor = np.array(phasor)
#     phasor_real = np.concatenate((phasor.real, phasor.imag))



#     x, residuals, rank, s = np.linalg.lstsq(m_real, phasor_real, rcond=None)

#     amplitudes = []
#     angles = []
#     for i in range(0, len(x), 2):
#         v = np.sqrt(x[i]**2 + x[i+1]**2)
#         theta = np.arctan2(-x[i+1], x[i])
#         amplitudes.append(v)
#         angles.append(theta)

#     # calculated
#     return amplitudes, np.degrees(angles)



def solve(f1, fos, phasor, times, samples_per_cycle, m=128/2):
    freqs = [f1, f1-fos, f1+fos]
    num_blocks = len(phasor)
    delta_t = (1/f1)/samples_per_cycle

    weights = np.ones((num_blocks, samples_per_cycle))
    gain = weights.sum(axis=1)  # per-block gain, shape (num_blocks,)

    i_arr = np.arange(samples_per_cycle)
    t_i = i_arr * delta_t  # time-within-cycle for each sample, shape (samples_per_cycle,)

    times = np.asarray(times)
    shifted_times = times - m * delta_t  # per-block time offset, shape (num_blocks,)

    # T[k, i] = i*delta_t + times[k] - m*delta_t, for every block k and sample i at once
    T = shifted_times[:, None] + t_i[None, :]  # shape (num_blocks, samples_per_cycle)

    columns = []
    for f in freqs:
        phase = 2 * np.pi * f * T
        carrier = np.exp(-1j * 2 * np.pi * f1 * T)
        cos_term = np.cos(phase) * carrier
        sin_term = np.sin(phase) * carrier

        column_cos = (2 / gain) * np.sum(weights * cos_term, axis=1)
        column_sin = (2 / gain) * np.sum(weights * sin_term, axis=1)

        columns.append(column_cos)
        columns.append(column_sin)

    matrix = np.column_stack(columns)
    matrix_real = np.vstack((matrix.real, matrix.imag))
    phasor = np.array(phasor)
    phasor_real = np.concatenate((phasor.real, phasor.imag))

    x, residuals, rank, s = np.linalg.lstsq(matrix_real, phasor_real, rcond=None)

    amplitudes = []
    angles = []
    for i in range(0, len(x), 2):
        v = np.sqrt(x[i]**2 + x[i+1]**2)
        theta = np.arctan2(-x[i+1], x[i])
        amplitudes.append(float(v))
        angles.append(float(np.degrees(theta)))

    return amplitudes, angles


# TODO: understand the vectorization