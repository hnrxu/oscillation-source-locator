import io
from fastapi import FastAPI, File, Form, UploadFile, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import numpy as np
import pandas as pd
from pydantic import BaseModel

from excel import read_excel, read_locations, validate_structure, write_output, write_output_excel
from solver import detect_max_fos, solve
from utils import calculate_power, convert_to_phasor, safe_convert
import config


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this later when you have your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def health():
    return { 'status': 'ok' }

# maybe rename? idk
@app.websocket('/ws/interharmonics')
async def generate_output(websocket: WebSocket):
    await websocket.accept() # waits for frontend to open conneciton

    try:

        params = await websocket.receive_json()
        contents = await websocket.receive_bytes()

        timestamp = params.get('timestamp', 'middle')
        num_samples = safe_convert(params.get('num_samples'), int, 128)
        start_time = safe_convert(params.get('start_time'), float, 0)
        end_time = safe_convert(params.get('end_time'), float, None)

        input_df = pd.read_excel(io.BytesIO(contents), header=None)
        validate_structure(input_df)


        m = (num_samples - 1) / 2
        if timestamp == 'start':
            m = 0
        elif timestamp == 'end':
            m = num_samples - 1


        output_v = {}
        output_i = {}
        output_s = {}
        locations = read_locations(input_df)

        cached_data = {}
        for i in range(len(locations)):
            start = i*5 + 1
            cached_data[i] = read_excel(input_df, start, start_time, end_time)


        # finding highest fos from all locations
        num_cycles, beat_period, best_mags, best_freqs, best_location = detect_max_fos(locations, cached_data)

        # send best oscillation segment to front
        best_index = locations.index(best_location)
        f1_freqs, phasor_mags_v, phasor_mags_i, phasor_angs_v, phasor_angs_i, times = cached_data[best_index]

        segment_data = {
            'time': times.tolist(),
            'voltage': phasor_mags_v.tolist(),
            'location': best_location
        }
        await websocket.send_json({'type': 'segment_chart', 'data': segment_data})
        fft_data = {
            'frequencies': best_freqs.tolist(),
            'magnitudes': best_mags.tolist(),
            'location': best_location,
            'fos': 1/beat_period
        }
        await websocket.send_json({'type': 'fft_chart', 'data': fft_data})




        for i in range(len(locations)):

            #parsing data
            start = i*5 + 1
            f1_freqs, phasor_mags_v, phasor_mags_i, phasor_angs_v, phasor_angs_i, times = cached_data[i]
            phasor_v = convert_to_phasor(phasor_mags_v, phasor_angs_v)
            phasor_i = convert_to_phasor(phasor_mags_i, phasor_angs_i)       

            assert len(phasor_v) == len(phasor_i), "Voltage and current phasor lengths don't match"

            #solve/get calculated data
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

                amplitudes_v, angles_v = solve(f1, f1/num_cycles, phasor_data, times_data, num_samples, m)

                amp_f1_v, amp_ih1_v, amp_ih2_v = amplitudes_v
                ang_f1_v, ang_ih1_v, ang_ih2_v = angles_v

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

                amplitudes_i, angles_i = solve(f1, f1/num_cycles, phasor_data, times_data, num_samples, m)
                
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
            
            sf1, sih1, sih2, pf1, pih1, pih2, qf1, qih1, qih2 = calculate_power(amps_f1_v, amps_f1_i, angs_f1_v, angs_f1_i, 
                                                                amps_ih1_v, amps_ih1_i, angs_ih1_v, angs_ih1_i,
                                                                amps_ih2_v, amps_ih2_i, angs_ih2_v, angs_ih2_i)
            


            data_v = {}
            data_i = {}
            data_s = {}

            data_v['Time'] = times_output
            data_v['FM'] = amps_f1_v
            data_v['IH1M'] = amps_ih1_v
            data_v['IH2M'] = amps_ih2_v
            data_v['FA'] = angs_f1_v
            data_v['IH1A'] = angs_ih1_v
            data_v['IH2A'] = angs_ih2_v

            data_i['Time'] = times_output
            data_i['FM'] = amps_f1_i
            data_i['IH1M'] = amps_ih1_i
            data_i['IH2M'] = amps_ih2_i
            data_i['FA'] = angs_f1_i
            data_i['IH1A'] = angs_ih1_i
            data_i['IH2A'] = angs_ih2_i

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

        
        # write_output_excel(output_v, 'voltage_output.xlsx')
        # write_output_excel(output_i, 'current_output.xlsx')
        # write_output_excel(output_s, 'power_output.xlsx')

        output_data = {
            'output_v': output_v,
            'output_i': output_i,
            'output_s': output_s
        }
        await websocket.send_json({'type': 'ih_chart', 'data': output_data})

        params_data = {
            'Start time': start_time,
            'End time': end_time,
            'Timestamp': timestamp,
            'Sampling rate': num_samples
        }
        output_final = write_output(output_v, output_i, output_s, params_data)
        await websocket.send_bytes(output_final.read())
   
   
    except ValueError as e:
        await websocket.send_json({'type': 'error', 'message': str(e)})
    except Exception as e:
        await websocket.send_json({'type': 'error', 'message': f'Unexpected error: {str(e)}'})
    finally:
        await websocket.close()



# uvicorn main:app --reload



            


