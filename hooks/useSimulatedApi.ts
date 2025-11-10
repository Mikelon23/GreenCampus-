
import { useState, useEffect, useCallback } from 'react';
import { SensorData } from '../types';

const DATA_POINTS_24H = (24 * 60 * 60) / 5; // 17280 points for updates every 5 seconds

// Function to generate a single realistic data point
const generateDataPoint = (lastData?: SensorData): SensorData => {
  const newTimestamp = Date.now();
  
  const randomFactor = (value: number, variation: number) => {
    return value + (Math.random() - 0.5) * variation;
  };

  if (lastData) {
    return {
      timestamp: newTimestamp,
      temperature: Math.max(18, Math.min(32, randomFactor(lastData.temperature, 0.2))),
      humidity: Math.max(30, Math.min(75, randomFactor(lastData.humidity, 0.5))),
      co2: Math.max(400, Math.min(1200, randomFactor(lastData.co2, 10))),
      energy: Math.max(80, Math.min(220, randomFactor(lastData.energy, 2))),
    };
  }

  // Initial values
  return {
    timestamp: newTimestamp,
    temperature: 22.5,
    humidity: 45.0,
    co2: 600,
    energy: 120.0,
  };
};

export const useSimulatedApi = (isUserLoggedIn: boolean) => {
  const [latestData, setLatestData] = useState<SensorData | null>(null);
  const [historicalData, setHistoricalData] = useState<SensorData[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Initialize data on mount if user is logged in
  useEffect(() => {
    if (!isUserLoggedIn) {
        setIsLoading(false);
        return;
    };
    
    setIsLoading(true);
    const initialHistory: SensorData[] = [];
    let lastPoint = generateDataPoint();
    initialHistory.push(lastPoint);

    for (let i = 0; i < 288; i++) { // Approx 24 hours of data at 5 min intervals for initial load
      const newPoint = generateDataPoint(lastPoint);
      newPoint.timestamp = lastPoint.timestamp - 5 * 60 * 1000; // Go back in time
      initialHistory.unshift(newPoint);
      lastPoint = newPoint;
    }

    setHistoricalData(initialHistory);
    setLatestData(initialHistory[initialHistory.length - 1]);
    setIsLoading(false);
  }, [isUserLoggedIn]);

  // Update data every 5 seconds if user is logged in
  useEffect(() => {
    if (!isUserLoggedIn) return;

    const intervalId = setInterval(() => {
      setLatestData(prevLatest => {
        const newDataPoint = generateDataPoint(prevLatest ?? undefined);
        setHistoricalData(prevData => {
            const updatedData = [...prevData, newDataPoint];
            // Keep history to a manageable size (approx. 24 hours)
            if (updatedData.length > DATA_POINTS_24H) {
            return updatedData.slice(updatedData.length - DATA_POINTS_24H);
            }
            return updatedData;
        });
        return newDataPoint;
      });
    }, 5000);

    return () => clearInterval(intervalId);
  }, [isUserLoggedIn]);

  return { latestData, historicalData, isLoading };
};
