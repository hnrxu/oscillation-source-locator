import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

from excel import read_excel, read_locations, write_excel, write_excel_power
from graphs import generate_error_graph, generate_graph
from solver import detect_beat_cyles, detect_f1, solve
from test_setup import generate_phasor, generate_phasor_times, generate_test
from utils import convert_to_phasor, mape, nrmse, rmse_angle_deg

SAMPLES_PER_CYCLE = 128
#F1 = 60
INPUT_FILE = 'TFcase3full-1.xlsx'
OUTPUT_FILE = 'Case1WF23outputVI.xlsx'

# this only for 2test cases
M = 63.46752
target_offset_seconds = M * ((1/60.03337057912106)/128)
m_for_dynamic = target_offset_seconds / ((1/60.03337057912106)/SAMPLES_PER_CYCLE)
#TODO:: m changes with samples

delta_t = (1/60)/128
offset_seconds = 32 * delta_t 



if __name__ == "__main__":

#    # setting up test data
#     f1_v, data_v, times_v = generate_test(60, 60/17, [100, 50, 10], [np.pi/6, 0, np.pi/3], 128, 170)
#     phasor_mags_v, phasor_angs_v = generate_phasor(f1_v, data_v, times_v, 128)
#     f1_i, data_i, times_i = generate_test(60, 60/17, [50, 10, 5], [0, np.pi/6, np.pi/4], 128, 170)
#     phasor_mags_i, phasor_angs_i = generate_phasor(f1_i, data_i, times_i, 128)
#     phasor_times = generate_phasor_times(60, len(phasor_mags_v), offset_seconds)
#     #setting up test file
#     write_excel(phasor_times, phasor_mags_v, phasor_angs_v, phasor_mags_i, phasor_angs_i)
    locations = read_locations(INPUT_FILE)
    for i in range(len(locations)):
        #parsing data
        start = i*5 + 1
        f1_freqs, phasor_mags_v, phasor_mags_i, phasor_angs_v, phasor_angs_i, times = read_excel(INPUT_FILE, start)
        phasor_v = convert_to_phasor(phasor_mags_v, phasor_angs_v)
        phasor_i = convert_to_phasor(phasor_mags_i, phasor_angs_i)

        #solve/get calculated data
        #get fos
        NUM_CYCLES = detect_beat_cyles(phasor_mags_v)
        print(NUM_CYCLES)

        F1 = detect_f1(times)
        print(F1)

        amps_f1_v = []
        amps_ih1_v = []
        amps_ih2_v = []

        angs_f1_v = []
        angs_ih1_v = []
        angs_ih2_v = []

        for i in range(len(phasor_v) // NUM_CYCLES):
            phasor_data = phasor_v[i*NUM_CYCLES: i*NUM_CYCLES+NUM_CYCLES]
            times_data = times[i*NUM_CYCLES: i*NUM_CYCLES+NUM_CYCLES]    
            amplitudes_v, angles_v = solve(F1, F1/NUM_CYCLES, phasor_data, times_data, SAMPLES_PER_CYCLE, NUM_CYCLES, 96)

            amp_f1_v, amp_ih1_v, amp_ih2_v = amplitudes_v
            ang_f1_v, ang_ih1_v, ang_ih2_v = angles_v
            amps_f1_v.append(amp_f1_v)
            amps_ih1_v.append(amp_ih1_v)
            amps_ih2_v.append(amp_ih2_v)
            angs_f1_v.append(ang_f1_v)
            angs_ih1_v.append(ang_ih1_v)
            angs_ih2_v.append(ang_ih2_v)



        amps_f1_i = []
        amps_ih1_i = []
        amps_ih2_i = []

        angs_f1_i = []
        angs_ih1_i = []
        angs_ih2_i = []

        for i in range(len(phasor_i) // NUM_CYCLES):
            phasor_data = phasor_i[i*NUM_CYCLES: i*NUM_CYCLES+NUM_CYCLES]
            times_data = times[i*NUM_CYCLES: i*NUM_CYCLES+NUM_CYCLES]    
            amplitudes_i, angles_i = solve(F1, F1/NUM_CYCLES, phasor_data, times_data, SAMPLES_PER_CYCLE, NUM_CYCLES, 96)
            
            amp_f1_i, amp_ih1_i, amp_ih2_i = amplitudes_i
            ang_f1_i, ang_ih1_i, ang_ih2_i = angles_i
            amps_f1_i.append(amp_f1_i)
            amps_ih1_i.append(amp_ih1_i)
            amps_ih2_i.append(amp_ih2_i)
            angs_f1_i.append(ang_f1_i)
            angs_ih1_i.append(ang_ih1_i)
            angs_ih2_i.append(ang_ih2_i)


        # df = pd.DataFrame({
        #     'Vih1m': amps_f1_v,
        #     'Vih2m': amps_ih1_v,
        #     'Vih3m': amps_ih2_v,
        #     'Vih1a': angs_f1_v,
        #     'Vih2a': angs_ih1_v,
        #     'Vih3a': angs_ih2_v,
        #     'Iih1m': amps_f1_i,
        #     'Iih2m': amps_ih1_i,
        #     'Iih3m': amps_ih2_i,
        #     'Iih1a': angs_f1_i,
        #     'Iih2a': angs_ih1_i,
        #     'Iih3a': angs_ih2_i,
            
        # })

        # df.to_excel('test_output.xlsx', index=False)



        #graphing/comparison
        #get verified data
        df_verified = pd.read_excel(OUTPUT_FILE)
        amps_f1_v_verified = df_verified['Vih1m']
        amps_ih1_v_verified = df_verified['Vih2m']
        amps_ih2_v_verified = df_verified['Vih3m']
        amps_f1_i_verified = df_verified['Iih1m']
        amps_ih1_i_verified = df_verified['Iih2m']
        amps_ih2_i_verified = df_verified['Iih3m']
        #angles, add more if want to
        angs_f1_v_verified = df_verified['Vih1a']
        angs_ih1_v_verified = df_verified['Vih2a']
        angs_ih2_v_verified = df_verified['Vih3a']
        angs_f1_i_verified = df_verified['Iih1a']
        angs_ih1_i_verified = df_verified['Iih2a']
        angs_ih2_i_verified = df_verified['Iih3a']

        # amps_f1_v = amps_f1_v[:10]
        # amps_ih1_v = amps_ih1_v[:10]
        # amps_ih2_v = amps_ih2_v[:10]
        # amps_f1_i = amps_f1_i[:10]
        # amps_ih1_i = amps_ih1_i[:10]
        # amps_ih2_i = amps_ih2_i[:10]
        # angs_ih1_v = angs_ih1_v[:10]



        generate_graph(amps_f1_v, amps_f1_v_verified, "F1", "Magnitude", "Voltage")
        generate_graph(amps_ih1_v, amps_ih1_v_verified, "IH1", "Magnitude", "Voltage")
        generate_graph(amps_ih2_v, amps_ih2_v_verified, "IH2", "Magnitude", "Voltage")
        generate_graph(amps_f1_i, amps_f1_i_verified, "F1", "Magnitude", "Current")
        generate_graph(amps_ih1_i, amps_ih1_i_verified, "IH1", "Magnitude", "Current")
        generate_graph(amps_ih2_i, amps_ih2_i_verified, "IH2", "Magnitude", "Current")

        generate_graph(angs_f1_v, angs_f1_v_verified, "F1", "Angle", "Voltage")
        generate_graph(angs_ih1_v, angs_ih1_v_verified, "IH1", "Angle", "Voltage")
        generate_graph(angs_ih2_v, angs_ih2_v_verified, "IH2", "Angle", "Voltage")
        generate_graph(angs_f1_i, angs_f1_i_verified, "F1", "Angle", "Current")
        generate_graph(angs_ih1_i, angs_ih1_i_verified, "IH1", "Angle", "Current")
        generate_graph(angs_ih2_i, angs_ih2_i_verified, "IH2", "Angle", "Current")
        


        #generate graphs for error
        # generate_error_graph(amps_f1_v, amps_f1_v_verified, "F1", "Magnitude", "Voltage")
        # generate_error_graph(amps_ih1_v, amps_ih1_v_verified, "IH1", "Magnitude", "Voltage")
        # generate_error_graph(amps_ih2_v, amps_ih2_v_verified, "IH2", "Magnitude", "Voltage")
        # generate_error_graph(amps_f1_i, amps_f1_i_verified, "F1", "Magnitude", "Current")
        # generate_error_graph(amps_ih1_i, amps_ih1_i_verified, "IH1", "Magnitude", "Current")
        # generate_error_graph(amps_ih2_i, amps_ih2_i_verified, "IH2", "Magnitude", "Current")

        # generate_error_graph(angs_f1_v, angs_f1_v_verified, "F1", "Angle", "Voltage")
        # generate_error_graph(angs_ih1_v, angs_ih1_v_verified, "IH1", "Angle", "Voltage")
        # generate_error_graph(angs_ih2_v, angs_ih2_v_verified, "IH2", "Angle", "Voltage")
        # generate_error_graph(angs_f1_i, angs_f1_i_verified, "F1", "Angle", "Current")
        # generate_error_graph(angs_ih1_i, angs_ih1_i_verified, "IH1", "Angle", "Current")
        # generate_error_graph(angs_ih2_i, angs_ih2_i_verified, "IH2", "Angle", "Current")
    

        #trying to get overall error 
        print('magnitudes:')
        print(mape(amps_f1_v, amps_f1_v_verified))
        print(mape(amps_ih1_v, amps_ih1_v_verified))
        print(mape(amps_ih2_v, amps_ih2_v_verified))

        print(mape(amps_f1_i, amps_f1_i_verified))
        print(mape(amps_ih1_i, amps_ih1_i_verified))
        print(mape(amps_ih2_i, amps_ih2_i_verified))

        print('angles:')
        print(rmse_angle_deg(angs_f1_v, angs_f1_v_verified))
        print(rmse_angle_deg(angs_ih1_v, angs_ih1_v_verified))
        print(rmse_angle_deg(angs_ih2_v, angs_ih2_v_verified))

        print(rmse_angle_deg(angs_f1_i, angs_f1_i_verified))
        print(rmse_angle_deg(angs_ih1_i, angs_ih1_i_verified))
        print(rmse_angle_deg(angs_ih2_i, angs_ih2_i_verified))

        # generate S (power) #TODO: refactor this section
        s1 = np.array(amps_f1_v) * np.array(amps_f1_i)
        angle_diff_rad = np.radians(np.array(angs_f1_v) - np.array(angs_f1_i))
        p1 = s1 * np.cos(angle_diff_rad)

        sih1 = np.array(amps_ih1_v) * np.array(amps_ih1_i)
        angle_diff_rad = np.radians(np.array(angs_ih1_v) - np.array(angs_ih1_i))
        pih1 = sih1 * np.cos(angle_diff_rad)

        sih2 = np.array(amps_ih2_v) * np.array(amps_ih2_i)
        angle_diff_rad = np.radians(np.array(angs_ih2_v) - np.array(angs_ih2_i))
        pih2 = sih2 * np.cos(angle_diff_rad)

        write_excel_power(s1, p1, sih1, pih1, sih2, pih2)
        
        plt.figure()
        x = np.arange(len(pih1))
        width = 0.35
        plt.bar(x - width/2, pih1, width, label='IH1')
        plt.bar(x + width/2, pih2, width, label='IH2')
        plt.legend()
        plt.xlabel('Cycle')
        plt.ylabel('Power')
        plt.title('IH1 & IH2 Power')
        plt.show()

    
# poewr chart
# sensitivty stdy
# detect f1
# m?? how to detect
# missing data enough data 2xcycles problem/solution
# phenomenon with m that if shifted half cycle, still correct for mag

#TODO: try with nrmse instead for mags


    

    










        
    
    


