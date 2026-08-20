import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import SegmentChart from './components/SegmentChart'
import FftChart from './components/FftChart'
import IhChart from './components/IhChart'
import LandingScreen from './components/LandingScreen'
import InfoButton from './components/InfoButton'

function Spinner() {
  return <div className="spinner" />
}

function App() {
  const [started, setStarted] = useState(false)
  const [upload, setUpload] = useState(null)
  const [downloadUrl, setDownloadUrl] = useState(null)
  const [timestamp, setTimestamp] = useState('middle')
  const [numSamples, setNumSamples] = useState(128)
  const [startTime, setStartTime] = useState(0)
  const [endTime, setEndTime] = useState(null)
  const [segmentData, setSegmentData] = useState(null)
  const [fftData, setFftData] = useState(null)
  const [ihData, setIhData] = useState(null)
  const [processing, setProcessing] = useState(false)
  const [activeTab, setActiveTab] = useState('detection')
  const [error, setError] = useState(null)


  // TODO: add error state when not number (for safari and othe browsers)
  // TODO: test what happens during exceptions

  const uploadData = async () => {
    if (!upload) {
      console.error('no input selected')
      return
    }

    setSegmentData(null)
    setFftData(null)
    setIhData(null)
    setProcessing(true)
    setActiveTab('detection')

    const ws = new WebSocket('wss://oscillation-source-locator-production.up.railway.app/ws/interharmonics')

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
        if (response.type === 'error') {
          setError(response.message) 
          setProcessing(false) 
        } else if (response.type === 'segment_chart') {
          setSegmentData(response.data)
        } else if (response.type === 'fft_chart') {
          setFftData(response.data)
          console.log('fft data received')
        } else if (response.type === 'ih_chart') {
          setIhData(response.data)
          setActiveTab('results')
        } else if (response.type === 'progress') {
          console.log('done' + response.location)
        }
        // binary data -- returned excel
      } else {
        const blob = new Blob([event.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
        const url = window.URL.createObjectURL(blob);
        setDownloadUrl(url)
        setProcessing(false)
      }
    }
  }

  return (!started ? (
            <LandingScreen onBegin={() => setStarted(true)} />
        ) : (
        <div className="app">
        <header className="app-header">
            {/* <div className="app-mark">IH</div> */}
            <div className="app-title-group">
            <h1 className="app-title">OSLocator</h1>
            <p className="app-subtitle">Upload a phasor dataset to detect the dominant oscillation and resolve its components.</p>
            </div>
        </header>

        <section className="panel">
            <h2 className="panel-title-centered">
                <span className="title-text">Input</span>
                <InfoButton title="File Requirements" hasError={!!error}>
                        Upload a .xlsx phasor export containing a Time column
                        followed by 5-column signal blocks (F, VM, VA, IM, IA) for each location. 
                        <br /><br />
                        <a href="/example_data.xlsx" download className="modal-link">
                            Download example file
                        </a>
                        
                </InfoButton>
            </h2>
     
            <div className="upload-zone">
            <input
                type="file"
                accept=".xlsx"
                onChange={e => { setUpload(e.target.files[0]); setError(null) }}
            />
            </div>
            {error && (
                <div className="error-banner">
                    <div className="error-banner-icon">!</div>
                    <p className="error-banner-text">{error} Please check guidelines for supported data structure. </p>
                </div>
            )}
        </section>

        <section className="panel">
            <h2 className="panel-title">Parameters</h2>
            <div className="param-grid">


                <div className="field">
                    <label className="field-label">Start time</label>
                    <input type="number" value={startTime} placeholder={'Default: 0'} onChange={e => { setStartTime(e.target.value) }} />
                </div>

                <div className="field">
                    <label className="field-label">End time</label>
                    <input type="number" value={endTime ?? ''} placeholder={'Default: None'} onChange={e => setEndTime(e.target.value)} />
                </div>

                <div className="field">
                    <label className="field-label">Timestamp anchor</label>
                    <select value={timestamp} onChange={e => setTimestamp(e.target.value)}>
                    <option value="start">Start</option>
                    <option value="middle">Middle</option>
                    <option value="end">End</option>
                    </select>
                </div>

                <div className="field">
                    <label className="field-label">Sampling rate</label>
                    <input type="number" value={numSamples} placeholder={'Default: 128'} onChange={e => { setNumSamples(e.target.value) }} />
                </div>

            </div>

            <div className="submit-row">
            <button className="submit-btn" onClick={() => { uploadData(); setDownloadUrl(null) }} disabled={!upload}>
                Submit Data
            </button>
            </div>
        </section>

        {processing || segmentData || fftData || ihData ? (
        <>
        <div className="tab-row">
            <button
            className={`tab-btn ${activeTab === 'detection' ? 'tab-btn-active' : ''}`}
            onClick={() => setActiveTab('detection')}
            >
            Detection
            </button>
            <button
            className={`tab-btn ${activeTab === 'results' ? 'tab-btn-active' : ''}`}
            onClick={() => setActiveTab('results')}
            disabled={!ihData && !processing}
            >
            Results
            </button>
        </div>

        {activeTab === 'detection' && (
            <div className="results-section">
            <div className="chart-panel">
                <h3 className="chart-panel-title">Strongest Oscillation Location</h3>
                {segmentData ? <SegmentChart segmentData={segmentData} /> : <div className="chart-loading"><Spinner /></div>}
            </div>

            <div className="chart-panel">
                <h3 className="chart-panel-title">FFT Spectrum </h3>
                {fftData ? <FftChart fftData={fftData} /> : <div className="chart-loading"><Spinner /></div>}
            </div>
            </div>
        )}

        {activeTab === 'results' && (
            <div className="results-section">
            <div className="chart-panel">
                <h3 className="chart-panel-title">Interharmonic Components</h3>
                {ihData ? <IhChart ihData={ihData} /> : <div className="chart-loading"><Spinner /></div>}
            </div>

            {downloadUrl && (
                <div className="download-row">
                <a className="download-link" href={downloadUrl} download="interharmonics_results.xlsx">
                    Download Detailed Results
                </a>
                </div>
            )}
            </div>
        )}
        </>
        ) : null}

        </div>
    ))
}

export default App