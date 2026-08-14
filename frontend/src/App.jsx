import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import SegmentChart from './components/SegmentChart'
import FftChart from './components/FftChart'
import IhChart from './components/IhChart'

function App() {
    const [upload, setUpload] = useState(null)
    const [downloadUrl, setDownloadUrl] = useState(null)
    const [timestamp, setTimestamp] = useState('middle')
    const [numSamples, setNumSamples] = useState(128)
    const [startTime, setStartTime] = useState(0)
    const [endTime, setEndTime] = useState(null)
    const [segmentData, setSegmentData] = useState(null)
    const [fftData, setFftData] = useState(null)
    const [ihData, setIhData] = useState(null)

  // TODO: add error state when not number (for safari and othe browsers)


    

    const uploadData = async () => {
        if (!upload) {
            console.error('no input selected')
            return
        }

        const ws = new WebSocket('ws://localhost:8000/ws/interharmonics')

        ws.onopen = () => {
            // send params
            ws.send(JSON.stringify({
                timestamp, num_samples: numSamples, start_time: startTime, end_time: endTime
            }))
            // sned input file
            upload.arrayBuffer().then(buffer => ws.send(buffer))
        }

        ws.onmessage = (event) => {
            if (typeof event.data === 'string') {
                const response = JSON.parse(event.data)
                if (response.type === 'segment_chart') {
                    setSegmentData(response.data)  
                } else if (response.type === 'fft_chart') {
                    setFftData(response.data)  
                } else if (response.type === 'ih_chart') {
                    setIhData(response.data)  
            }
            
            // binary data -- returned excel
            } else {
                const blob = new Blob([event.data], {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'})
                const url = window.URL.createObjectURL(blob);
                setDownloadUrl(url)
            }
        }

        
        



    }

    return (
    <>
        <input
            type="file"
            accept=".xlsx"
            onChange={e => {setUpload(e.target.files[0])}}
        />
        

        <select value={timestamp} onChange={e => setTimestamp(e.target.value)}>
            <option value="start">Start</option>
            <option value="middle">Middle</option>
            <option value="end">End</option>
        </select>

        <input type="number" value={numSamples} placeholder={'Default: 128'} onChange={e => {setNumSamples(e.target.value)}}/>
        <input type="number" value={startTime} placeholder={'Default: 0'} onChange={e => {setStartTime(e.target.value)}}/>
        <input type="number" value={endTime ?? ''} placeholder={'Default: None'} onChange={e => setEndTime(e.target.value)} />

        <button onClick={() => {uploadData(); setDownloadUrl(null)}}>
            Submit Data
        </button>

        {segmentData && <SegmentChart segmentData={segmentData} />}
        {fftData && <FftChart fftData={fftData} />}
        {ihData && <IhChart ihData={ihData} />}

        {downloadUrl && (
            <a href={downloadUrl} download="interharmonics_results.xlsx">
                Download Results
            </a>
        )} 

        
    </>
  )
}

export default App
