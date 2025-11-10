
import React from 'react';

interface SummaryCardProps {
    icon: React.ReactNode;
    title: string;
    value: string;
    description: string;
}

const SummaryCard: React.FC<SummaryCardProps> = ({ icon, title, value, description }) => {
  return (
    <div className="bg-base-200 p-5 rounded-xl shadow-lg flex items-center space-x-4">
        <div className="flex-shrink-0">
            <div className="bg-base-300 p-3 rounded-full text-primary">
                {icon}
            </div>
        </div>
        <div>
            <p className="text-sm text-gray-400">{title}</p>
            <p className="text-2xl font-bold text-white">{value}</p>
            <p className="text-xs text-gray-500">{description}</p>
        </div>
    </div>
  );
};

export default SummaryCard;
