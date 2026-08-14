import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

function FftChart({ fftData }) {
    if (!fftData) return null

    const chartData = fftData.frequencies.map((freq, i) => ({
        frequencies: freq,
        magnitudes: fftData.magnitudes[i]
    }))

    return (
        <>
        <h3>FFT — {fftData.location} (fos ≈ {fftData.fos.toFixed(3)} Hz)</h3>
        <ResponsiveContainer width="100%" height={400}>
            <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
                dataKey="frequencies"
                label={{ value: 'Frequency (Hz)', position: 'insideBottom', offset: -5 }}
            />
            <YAxis
                label={{ value: 'Magnitude', angle: -90, position: 'insideLeft' }}
            />
            <Tooltip />
            <Bar dataKey="magnitudes" fill="#2563eb" />
            </BarChart>
        </ResponsiveContainer>
        </>
    )
    }

export default FftChart