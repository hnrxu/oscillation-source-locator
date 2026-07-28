import numpy as np
from test_setup import generate_times


def convert_to_phasor(magnitudes, angles):
    phasor = magnitudes * np.exp(1j * angles)
    return phasor

def solve(f1, fos, phasor, samples_per_cycle, num_cycles):
    freqs = [f1, f1+fos, f1-fos]
    times = generate_times(f1, samples_per_cycle, num_cycles)
    weights = np.ones(len(times))

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
            for i in range(samples_per_cycle):
                index = k*samples_per_cycle + i
                sum_cos += weights[index] * np.cos(2*np.pi*f*times[index]) * np.exp(-1j*times[index]*2*np.pi*f1)
                sum_sin += weights[index] * np.sin(2*np.pi*f*times[index]) * np.exp(-1j*times[index]*2*np.pi*f1)
            column_cos.append((2/gain)*sum_cos)
            column_sin.append((2/gain)*sum_sin)

        columns.append(column_cos)
        columns.append(column_sin)

    m = np.column_stack(columns)
    print(m.shape)

    m_real = np.vstack((m.real, m.imag))
    phasor = np.array(phasor)
    phasor_real = np.concatenate((phasor.real, phasor.imag))


    x, residuals, rank, s = np.linalg.lstsq(m_real, phasor_real, rcond=None)

    amplitudes = []
    angles = []
    for i in range(0, len(x), 2):
        v = np.sqrt(x[i]**2 + x[i+1]**2)
        theta = np.arctan2(-x[i+1], x[i])
        amplitudes.append(v)
        angles.append(theta)

    # calculated
    return amplitudes, np.degrees(angles)