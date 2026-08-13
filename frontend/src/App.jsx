import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'

function App() {
  const [upload, setUpload] = useState(null)

  const uploadData = async () => {
    // call fetch and parse output here
  }

  return (
    <>
      <input
            type="file"
            accept=".xlsx"
            onChange={e => setUpload(e.target.files)}
        />
        <button onClick={uploadData}>
            Submit Data
        </button>
    </>
  )
}

export default App
