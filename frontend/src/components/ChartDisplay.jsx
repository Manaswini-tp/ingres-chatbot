import React from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a'];

const ChartDisplay = ({ chartData }) => {
  if (!chartData || !chartData.type) {
    console.log('No chart data received');
    return null;
  }

  console.log('Chart data:', chartData); // Debug log

  const { type, data } = chartData;

  if (type === 'rainfall') {
    return (
      <div className="chart-container">
        <h4>📊 Rainfall Distribution (mm)</h4>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="district" angle={-45} textAnchor="end" height={100} />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="rainfall" fill="#667eea" name="Rainfall (mm)" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    );
  }

  if (type === 'extraction') {
    return (
      <div className="chart-container">
        <h4>📊 Groundwater Extraction Stage (%)</h4>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="district" angle={-45} textAnchor="end" height={100} />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="extraction" stroke="#764ba2" strokeWidth={3} name="Extraction (%)" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    );
  }

  if (type === 'comparison') {
    return (
      <div className="chart-container">
        <h4>📊 Comparison Analysis</h4>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis yAxisId="left" orientation="left" stroke="#667eea" />
            <YAxis yAxisId="right" orientation="right" stroke="#764ba2" />
            <Tooltip />
            <Legend />
            <Bar yAxisId="left" dataKey="rainfall" fill="#667eea" name="Rainfall (mm)" />
            <Bar yAxisId="right" dataKey="extraction" fill="#764ba2" name="Extraction (%)" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    );
  }

  if (type === 'state_overview') {
    return (
      <div className="chart-container">
        <h4>📊 State Overview</h4>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, value }) => `${name}: ${value.toFixed(2)}`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    );
  }

  return null;
};

export default ChartDisplay;
