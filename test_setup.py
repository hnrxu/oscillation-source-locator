import math
import numpy as np


def generate_times(f1, samples_per_cycle, num_cycles):
    time_per_cycle = 1/f1
    total_time = num_cycles * time_per_cycle
    total_samples = num_cycles * samples_per_cycle 
    times = np.linspace(0, total_time, total_samples, endpoint=False)
    return times


def generate_test(f1, fos, amplitudes, angles, samples_per_cycle, num_cycles):

    freqs = [f1, f1+fos, f1-fos]
    times = generate_times(f1, samples_per_cycle, num_cycles)
    v = 0
    for i in range(len(freqs)):
        w = 2*np.pi*freqs[i]
        v += amplitudes[i] * np.cos(w*times + angles[i])

    #plt.plot(times, v)
    #plt.show()

    return f1, v, times

def generate_phasor(f1, data, times, samples_per_cycle):
    phasor = []   
    sum = 0

    w = np.ones(len(data))

    for index in range(len(data)):
        # will probably need to change this "per block" logic for w as not all blocks have same w composition 
        sum += w[index] * data[index] * np.exp(-1j*times[index]*f1*2*np.pi) #reorganize maybe
        if (index + 1) % samples_per_cycle == 0: # new period/block
            gain = np.sum(w[(index // samples_per_cycle) * samples_per_cycle: (index // samples_per_cycle) * samples_per_cycle + samples_per_cycle])
            coeff = math.sqrt(2)/gain
            phasor.append(coeff*sum)
            sum = 0

    magnitudes = np.abs(phasor)
    angles = np.angle(phasor)

    # for x in phasor:
    #     print(x.real, x.imag)
    #plt.plot(magnitudes, marker = 'o')
    #plt.show()
    # print(magnitudes)
    # print(angles)
    return magnitudes, angles