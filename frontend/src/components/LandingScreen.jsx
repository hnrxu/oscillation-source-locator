import './LandingScreen.css'

function LandingScreen({ onBegin }) {
  return (
    <div className="landing">

      <h1 className="landing-headline">
        OSLocator
      </h1>

      <p className="landing-sub">
        Version 1.0
      </p>

      <div className="landing-signature">
        <svg viewBox="0 0 800 140" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M 0 70 
               C 40 20, 80 20, 120 70 
               C 160 120, 200 120, 240 70
               C 280 20, 320 20, 360 70
               C 400 120, 440 120, 480 70
               C 520 20, 560 20, 600 70
               C 640 120, 680 120, 720 70
               C 750 40, 780 40, 800 70"
            fill="none"
            stroke="var(--border-strong)"
            strokeWidth="1"
          />
          <path
            d="M 0 70 
               Q 15 40 30 70 T 60 70 T 90 70 T 120 70 T 150 70 T 180 70 T 210 70 T 240 70
               T 270 70 T 300 70 T 330 70 T 360 70 T 390 70 T 420 70 T 450 70 T 480 70
               T 510 70 T 540 70 T 570 70 T 600 70 T 630 70 T 660 70 T 690 70 T 720 70
               T 750 70 T 780 70 T 800 70"
            fill="none"
            stroke="var(--accent-strong)"
            strokeWidth="1.5"
          />
        </svg>
        {/* <div className="landing-signature-caption">
          <span>Combined signal, F1 ± fos</span>
          <span>Beat period resolved</span>
        </div> */}
      </div>

      {/* <div className="landing-features">
        <div className="landing-feature">
          <p className="landing-feature-label">Automatic Detection</p>
          <p className="landing-feature-body">
            Scans every location in the dataset and locks onto the strongest
            genuine oscillation, filtering out transients.
          </p>
        </div>
        <div className="landing-feature">
          <p className="landing-feature-label">Per-Location Breakdown</p>
          <p className="landing-feature-body">
            View F1, IH1, and IH2 magnitude, angle, and power for any location
            in the network, side by side.
          </p>
        </div>
        <div className="landing-feature">
          <p className="landing-feature-label">Exportable Results</p>
          <p className="landing-feature-body">
            Download the full voltage, current, and power breakdown as a
            multi-sheet workbook.
          </p>
        </div>
      </div> */}

      <div className="landing-cta-row">
        <button className="landing-cta" onClick={onBegin}>
          Begin Analysis
        </button>
      </div>
    </div>
  )
}

export default LandingScreen