from matplotlib import pyplot as plt
import numpy as np

from backend.utils import absolute_error_per_point

def generate_graph(calculated, verified, wave_num, y_type, data_type):
    # voltage magnitudes
    plt.figure()
    plt.plot(calculated, marker='o', label=f'{y_type} {wave_num} calculated', color='red')
    plt.plot(verified, marker='o', label=f'{y_type} {wave_num} verified', color='green')
    plt.legend()
    plt.title(f'{wave_num} {data_type} {y_type} Calculated vs Verified')
    plt.xlabel('Cycle')
    plt.ylabel(f'{y_type}')
    plt.savefig(f'output_graphs/{data_type}_{y_type}_{wave_num}.png')
    


def generate_error_graph(calculated, verified, wave_num, y_type, data_type):
    error_amps_f1_v = absolute_error_per_point(calculated, verified)
    plt.figure()
    plt.plot(error_amps_f1_v, marker='o', color='purple')
    plt.axhline(0, color='gray', linestyle='--')  # reference line at zero error
    plt.title(f'{wave_num} {data_type} {y_type} Absolute Error')
    plt.xlabel('Cycle')
    plt.ylabel(' Error')
    plt.savefig(f'error_graphs/{data_type}_{y_type}_{wave_num}_error.png')
   