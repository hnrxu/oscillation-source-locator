import { useState } from 'react'
import './InfoModal.css'

function InfoButton({ title, children, hasError = false }) {
  const [open, setOpen] = useState(false)

  return (
    <>
      <button
        className={`info-btn ${hasError ? 'info-btn-error' : ''}`}
        onClick={() => setOpen(true)}
      >
        i
      </button>

      {open && (
        <div className="modal-overlay" onClick={() => setOpen(false)}>
          <div className="modal-panel" onClick={e => e.stopPropagation()}>
            <p className="modal-title">{title}</p>
            <p className="modal-body">{children}</p>
            <button className="modal-close" onClick={() => setOpen(false)}>Close</button>
          </div>
        </div>
      )}
    </>
  )
}

export default InfoButton