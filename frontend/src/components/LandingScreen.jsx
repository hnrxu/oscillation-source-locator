import './LandingScreen.css'

function LandingScreen({ onBegin }) {
  return (
    <div className="landing">
        

      <h1 className="landing-headline">OSLocator</h1>

      <p className="landing-tagline">
        Power system oscillation source locator using interharmonics extracted from synchrophasor data
      </p>

      <div className="landing-meta">
        <span>Version 1.0</span>
        <span>Aug. 20, 2026</span>
        <span>Copyright © Sophia Xu</span>
      </div>

      {/* <div className="landing-signature">
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
      </div> */}

      <div className="landing-cta-row">
        <button className="landing-cta" >
          About OSLocator
        </button>
        <button className="landing-cta" onClick={onBegin}>
          Begin Analysis
        </button>
      </div>
    </div>
  )
}

export default LandingScreen