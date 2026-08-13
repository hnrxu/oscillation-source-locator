from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from backend.excel import read_excel
from backend.test_setup import generate_times
from scipy.signal import find_peaks
from scipy.signal import detrend
import backend.config as config

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
    mags = np.abs(fft)

    cutoff_index = np.argmin(np.abs(freqs - config.SPECTRAL_CUTOFF_HZ))
    idx = np.argmax(mags[cutoff_index:]) + cutoff_index
    period = 1/freqs[idx]
    f_period = 1/60
    num_cycles = period/f_period
    max_mag = mags[idx] / np.mean(column)


    plt.figure()
    plt.bar(range(len(mags[1:250])), mags[1:250])   # only show first 250 bins
    plt.xlabel('Frequency index')
    plt.ylabel('Magnitude')
    plt.title(f'fft magnitudes - {location}')
    plt.savefig(f'fft_{location}.png')
    plt.close()

    print(f"{location} - {freqs[idx]}")
    print(f'{cutoff_index}')
    print(f"[{location}] index of that max: {np.argmax(mags[cutoff_index:])+cutoff_index}")
    print(f"[{location}] normalized max = {max_mag}")
    print(f"[{location}] - {num_cycles}")

    # # require at least 2 repeats to even consider this a "real" period
    # if num_cycles > len(column) / 2:
    #     return (-np.inf, None)

    return (max_mag, num_cycles, period)

def detect_max_fos(locations, cached_data):
    max_mag = -np.inf
    best_num_cycles = None
    best_period = None
    mags = []
    cycles = []
    for i in range(len(locations)):
        start = i*5 + 1
        f1_freqs, phasor_mags_v, phasor_mags_i, phasor_angs_v, phasor_angs_i, times = cached_data[i]
        phasor_mags_v = phasor_mags_v.astype(float)
        mag, num_cycles, period = detect_fos(phasor_mags_v, locations[i], times)
        mags.append(mag)
        cycles.append(num_cycles)
        if mag > max_mag:
            max_mag = mag
            best_num_cycles = num_cycles
            best_period = period


    plt.figure(figsize=(14, 6))
    bars = plt.bar(range(len(mags)), mags)

    for idx, (bar, cycles) in enumerate(zip(bars, cycles)):
        height = bar.get_height()
        label = f"{cycles:.1f}" if cycles is not None else "N/A"
        plt.text(bar.get_x() + bar.get_width()/2, height,
                  label, ha='center', va='bottom', fontsize=7, rotation=90)

    plt.xlabel('Location')
    plt.ylabel('Magnitude')
    plt.title('FFT best magnitudes (labeled with detected num_cycles)')
    plt.xticks(range(len(locations)), locations, rotation=90, fontsize=6)
    plt.tight_layout()
    plt.savefig('fft_best_mags.png')

    if best_num_cycles is None or best_period is None:
        raise ValueError("No valid oscillation detected in any location")
    print(round(best_num_cycles))

    return round(best_num_cycles), best_period





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



def solve(f1, fos, phasor, times, samples_per_cycle, m = 128/2):
    freqs = [f1, f1-fos, f1+fos]
    weights = np.ones(len(times)*samples_per_cycle)

    # making the eq matrix
    columns = []
    for f in freqs:
        column_cos = []
        column_sin = []
        for k in range(len(phasor)):
            #k is the "block" num

            sum_cos = 0
            sum_sin = 0
            gain = sum(weights[k*samples_per_cycle:k*samples_per_cycle+samples_per_cycle])
            delta_t = (1/f1)/samples_per_cycle
            for i in range(samples_per_cycle):
                index = k*samples_per_cycle + i
                sum_cos += weights[index] * np.cos(2*np.pi*f*(i*delta_t + times[k] - m*delta_t)) * np.exp(-1j*2*np.pi*f1*(i*delta_t + times[k] - m*delta_t))
                sum_sin += weights[index] * np.sin(2*np.pi*f*(i*delta_t + times[k] - m*delta_t)) * np.exp(-1j*2*np.pi*f1*(i*delta_t + times[k] - m*delta_t))  
            column_cos.append((2/gain)*sum_cos)
            column_sin.append((2/gain)*sum_sin)

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
        amplitudes.append(v)
        angles.append(theta)

    # calculated
    return amplitudes, np.degrees(angles)