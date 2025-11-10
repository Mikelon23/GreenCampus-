
import React from 'react';

interface MetricCardProps {
  label: string;
  value: string;
  unit: string;
  icon: React.ReactNode;
  thresholds: { warn: number; danger: number };
  currentValue?: number;
}

const MetricCard: React.FC<MetricCardProps> = ({ label, value, unit, icon, thresholds, currentValue }) => {
  
  const getStatusColor = () => {
    if (currentValue === undefined) return 'bg-gray-500';
    if (currentValue >= thresholds.danger) return 'bg-danger';
    if (currentValue >= thresholds.warn) return 'bg-secondary';
    return 'bg-primary';
  };

  const statusColor = getStatusColor();

  return (
    <div className="bg-base-200 p-4 sm:p-6 rounded-xl shadow-lg flex flex-col justify-between transition-transform duration-300 hover:scale-105">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="text-primary">{icon}</div>
          <span className="text-gray-300 font-medium">{label}</span>
        </div>
        <div className={`w-3 h-3 rounded-full ${statusColor} animate-pulse`}></div>
      </div>
      <div className="text-center mt-4">
        <span className="text-4xl lg:text-5xl font-bold text-white">{value}</span>
        <span className="text-lg text-gray-400 ml-1">{unit}</span>
      </div>
    </div>
  );
};

export default MetricCard;
