function ParametersInfo() {
  return (
    <>
      <strong>Start time / End time</strong> — restrict analysis to a specific
      window of the recording. Leave blank to use the whole file.
      <br /><br />

      <strong>Timestamp anchor</strong> — where in each phasor data point the
      reported timestamp falls: at the <em>start (0%) </em>, <em>middle (50%) </em>, or{' '}
      <em>end (100%)</em> of the sampling interval.
      <br /><br />

      <strong>Sampling rate</strong> — the number of samples taken to generate each phasor data point.
    </>
  )
}

export default ParametersInfo