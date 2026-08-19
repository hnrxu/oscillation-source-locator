import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

from backend.excel import read_excel, read_locations, write_excel, write_excel_power, write_output_excel
from backend.graphs import generate_error_graph, generate_graph
from backend.solver import detect_max_fos, solve
from backend.test_setup import generate_phasor, generate_phasor_times, generate_test
from backend.utils import calculate_power, convert_to_phasor, mape, nrmse, rmse_angle_deg
import backend.config as config

# SAMPLES_PER_CYCLE = 128
#F1 = 60
# INPUT_FILE = 'TFcase3full-1.xlsx'
# OUTPUT_FILE = 'Case1WF23outputVI.xlsx'

# # this only for 2test cases
# M = 63.46752
# target_offset_seconds = M * ((1/60.03337057912106)/128)
# m_for_dynamic = target_offset_seconds / ((1/60.03337057912106)/SAMPLES_PER_CYCLE)


# delta_t = (1/60)/128
# offset_seconds = 32 * delta_t 



if __name__ == "__main__":

#    # setting up test data
#     f1_v, data_v, times_v = generate_test(60, 60/17, [100, 50, 10], [np.pi/6, 0, np.pi/3], 128, 170)
#     phasor_mags_v, phasor_angs_v = generate_phasor(f1_v, data_v, times_v, 128)
#     f1_i, data_i, times_i = generate_test(60, 60/17, [50, 10, 5], [0, np.pi/6, np.pi/4], 128, 170)
#     phasor_mags_i, phasor_angs_i = generate_phasor(f1_i, data_i, times_i, 128)
#     phasor_times = generate_phasor_times(60, len(phasor_mags_v), offset_seconds)
#     #setting up test file
#     write_excel(phasor_times, phasor_mags_v, phasor_angs_v, phasor_mags_i, phasor_angs_i)
    output_v = {}
    output_i = {}
    output_s = {}
    locations = read_locations(config.INPUT_FILE)

    cached_data = {}
    for i in range(len(locations)):
        start = i*5 + 1
        cached_data[i] = read_excel(config.INPUT_FILE, start, config.T_START, config.T_END)

 
    # finding highest fos from all locations
    num_cycles, beat_period = detect_max_fos(locations, cached_data)

    for i in range(len(locations)):

        #parsing data
        start = i*5 + 1
        f1_freqs, phasor_mags_v, phasor_mags_i, phasor_angs_v, phasor_angs_i, times = cached_data[i]
        phasor_v = convert_to_phasor(phasor_mags_v, phasor_angs_v)
        phasor_i = convert_to_phasor(phasor_mags_i, phasor_angs_i)
        print(f"start={start}, len(locations)={len(locations)}")
        print(f"f1_freqs[:5]={f1_freqs[:5]}")
        print(f"phasor_mags_v[:5]={phasor_mags_v[:5]}")
        print(f"phasor_angs_v[:5]={phasor_angs_v[:5]}")   # should be small values (radians), not large (degrees)
        print(f"beat_period={beat_period}")                # should be ≈0.2832

        assert len(phasor_v) == len(phasor_i), "Voltage and current phasor lengths don't match"

        #solve/get calculated data
        #get fos
  

        # F1 = detect_f1(times)
        # print(F1)
        times_output = []

        amps_f1_v = []
        amps_ih1_v = []
        amps_ih2_v = []

        angs_f1_v = []
        angs_ih1_v = []
        angs_ih2_v = []

        j = 0
        while j < (times[len(times)-1] // beat_period):
            
            phasor_start_idx = np.argmin(np.abs(j*beat_period - times))
            phasor_end_idx = np.argmin(np.abs(j*beat_period+beat_period - times))

            phasor_data = phasor_v[phasor_start_idx: phasor_end_idx]

            # 18 total, may change 
            temp = j
            while len(phasor_data) < config.MIN_NUM_DATA:
                
                if j-temp >= config.MAX_PERIODS_PER_CALC:
                    break

                if j+1 < times[len(times)-1] // beat_period:
                    j += 1
                    phasor_end_idx = np.argmin(np.abs(j*beat_period+beat_period - times))
                    phasor_data = phasor_v[phasor_start_idx: phasor_end_idx]
                else:
                    break
            
            if j >= times[len(times)-1] // beat_period:
                break

    


            times_data = times[phasor_start_idx: phasor_end_idx]
            f1_freqs_data = f1_freqs[phasor_start_idx: phasor_end_idx]
            f1 = np.mean(f1_freqs_data) 
            print(f"CALLING SOLVE: f1={f1}, fos={f1/num_cycles}, len(phasor_data)={len(phasor_data)}, len(times_data)={len(times_data)}, samples_per_cycle={config.SAMPLES_PER_CYCLE}, m={config.M}")
            print(f"phasor_data (full): {phasor_data}")
            print(f"times_data (full): {times_data}")

            amplitudes_v, angles_v = solve(f1, f1/num_cycles, phasor_data, times_data, config.SAMPLES_PER_CYCLE, config.M)

            amp_f1_v, amp_ih1_v, amp_ih2_v = amplitudes_v
            ang_f1_v, ang_ih1_v, ang_ih2_v = angles_v

            print(f"RAW amplitudes_v returned: {amplitudes_v}")
            print(f"amp_f1_v after unpacking: {amp_f1_v}")
            amps_f1_v.append(amp_f1_v)
            amps_ih1_v.append(amp_ih1_v)
            amps_ih2_v.append(amp_ih2_v)
            angs_f1_v.append(ang_f1_v)
            angs_ih1_v.append(ang_ih1_v)
            angs_ih2_v.append(ang_ih2_v)

            # only do this once
            times_output.append(times_data[0])

            j += 1


        amps_f1_i = []
        amps_ih1_i = []
        amps_ih2_i = []

        angs_f1_i = []
        angs_ih1_i = []
        angs_ih2_i = []

        print("number produced:", len(amps_f1_v))
        print("times_output:", times_output)
        print("last input time:", times[-1])
        print("limit:", times[-1] // beat_period)


        j = 0
        while j < (times[len(times)-1] // beat_period):
            
            phasor_start_idx = np.argmin(np.abs(j*beat_period - times))
            phasor_end_idx = np.argmin(np.abs(j*beat_period+beat_period - times))

            phasor_data = phasor_i[phasor_start_idx: phasor_end_idx]

            # 18 total, may change 
            temp = j
            while len(phasor_data) < config.MIN_NUM_DATA:

                if j-temp >= config.MAX_PERIODS_PER_CALC:
                    break
                
                if j+1 < times[len(times)-1] // beat_period:
                    j += 1
                    phasor_end_idx = np.argmin(np.abs(j*beat_period+beat_period - times))
                    phasor_data = phasor_i[phasor_start_idx: phasor_end_idx]
                else:
                    break
            
            if j >= times[len(times)-1] // beat_period:
                break


            times_data = times[phasor_start_idx: phasor_end_idx]
            f1_freqs_data = f1_freqs[phasor_start_idx: phasor_end_idx]
            f1 = np.mean(f1_freqs_data) 

            amplitudes_i, angles_i = solve(f1, f1/num_cycles, phasor_data, times_data, config.SAMPLES_PER_CYCLE, config.M)
            
            amp_f1_i, amp_ih1_i, amp_ih2_i = amplitudes_i
            ang_f1_i, ang_ih1_i, ang_ih2_i = angles_i

            
            amps_f1_i.append(amp_f1_i)
            amps_ih1_i.append(amp_ih1_i)
            amps_ih2_i.append(amp_ih2_i)
            angs_f1_i.append(ang_f1_i)
            angs_ih1_i.append(ang_ih1_i)
            angs_ih2_i.append(ang_ih2_i)

            j += 1

        
        assert len(amps_f1_v) == len(amps_f1_i), \
        f"Block count mismatch: voltage={len(amps_f1_v)}, current={len(amps_f1_i)}"

        all_lists = [amps_f1_v, amps_ih1_v, amps_ih2_v, angs_f1_v, angs_ih1_v, angs_ih2_v, amps_f1_i, amps_ih1_i, amps_ih2_i, angs_f1_i, angs_ih1_i, angs_ih2_i]
        if any(len(lst) == 0 for lst in all_lists):
            raise ValueError("Results are empty! Maybe not enough data provided")


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
        # df_verified = pd.read_excel(OUTPUT_FILE)
        # amps_f1_v_verified = df_verified['Vih1m']
        # amps_ih1_v_verified = df_verified['Vih2m']
        # amps_ih2_v_verified = df_verified['Vih3m']
        # amps_f1_i_verified = df_verified['Iih1m']
        # amps_ih1_i_verified = df_verified['Iih2m']
        # amps_ih2_i_verified = df_verified['Iih3m']
        # #angles, add more if want to
        # angs_f1_v_verified = df_verified['Vih1a']
        # angs_ih1_v_verified = df_verified['Vih2a']
        # angs_ih2_v_verified = df_verified['Vih3a']
        # angs_f1_i_verified = df_verified['Iih1a']
        # angs_ih1_i_verified = df_verified['Iih2a']
        # angs_ih2_i_verified = df_verified['Iih3a']

        # amps_f1_v = amps_f1_v[:10]
        # amps_ih1_v = amps_ih1_v[:10]
        # amps_ih2_v = amps_ih2_v[:10]
        # amps_f1_i = amps_f1_i[:10]
        # amps_ih1_i = amps_ih1_i[:10]
        # amps_ih2_i = amps_ih2_i[:10]
        # angs_ih1_v = angs_ih1_v[:10]



        # generate_graph(amps_f1_v, amps_f1_v_verified, "F1", "Magnitude", "Voltage")
        # generate_graph(amps_ih1_v, amps_ih1_v_verified, "IH1", "Magnitude", "Voltage")
        # generate_graph(amps_ih2_v, amps_ih2_v_verified, "IH2", "Magnitude", "Voltage")
        # generate_graph(amps_f1_i, amps_f1_i_verified, "F1", "Magnitude", "Current")
        # generate_graph(amps_ih1_i, amps_ih1_i_verified, "IH1", "Magnitude", "Current")
        # generate_graph(amps_ih2_i, amps_ih2_i_verified, "IH2", "Magnitude", "Current")

        # generate_graph(angs_f1_v, angs_f1_v_verified, "F1", "Angle", "Voltage")
        # generate_graph(angs_ih1_v, angs_ih1_v_verified, "IH1", "Angle", "Voltage")
        # generate_graph(angs_ih2_v, angs_ih2_v_verified, "IH2", "Angle", "Voltage")
        # generate_graph(angs_f1_i, angs_f1_i_verified, "F1", "Angle", "Current")
        # generate_graph(angs_ih1_i, angs_ih1_i_verified, "IH1", "Angle", "Current")
        # generate_graph(angs_ih2_i, angs_ih2_i_verified, "IH2", "Angle", "Current")
        

    

        # #trying to get overall error 
        # print('magnitudes:')
        # print(mape(amps_f1_v, amps_f1_v_verified))
        # print(mape(amps_ih1_v, amps_ih1_v_verified))
        # print(mape(amps_ih2_v, amps_ih2_v_verified))

        # print(mape(amps_f1_i, amps_f1_i_verified))
        # print(mape(amps_ih1_i, amps_ih1_i_verified))
        # print(mape(amps_ih2_i, amps_ih2_i_verified))

        # print('angles:')
        # print(rmse_angle_deg(angs_f1_v, angs_f1_v_verified))
        # print(rmse_angle_deg(angs_ih1_v, angs_ih1_v_verified))
        # print(rmse_angle_deg(angs_ih2_v, angs_ih2_v_verified))

        # print(rmse_angle_deg(angs_f1_i, angs_f1_i_verified))
        # print(rmse_angle_deg(angs_ih1_i, angs_ih1_i_verified))
        # print(rmse_angle_deg(angs_ih2_i, angs_ih2_i_verified))

        sf1, sih1, sih2, pf1, pih1, pih2, qf1, qih1, qih2 = calculate_power(amps_f1_v, amps_f1_i, angs_f1_v, angs_f1_i, 
                                                            amps_ih1_v, amps_ih1_i, angs_ih1_v, angs_ih1_i,
                                                            amps_ih2_v, amps_ih2_i, angs_ih2_v, angs_ih2_i)

        #write_excel_power(s1, p1, sih1, pih1, sih2, pih2)
        
        # plt.figure()
        # x = np.arange(len(pih1))
        # width = 0.35
        # plt.bar(x - width/2, pih1, width, label='IH1')
        # plt.bar(x + width/2, pih2, width, label='IH2')
        # plt.legend()
        # plt.xlabel('Cycle')
        # plt.ylabel('Power')
        # plt.title('IH1 & IH2 Power')
        # plt.show()
        data_v = {}
        data_i = {}
        data_s = {}

        data_v['Time'] = times_output
        data_v['FVM'] = amps_f1_v
        data_v['IH1VM'] = amps_ih1_v
        data_v['IH2VM'] = amps_ih2_v
        data_v['FVA'] = angs_f1_v
        data_v['IH1VA'] = angs_ih1_v
        data_v['IH2VA'] = angs_ih2_v

        data_i['Time'] = times_output
        data_i['FIM'] = amps_f1_i
        data_i['IH1IM'] = amps_ih1_i
        data_i['IH2IM'] = amps_ih2_i
        data_i['FIA'] = angs_f1_i
        data_i['IH1IA'] = angs_ih1_i
        data_i['IH2IA'] = angs_ih2_i

        data_s['Time'] = times_output
        data_s['FS'] = sf1
        data_s['IH1S'] = sih1
        data_s['IH2S'] = sih2
        data_s['FP'] = pf1
        data_s['IH1P'] = pih1
        data_s['IH2P'] = pih2
        data_s['FQ'] = qf1
        data_s['IH1Q'] = qih1
        data_s['IH2Q'] = qih2


        output_v[locations[i]] = data_v
        output_i[locations[i]] = data_i
        output_s[locations[i]] = data_s
    
  
        
    write_output_excel(output_v, 'voltage_output.xlsx')
    write_output_excel(output_i, 'current_output.xlsx')
    write_output_excel(output_s, 'power_output.xlsx')








    

    










        
    
    


