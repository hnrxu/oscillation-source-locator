import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

function SegmentChart({ segmentData }) {
  if (!segmentData) return null

  const chartData = segmentData.time.map((t, i) => ({
    time: t,
    voltage: segmentData.voltage[i]
  }))

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis 
          dataKey="time" 
          label={{ value: 'Time (s)', position: 'insideBottom', offset: -5 }} 
        />
        <YAxis 
          label={{ value: 'Voltage', angle: -90, position: 'insideLeft' }} 
        />
        <Tooltip />
        <Line 
          type="monotone" 
          dataKey="voltage" 
          stroke="#2563eb" 
          dot={false} 
          strokeWidth={1.5}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}

export default SegmentChart