import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

function IhChart({ ihData }) {
    const [signal, setSignal] = useState('voltage')
    const [location, setLocation] = useState('')
    const [component, setComponent] = useState('IH1')
    const [dataType, setDataType] = useState('magnitude')

    if (!ihData) return null

    const locations = ihData ? Object.keys(ihData.output_v) : []

    const currentLocation = location || locations[0]

    
    const getChartData = () => {
        const outputKey = signal === 'voltage' ? 'output_v' 
                            : signal === 'current' ? 'output_i' 
                            : 'output_s'
        
        const locationData = ihData[outputKey]?.[currentLocation]
        if (!locationData) return []

        // build the field key, e.g. "FM", "IH1A", "IH2P"
        let suffix
            if (signal === 'power') {
                suffix = dataType.toUpperCase()   // 'p' -> 'P', 's' -> 'S', 'q' -> 'Q' // prob change later
            } else {
                suffix = dataType === 'magnitude' ? 'M' : 'A'
            }
        
        const fieldKey = component === 'F1' ? `F${suffix}` : `${component}${suffix}`
        const values = locationData[fieldKey]
        const times = locationData['Time']

        return times.map((t, i) => ({ time: t, value: values[i] }))
    }

    const chartData = getChartData()



    const signalChange = (value) => {
        const wasVoltageOrCurrent = signal === 'voltage' || signal === 'current'
        const isNowVoltageOrCurrent = value === 'voltage' || value === 'current'

        if (wasVoltageOrCurrent !== isNowVoltageOrCurrent) {
            setDataType(isNowVoltageOrCurrent ? 'magnitude' : 'p')
        }

        setSignal(value)

    }

   


    return (
        <>
        <select value={signal} onChange={e => signalChange(e.target.value)}>
            <option value="voltage">Voltage</option>
            <option value="current">Current</option>
            <option value="power">Power</option>
        </select>

        <select value={currentLocation} onChange={e => setLocation(e.target.value)}>
            {locations.map((l) => (
                <option key={l} value={l}> {l} </option>
            ))}
        </select>

        <select value={component} onChange={e => setComponent(e.target.value)}>
            <option value="F1">F1</option>
            <option value="IH1">IH1</option>
            <option value="IH2">IH2</option>
        </select>

        {(signal === 'voltage' || signal === 'current') && <select value={dataType} onChange={e => setDataType(e.target.value)}>
            <option value="magnitude">Magnitude</option>
            <option value="angle">Angle</option>
        </select>}

        {signal === 'power' && <select value={dataType} onChange={e => setDataType(e.target.value)}>
            <option value="p">p</option>
            <option value="s">s</option>
            <option value="q">q</option>
        </select>}


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
                dataKey="value" 
                stroke="#2563eb" 
                dot={false} 
                strokeWidth={1.5}
            />
            </LineChart>
        </ResponsiveContainer>

        </>
        
    )
}

export default IhChart