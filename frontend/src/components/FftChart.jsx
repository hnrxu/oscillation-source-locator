import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

function FftChart({ fftData }) {
  if (!fftData) return null

  
  const fosIndex = fftData.frequencies.findIndex(i => 
    Math.abs(i - fftData.fos) < 0.01
  )
  console.log(fosIndex)
  const BIN_LIMIT = fosIndex + 5
  const chartData = fftData.frequencies.map((freq, i) => ({
    frequency: freq.toFixed(2),
    magnitude: fftData.magnitudes[i].toFixed(2)
  })).filter(i => i.frequency >= 0.1).slice(0, BIN_LIMIT)


  // avoid a wall of unreadable x-axis labels when there are many bins
  const tickInterval = Math.max(0, Math.floor(chartData.length / 12) - 1)

  return (
    <div>
      <h3
        style={{
          fontFamily: 'var(--mono)',
          fontSize: '13px',
          fontWeight: 500,
          color: 'var(--text)',
          margin: '0 0 2px',
        }}
      >
        Location: {fftData.location}
      </h3>
      <p
        style={{
          fontFamily: 'var(--mono)',
          fontSize: '13px',
          color: 'var(--signature)',
          margin: '0 0 0px',
          fontWeight: 500,
        }}
      >
        fos ≈ {fftData.fos.toFixed(3)} Hz
      </p>

      <ResponsiveContainer width="100%" height={170}>
        <BarChart data={chartData} margin={{ top: 8, right: 16, bottom: 28, left: 16 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
          <XAxis
            dataKey="frequency"
            interval={tickInterval}
            tick={{ fill: 'var(--text-faint)', fontSize: 11, fontFamily: 'var(--mono)' }}
            axisLine={{ stroke: 'var(--border-strong)' }}
            tickLine={{ stroke: 'var(--border-strong)' }}
            label={{
              value: 'Frequency (Hz)',
              position: 'insideBottom',
              offset: -15,
              fill: 'var(--text-faint)',
              fontSize: 11,
            }}
          />
          <YAxis
            tick={{ fill: 'var(--text-faint)', fontSize: 11, fontFamily: 'var(--mono)' }}
            axisLine={{ stroke: 'var(--border-strong)' }}
            tickLine={{ stroke: 'var(--border-strong)' }}
            domain={['dataMin', 'dataMax']}
            width={44}
            label={{
              value: 'Magnitude (%)',
              angle: -90,
              position: 'insideLeft',
              fill: 'var(--text-faint)',
              fontSize: 11,
              offset: -10,
            }}
          />
          <Tooltip
            cursor={{ fill: 'var(--surface-raised)' }}
            contentStyle={{
              background: 'var(--surface-raised)',
              border: '1px solid var(--border-strong)',
              borderRadius: 4,
              fontFamily: 'var(--mono)',
              fontSize: 12,
            }}
            labelStyle={{ color: 'var(--text-dim)' }}
            itemStyle={{ color: 'var(--text)' }}
          />
          <Bar dataKey="magnitude" fill="var(--accent-strong)" radius={[2, 2, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export default FftChart