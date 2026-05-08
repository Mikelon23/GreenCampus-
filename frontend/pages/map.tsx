import dynamic from "next/dynamic";
import { useEffect, useMemo, useState } from "react";
import Layout from "../components/Layout";
import SectionHeader from "../components/SectionHeader";
import { useAuth } from "../contexts/AuthContext";
import { api } from "../services/api";
import type { MapSensor, MapZone, SmartBin } from "../components/CampusLeafletMap";

const CampusLeafletMap = dynamic(() => import("../components/CampusLeafletMap"), {
  ssr: false,
  loading: () => (
    <div className="flex h-full items-center justify-center text-sm text-campus-500">
      Loading interactive map...
    </div>
  )
});

const SMART_BINS: SmartBin[] = [
  { id: 1, name: "Smart Bin - Library", position: [-0.20945, -78.48945] },
  { id: 2, name: "Smart Bin - Main Patio", position: [-0.2106, -78.49055] },
  { id: 3, name: "Smart Bin - Lab Hall", position: [-0.2111, -78.48985] }
];

const recyclingActions = {
  plastic: "smart recycling plastic",
  paper: "smart recycling paper",
  glass: "smart recycling glass"
};

export default function MapPage() {
  const { user, loading: authLoading } = useAuth();
  const [zones, setZones] = useState<MapZone[]>([]);
  const [sensors, setSensors] = useState<MapSensor[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [recyclingBusy, setRecyclingBusy] = useState<"plastic" | "paper" | "glass" | null>(null);
  const [rewardMessage, setRewardMessage] = useState("");

  const load = async () => {
    try {
      setError("");
      setLoading(true);
      const [zonesData, sensorsData] = await Promise.all([
        api.getZones(),
        api.getSensors("")
      ]);
      setZones(zonesData as MapZone[]);
      setSensors(sensorsData as MapSensor[]);
    } catch (err: any) {
      setError(err.message || "Failed to load map data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!authLoading) {
      load();
    }
  }, [authLoading]);

  const zoneMetrics = useMemo(() => {
    const metrics: Record<number, MapSensor> = {};
    sensors.forEach((sensor) => {
      if (!metrics[sensor.zone_id]) {
        metrics[sensor.zone_id] = sensor;
      }
    });
    return metrics;
  }, [sensors]);

  const handleRecycle = async (material: "plastic" | "paper" | "glass") => {
    if (!user) {
      setRewardMessage("");
      setError("Sign in to earn Green Points for recycling.");
      return;
    }

    setRecyclingBusy(material);
    setError("");
    setRewardMessage("");
    try {
      // Major change: simulated Smart Bin events become normal eco-actions, so Eco-Forest receives energy drops.
      const action = await api.logAction({
        user_id: user.id,
        action_type: recyclingActions[material]
      });
      setRewardMessage(`Recycling registered: +${action.points_awarded} Green Points.`);
    } catch (err: any) {
      setError(err.message || "Failed to register recycling action.");
    } finally {
      setRecyclingBusy(null);
    }
  };

  if (authLoading) return null;

  return (
    <Layout>
      <SectionHeader
        title="Campus Sustainability Map"
        subtitle="Live environmental ESP32 sensors and simulated smart recycling bins."
      />
      {error ? <div className="mb-6 rounded-2xl bg-red-50 p-4 text-sm text-red-700">{error}</div> : null}
      {rewardMessage ? (
        <div className="mb-6 rounded-2xl bg-emerald-50 p-4 text-sm text-emerald-800">{rewardMessage}</div>
      ) : null}

      <div className="grid gap-6 xl:grid-cols-[1.4fr_0.6fr]">
        <div className="h-[620px] overflow-hidden rounded-3xl bg-white/90 shadow-sm">
          {loading ? (
            <div className="flex h-full items-center justify-center text-sm text-campus-500">Loading zones...</div>
          ) : (
            <CampusLeafletMap
              zones={zones}
              zoneMetrics={zoneMetrics}
              smartBins={SMART_BINS}
              userSignedIn={!!user}
              recyclingBusy={recyclingBusy}
              onRecycle={handleRecycle}
            />
          )}
        </div>

        <div className="space-y-6">
          {/* Plant a Tree form intentionally hidden per mentor UI cleanup request. */}
          <div className="rounded-3xl bg-white/90 p-6 shadow-sm">
            <SectionHeader title="Map Layers" subtitle="Sensor and recycling points shown on campus." />
            <div className="space-y-3 text-sm text-campus-700">
              <div className="flex items-center gap-3">
                <span className="h-4 w-4 rounded-full bg-emerald-700" />
                <span>ESP32 environmental sensors</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="h-4 w-4 rounded-md bg-blue-500" />
                <span>Smart recycling bins</span>
              </div>
            </div>
          </div>

          <div className="rounded-3xl bg-campus-800 p-6 text-white shadow-sm">
            <SectionHeader title="Smart Bin Rewards" subtitle="Open a bin marker and simulate recycling." />
            <div className="space-y-3 text-sm text-campus-100/90">
              <p>Plastic: 30 points</p>
              <p>Paper: 25 points</p>
              <p>Glass: 35 points</p>
              <p>Each action also creates EcoEnergy for Eco Forest.</p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
