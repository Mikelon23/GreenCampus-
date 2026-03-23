import { useMemo, useCallback } from "react";
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import Layout from "../components/Layout";
import SectionHeader from "../components/SectionHeader";
import StatCard from "../components/StatCard";
import useSensorData from "../hooks/useSensorData";
import { api, type SensorData, type SustainabilityScore } from "../services/api";
import useFetch from "../hooks/useFetch";

export default function DashboardPage() {
  const { data: sensors, loading: sensorsLoading } = useSensorData();
  const sustainabilityFetcher = useCallback(() => api.getSustainability(), []);
  const sustainability = useFetch<SustainabilityScore[]>(sustainabilityFetcher, 30_000);

  const stats = useMemo(() => {
    if (!sensors || sensors.length === 0) {
      return {
        temperature: "--",
        humidity: "--",
        co2: "--",
        energy: "--"
      };
    }
    const total = sensors.reduce(
      (acc: { t: number; h: number; c: number; e: number }, item: SensorData) => {
        acc.t += item.temperature;
        acc.h += item.humidity;
        acc.c += item.co2_level;
        acc.e += item.energy_usage;
        return acc;
      },
      { t: 0, h: 0, c: 0, e: 0 }
    );
    const count = sensors.length;
    return {
      temperature: `${(total.t / count).toFixed(1)}°C`,
      humidity: `${(total.h / count).toFixed(1)}%`,
      co2: `${(total.c / count).toFixed(0)} ppm`,
      energy: `${(total.e / count).toFixed(0)} kWh`
    };
  }, [sensors]);

  const chartData = useMemo(() => {
    if (!sensors) {
      return [];
    }
    return [...sensors]
      .slice(0, 12)
      .reverse()
      .map((item: SensorData) => ({
        time: new Date(item.timestamp).toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit"
        }),
        temperature: item.temperature,
        energy: item.energy_usage
      }));
  }, [sensors]);

  return (
    <Layout>
      <div className="grid gap-6 lg:grid-cols-4">
        <StatCard title="Avg Temperature" value={stats.temperature} subtitle="Last 24h" />
        <StatCard title="Avg Humidity" value={stats.humidity} subtitle="Campus wide" />
        <StatCard title="Avg CO₂" value={stats.co2} subtitle="Indoor air quality" />
        <StatCard title="Avg Energy" value={stats.energy} subtitle="Building usage" />
      </div>

      <div className="mt-10 grid gap-8 lg:grid-cols-3">
        <div className="lg:col-span-2 rounded-3xl bg-white/90 p-6 shadow-sm">
          <SectionHeader
            title="Environmental Trends"
            subtitle="Recent sensor readings across campus zones"
          />
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="temp" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3e856a" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#3e856a" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#d9e7df" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Area
                  type="monotone"
                  dataKey="temperature"
                  stroke="#3e856a"
                  fillOpacity={1}
                  fill="url(#temp)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          {sensorsLoading ? (
            <p className="mt-4 text-sm text-campus-500">Loading sensor data...</p>
          ) : null}
        </div>
        <div className="rounded-3xl bg-white/90 p-6 shadow-sm">
          <SectionHeader title="Sustainability Scores" subtitle="Zone performance index" />
          {sustainability.loading ? (
            <p className="text-sm text-campus-500">Calculating scores...</p>
          ) : (
            <div className="space-y-4">
              {(sustainability.data || []).map((score) => (
                <div key={score.zone_id} className="rounded-2xl bg-campus-50 p-4">
                  <p className="text-sm text-campus-600">Zone {score.zone_id}</p>
                  <p className="font-display text-2xl text-campus-800">
                    {score.sustainability_score.toFixed(1)}
                  </p>
                  <p className="text-xs text-campus-500">
                    Energy {score.energy_efficiency_index.toFixed(0)} | Carbon{" "}
                    {score.carbon_index.toFixed(0)}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}
