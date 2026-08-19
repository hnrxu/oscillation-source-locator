import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

function SegmentChart({ segmentData }) {
  if (!segmentData) return null

  const chartData = segmentData.time.map((t, i) => ({
    time: t.toFixed(2),
    voltage: segmentData.voltage[i].toFixed(2)
  }))

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
          margin: '0 0 10px',
        }}
      >
        Location: {segmentData.location}
      </h3>
    <ResponsiveContainer width="100%" height={170}>
      <LineChart data={chartData} margin={{ top: 8, right: 16, bottom: 28, left: 16 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
        <XAxis
          dataKey="time"
          interval={tickInterval}
          tick={{ fill: 'var(--text-faint)', fontSize: 11, fontFamily: 'var(--mono)' }}
          axisLine={{ stroke: 'var(--border-strong)' }}
          tickLine={{ stroke: 'var(--border-strong)' }}
          label={{
            value: 'Time (s)',
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
            value: 'Voltage',
            angle: -90,
            position: 'insideLeft',
            fill: 'var(--text-faint)',
            fontSize: 11,
            offset: -10,
          }}
        />
        <Tooltip
          cursor={{ stroke: 'var(--border-strong)' }}
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
        <Line
          type="monotone"
          dataKey="voltage"
          stroke="var(--accent-strong)"
          dot={false}
          strokeWidth={1.5}
        />
      </LineChart>
    </ResponsiveContainer>
    </div>
  )
}

export default SegmentChart