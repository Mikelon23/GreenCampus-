
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { SensorData } from '../types';

interface HistoryChartProps {
  data: SensorData[];
}

const CustomTooltip: React.FC<any> = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const date = new Date(label).toLocaleTimeString();
      return (
        <div className="bg-base-300 p-3 rounded-md border border-gray-700 shadow-lg">
          <p className="label text-gray-300">{`${date}`}</p>
          {payload.map((pld: any) => (
            <p key={pld.dataKey} style={{ color: pld.color }}>
              {`${pld.name}: ${pld.value.toFixed(1)} ${pld.unit}`}
            </p>
          ))}
        </div>
      );
    }
  
    return null;
};

const HistoryChart: React.FC<HistoryChartProps> = ({ data }) => {
  const chartData = data.map(d => ({...d, time: d.timestamp}));

  return (
    <div className="w-full h-96">
        <h3 className="text-lg font-semibold text-white mb-4">24-Hour Sensor Readings</h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis 
            dataKey="time"
            tickFormatter={(unixTime) => new Date(unixTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            stroke="#9ca3af"
            dy={10}
          />
          <YAxis yAxisId="left" stroke="#9ca3af" />
          <YAxis yAxisId="right" orientation="right" stroke="#9ca3af" />
          <Tooltip content={<CustomTooltip />} />
          <Legend wrapperStyle={{paddingTop: '20px'}} />
          <Line yAxisId="left" type="monotone" dataKey="temperature" name="Temp" unit="°C" stroke="#f87171" dot={false} strokeWidth={2} />
          <Line yAxisId="left" type="monotone" dataKey="humidity" name="Humidity" unit="%" stroke="#3b82f6" dot={false} strokeWidth={2} />
          <Line yAxisId="right" type="monotone" dataKey="co2" name="CO₂" unit="ppm" stroke="#fbbf24" dot={false} strokeWidth={2} />
          <Line yAxisId="right" type="monotone" dataKey="energy" name="Energy" unit="kWh" stroke="#a78bfa" dot={false} strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default HistoryChart;
