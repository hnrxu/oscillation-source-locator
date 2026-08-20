import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { useState } from 'react'
// TODO: add units on axes esp angle degrees
const selectStyle = {
  fontFamily: 'var(--mono)',
  fontSize: '13px',
  color: 'var(--text)',
  background: 'var(--surface-raised)',
  border: '1px solid var(--border)',
  borderRadius: '4px',
  padding: '8px 10px',
  outline: 'none',
  width: '100%',
}

const controlLabelStyle = {
  fontFamily: 'var(--mono)',
  fontSize: '11px',
  letterSpacing: '0.03em',
  textTransform: 'uppercase',
  color: 'var(--accent)',
  marginBottom: '6px',
  marginTop: '6px',
  display: 'block',
  fontWeight: 450,
}

function IhChart({ ihData }) {
  const [signal, setSignal] = useState('Voltage')
  const [location, setLocation] = useState('')
  const [component, setComponent] = useState('IH1')
  const [dataType, setDataType] = useState('Magnitude')

  if (!ihData) return null

  const locations = ihData ? Object.keys(ihData.output_v) : []

  const currentLocation = location || locations[0]

  const getChartData = () => {
    const outputKey = signal === 'Voltage' ? 'output_v'
      : signal === 'Current' ? 'output_i'
        : 'output_s'
    const locationData = ihData[outputKey]?.[currentLocation]
    if (!locationData) return []

    // build the field key, e.g. "FM", "IH1A", "IH2P"
    let suffix
    if (signal === 'Power') {
      suffix = dataType.toUpperCase()   // 'p' -> 'P', 's' -> 'S', 'q' -> 'Q' // prob change later
    } else {
      suffix = dataType === 'Magnitude' ? 'M' : 'A'
    }
    const fieldKey = component === 'F1' ? `F${suffix}` : `${component}${suffix}`
    const values = locationData[fieldKey]
    const times = locationData['Time']

    return times.map((t, i) => ({ time: t.toFixed(2), value: values[i].toFixed(2) }))
  }

  const chartData = getChartData()

  const signalChange = (value) => {
    const wasVoltageOrCurrent = signal === 'Voltage' || signal === 'Current'
    const isNowVoltageOrCurrent = value === 'Voltage' || value === 'Current'

    if (wasVoltageOrCurrent !== isNowVoltageOrCurrent) {
      setDataType(isNowVoltageOrCurrent ? 'Magnitude' : 'p')
    }

    setSignal(value)
  }

  // avoid a wall of unreadable x-axis labels when there are many bins
  const tickInterval = Math.max(0, Math.floor(chartData.length / 12) - 1)

  return (
    <div>
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
          gap: '14px',
          marginBottom: '22px',
          paddingBottom: '18px',
          borderBottom: '1px solid var(--border)',
        }}
      >
        <div>
          <label style={controlLabelStyle}>Signal</label>
          <select style={selectStyle} value={signal} onChange={e => signalChange(e.target.value)}>
            <option value="Voltage">Voltage</option>
            <option value="Current">Current</option>
            <option value="Power">Power</option>
          </select>
        </div>

        <div>
          <label style={controlLabelStyle}>Location</label>
          <select style={selectStyle} value={currentLocation} onChange={e => setLocation(e.target.value)}>
            {locations.map((l) => (
              <option key={l} value={l}>{l}</option>
            ))}
          </select>
        </div>

        <div>
          <label style={controlLabelStyle}>Component</label>
          <select style={selectStyle} value={component} onChange={e => setComponent(e.target.value)}>
            <option value="F1">F1</option>
            <option value="IH1">IH1</option>
            <option value="IH2">IH2</option>
          </select>
        </div>

        {(signal === 'Voltage' || signal === 'Current') && (
          <div>
            <label style={controlLabelStyle}>Data type</label>
            <select style={selectStyle} value={dataType} onChange={e => setDataType(e.target.value)}>
              <option value="Magnitude">Magnitude</option>
              <option value="Angle">Angle</option>
            </select>
          </div>
        )}

        {signal === 'Power' && (
          <div>
            <label style={controlLabelStyle}>Data type</label>
            <select style={selectStyle} value={dataType} onChange={e => setDataType(e.target.value)}>
              <option value="p">P</option>
              <option value="s">S</option>
              <option value="q">Q</option>
            </select>
          </div>
        )}
      </div>

      <ResponsiveContainer width="100%" height={340}>
        <LineChart data={chartData} margin={{ top: 8, right: 16, bottom: 28, left: 8 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
          <XAxis
            dataKey="time"
            tick={{ fill: 'var(--text-faint)', fontSize: 11, fontFamily: 'var(--mono)' }}
            interval={tickInterval}
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
              value: dataType,
              angle: -90,
              position: 'insideLeft',
              fill: 'var(--text-faint)',
              fontSize: 11,
              offset: -5,
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
            dataKey="value"
            stroke="var(--accent-strong)"
            dot={false}
            strokeWidth={1.5}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default IhChart