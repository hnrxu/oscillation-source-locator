function ParametersInfo() {
  return (
    <>
      <strong>Start time / End time</strong> — restrict analysis to a specific
      window of the recording. Leave End time blank to use the rest of the file.
      <br /><br />

      <strong>Timestamp anchor</strong> — where in each sample window the
      reported timestamp falls: at the <em>start</em>, <em>middle</em>, or{' '}
      <em>end</em> of the sampling interval. This depends on your PMU or data
      source's convention — if results look off, try a different setting.
      <br /><br />

      <strong>Sampling rate</strong> — the number of samples per power cycle
      in your data. This should match how the file was originally recorded;
      an incorrect value can noticeably affect the interharmonic results.
    </>
  )
}

export default ParametersInfo