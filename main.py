import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

from excel import read_excel, write_excel
from solver import convert_to_phasor, solve
from test_setup import generate_phasor, generate_test

#add arguments if u want, TODO: also refactor this to be general later
def generate_graphs(amps_f1_v, amps_ih1_v, amps_ih2_v, 
                   amps_f1_v_verified, amps_ih1_v_verified, amps_ih2_v_verified, 
                   amps_f1_i, amps_ih1_i, amps_ih2_i, 
                   amps_f1_i_verified, amps_ih1_i_verified, amps_ih2_i_verified, 
                   angs_ih1_v, 
                   angs_ih1_v_verified):
    # voltage magnitudes
    plt.plot(amps_f1_v, marker='o', label='magnitude F1 calculated', color='red')
    plt.plot(amps_f1_v_verified, marker='o', label='magnitude F1 verified', color='green')
    plt.legend()
    plt.title('F1 Voltage Magnitudes Calculated vs Verified')
    plt.xlabel('Cycle')
    plt.ylabel('Magnitude')
    plt.savefig('voltage_magnitude_F1.png')
    plt.show()

    plt.plot(amps_ih1_v, marker='o', label='magnitude IH1 calculated', color='red')
    plt.plot(amps_ih1_v_verified, marker='o', label='magnitude IH1 verified', color='green')
    plt.legend()
    plt.title('IH1 Voltage Magnitudes Calculated vs Verified')
    plt.xlabel('Cycle')
    plt.ylabel('Magnitude')
    plt.savefig('voltage_magnitude_IH1.png')
    plt.show()

    plt.plot(amps_ih2_v, marker='o', label='magnitude IH2 calculated', color='red')
    plt.plot(amps_ih2_v_verified, marker='o', label='magnitude IH2 verified', color='green')
    plt.legend()
    plt.title('IH2 Voltage Magnitudes Calculated vs Verified')
    plt.xlabel('Cycle')
    plt.ylabel('Magnitude')
    plt.savefig('voltage_magnitude_IH2.png')
    plt.show()

    #current magnitudes
    plt.plot(amps_f1_i, marker='o', label='current F1 calculated', color='red')
    plt.plot(amps_f1_i_verified, marker='o', label='current F1 verified', color='green')
    plt.legend()
    plt.title('F1 Current Magnitudes Calculated vs Verified')
    plt.xlabel('Cycle')
    plt.ylabel('Current')
    plt.savefig('current_magnitude_F1.png')
    plt.show()

    plt.plot(amps_ih1_i, marker='o', label='current IH1 calculated', color='red')
    plt.plot(amps_ih1_i_verified, marker='o', label='current IH1 verified', color='green')
    plt.legend()
    plt.title('IH1 Current Magnitudes Calculated vs Verified')
    plt.xlabel('Cycle')
    plt.ylabel('Current')
    plt.savefig('current_magnitude_IH1.png')
    plt.show()

    plt.plot(amps_ih2_i, marker='o', label='current IH2 calculated', color='red')
    plt.plot(amps_ih2_i_verified, marker='o', label='current IH2 verified', color='green')
    plt.legend()
    plt.title('IH2 Current Magnitudes Calculated vs Verified')
    plt.xlabel('Cycle')
    plt.ylabel('Current')
    plt.savefig('current_magnitude_IH2.png')
    plt.show()

    #voltage angles
    plt.plot(angs_ih1_v, marker='o', label='angles IH1 calculated', color='red')
    plt.plot(angs_ih1_v_verified, marker='o', label='angles IH1 verified', color='green')
    plt.legend()
    plt.title('IH1 Voltage Angles Calculated vs Verified')
    plt.xlabel('Cycle')
    plt.ylabel('Angle')
    plt.savefig('voltage_angles_IH1.png')
    plt.show()

if __name__ == "__main__":

    #setting up test data
    f1_v, data_v, times_v = generate_test(60, 65, [100, 10, 100], [np.pi/6, np.pi/6, np.pi/3], 128, 12)
    phasor_mags_v, phasor_angs_v = generate_phasor(f1_v, data_v, times_v, 128)
    f1_i, data_i, times_i = generate_test(60, 65, [50, 10, 50], [0, np.pi/6, np.pi/3], 128, 12)
    phasor_mags_i, phasor_angs_i = generate_phasor(f1_i, data_i, times_i, 128)

    #setting up test file
    write_excel(phasor_mags_v, phasor_angs_v, phasor_mags_i, phasor_angs_i)


    #parsing data
    NUM_CYCLES = 4
    INPUT_FILE = 'Case2SF51input.xlsx'
    OUTPUT_FILE = 'Case2SF51outputVI.xlsx'

    phasor_mags_v, phasor_mags_i, phasor_angs_v, phasor_angs_i = read_excel(INPUT_FILE)
    phasor_v = convert_to_phasor(phasor_mags_v, phasor_angs_v)
    phasor_i = convert_to_phasor(phasor_mags_i, phasor_angs_i)

    #solve/get calculated data
    amps_f1_v = []
    amps_ih1_v = []
    amps_ih2_v = []

    angs_f1_v = []
    angs_ih1_v = []
    angs_ih2_v = []

    for i in range(len(phasor_v) // NUM_CYCLES):
        phasor_data = phasor_v[i*NUM_CYCLES: i*NUM_CYCLES+NUM_CYCLES]
        amplitudes_v, angles_v = solve(60, 60/NUM_CYCLES, phasor_data, 128, NUM_CYCLES)
        amp_f1_v, amp_ih1_v, amp_ih2_v = amplitudes_v
        ang_f1_v, ang_ih1_v, ang_ih2_v = angles_v
        amps_f1_v.append(amp_f1_v)
        amps_ih1_v.append(amp_ih1_v)
        amps_ih2_v.append(amp_ih2_v)

        angs_f1_v.append(ang_f1_v)
        angs_ih1_v.append(ang_f1_v)
        angs_ih2_v.append(ang_f1_v)

    print(amps_ih1_v)


    amps_f1_i = []
    amps_ih1_i = []
    amps_ih2_i = []

    angs_f1_i = []
    angs_ih1_i = []
    angs_ih2_i = []

    for i in range(len(phasor_i) // NUM_CYCLES):
        phasor_data = phasor_i[i*NUM_CYCLES: i*NUM_CYCLES+NUM_CYCLES]
        amplitudes_i, angles_i = solve(60, 60/NUM_CYCLES, phasor_data, 128, NUM_CYCLES)
        amp_f1_i, amp_ih1_i, amp_ih2_i = amplitudes_i
        ang_f1_i, ang_ih1_i, ang_ih2_i = angles_i
        amps_f1_i.append(amp_f1_i)
        amps_ih1_i.append(amp_ih1_i)
        amps_ih2_i.append(amp_ih2_i)
        angs_f1_i.append(ang_f1_i)
        angs_ih1_i.append(ang_f1_i)
        angs_ih2_i.append(ang_f1_i)


    #get verified data
    df_verified = pd.read_excel(OUTPUT_FILE)
    amps_f1_v_verified = df_verified['Vih1m']
    amps_ih1_v_verified = df_verified['Vih3m']
    amps_ih2_v_verified = df_verified['Vih2m']
    amps_f1_i_verified = df_verified['Iih1m']
    amps_ih1_i_verified = df_verified['Iih3m']
    amps_ih2_i_verified = df_verified['Iih2m']
    #angles, add more if want to
    angs_ih1_v_verified = df_verified['Vih1a']


    amps_f1_v = amps_f1_v[:10]
    amps_ih1_v = amps_ih1_v[:10]
    amps_ih2_v = amps_ih2_v[:10]
    amps_f1_i = amps_f1_i[:10]
    amps_ih1_i = amps_ih1_i[:10]
    amps_ih2_i = amps_ih2_i[:10]
    angs_ih1_v = angs_ih1_v[:10]

    generate_graphs(amps_f1_v, amps_ih1_v, amps_ih2_v, 
                   amps_f1_v_verified, amps_ih1_v_verified, amps_ih2_v_verified, 
                   amps_f1_i, amps_ih1_i, amps_ih2_i, 
                   amps_f1_i_verified, amps_ih1_i_verified, amps_ih2_i_verified, 
                   angs_ih1_v, 
                   angs_ih1_v_verified)










        
    
    


