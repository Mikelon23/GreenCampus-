import { useEffect, useMemo, useState } from "react";
import Layout from "../components/Layout";
import SectionHeader from "../components/SectionHeader";
import { useAuth } from "../contexts/AuthContext";
import { api } from "../services/api";

type Zone = {
  id: number;
  name: string;
  description?: string | null;
  location_coordinates?: string | null;
};

type Sensor = {
  zone_id: number;
  temperature: number;
  humidity: number;
  co2_level: number;
  energy_usage: number;
};

type TreeRecord = {
  id: number;
  user_id: number;
  zone_id: number;
  tree_species: string;
  planting_date: string;
};

const EDIT_WINDOW_MS = 30 * 60 * 1000;

export default function MapPage() {
  const { user, loading: authLoading } = useAuth();
  const [zones, setZones] = useState<Zone[]>([]);
  const [sensors, setSensors] = useState<Sensor[]>([]);
  const [trees, setTrees] = useState<TreeRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [editingTreeId, setEditingTreeId] = useState<number | null>(null);
  const [zoneId, setZoneId] = useState("");
  const [treeSpecies, setTreeSpecies] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const load = async () => {
    try {
      setError("");
      setLoading(true);
      const [zonesData, sensorsData, treesData] = await Promise.all([
        api.getZones(),
        api.getSensors(""),
        api.getTrees()
      ]);
      setZones(zonesData as Zone[]);
      setSensors(sensorsData as Sensor[]);
      setTrees(treesData as TreeRecord[]);
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
    const metrics: Record<number, Sensor> = {};
    sensors.forEach((sensor) => {
      if (!metrics[sensor.zone_id]) {
        metrics[sensor.zone_id] = sensor;
      }
    });
    return metrics;
  }, [sensors]);

  const treeCounts = useMemo(() => {
    const counts: Record<number, number> = {};
    trees.forEach((tree) => {
      counts[tree.zone_id] = (counts[tree.zone_id] || 0) + 1;
    });
    return counts;
  }, [trees]);

  const myTrees = useMemo(() => {
    if (!user) return [];
    return trees
      .filter((tree) => tree.user_id === user.id)
      .sort((a, b) => new Date(b.planting_date).getTime() - new Date(a.planting_date).getTime());
  }, [trees, user]);

  const canEditTree = (record: TreeRecord) =>
    !!user &&
    record.user_id === user.id &&
    Date.now() - new Date(record.planting_date).getTime() <= EDIT_WINDOW_MS;

  const resetForm = () => {
    setEditingTreeId(null);
    setZoneId("");
    setTreeSpecies("");
  };

  const startEdit = (record: TreeRecord) => {
    setEditingTreeId(record.id);
    setZoneId(record.zone_id.toString());
    setTreeSpecies(record.tree_species);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user || !zoneId || !treeSpecies) return;

    setSubmitting(true);
    setError("");
    try {
      if (editingTreeId) {
        await api.updateTreeRecord(editingTreeId, {
          zone_id: parseInt(zoneId, 10),
          tree_species: treeSpecies
        });
      } else {
        await api.createTreeRecord({
          user_id: user.id,
          zone_id: parseInt(zoneId, 10),
          tree_species: treeSpecies
        });
      }
      resetForm();
      setTrees((await api.getTrees()) as TreeRecord[]);
    } catch (err: any) {
      setError(err.message || "Failed to save tree record.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (record: TreeRecord) => {
    try {
      setError("");
      await api.deleteTreeRecord(record.id);
      if (editingTreeId === record.id) resetForm();
      setTrees((await api.getTrees()) as TreeRecord[]);
    } catch (err: any) {
      setError(err.message || "Failed to delete tree record.");
    }
  };

  if (authLoading) return null;

  return (
    <Layout>
      <SectionHeader
        title="Campus Sustainability Map"
        subtitle="Zone indicators plus personal tree planting records."
      />
      {error ? <div className="mb-6 rounded-2xl bg-red-50 p-4 text-sm text-red-700">{error}</div> : null}

      <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-3xl bg-white/90 p-6 shadow-sm">
          {loading ? (
            <p className="text-sm text-campus-500">Loading zones...</p>
          ) : (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {zones.map((zone) => {
                const metric = zoneMetrics[zone.id];
                return (
                  <div key={zone.id} className="rounded-2xl bg-campus-50 p-4">
                    <h3 className="font-display text-lg text-campus-800">{zone.name}</h3>
                    <p className="text-xs text-campus-600">{zone.description || "No description"}</p>
                    {metric ? (
                      <div className="mt-3 text-sm text-campus-700">
                        <p>Temp: {metric.temperature.toFixed(1)} C</p>
                        <p>Humidity: {metric.humidity.toFixed(1)}%</p>
                        <p>CO2: {metric.co2_level.toFixed(0)} ppm</p>
                        <p>Energy: {metric.energy_usage.toFixed(0)} kWh</p>
                      </div>
                    ) : (
                      <p className="mt-3 text-sm text-campus-500">No sensor data yet.</p>
                    )}
                    <p className="mt-2 text-xs text-campus-600">Trees planted: {treeCounts[zone.id] || 0}</p>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        <div className="space-y-6">
          <div className="rounded-3xl bg-campus-800 p-6 text-white shadow-sm">
            <SectionHeader
              title={editingTreeId ? "Edit Tree Record" : "Plant a Tree"}
              subtitle="Log a planting record and edit it for 30 minutes."
            />
            {!user ? (
              <p className="text-sm text-campus-100/90">Sign in to plant trees and keep a personal record.</p>
            ) : (
              <form onSubmit={handleSubmit} className="mt-4 space-y-4">
                <div>
                  <label className="mb-2 block text-sm font-medium text-campus-100">Zone</label>
                  <select
                    required
                    value={zoneId}
                    onChange={(e) => setZoneId(e.target.value)}
                    className="w-full rounded-xl border border-campus-600 bg-campus-700/70 px-4 py-3 text-white outline-none focus:border-campus-300"
                  >
                    <option value="" disabled>
                      Select a zone
                    </option>
                    {zones.map((zone) => (
                      <option key={zone.id} value={zone.id}>
                        {zone.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="mb-2 block text-sm font-medium text-campus-100">Species</label>
                  <input
                    required
                    value={treeSpecies}
                    onChange={(e) => setTreeSpecies(e.target.value)}
                    className="w-full rounded-xl border border-campus-600 bg-campus-700/70 px-4 py-3 text-white outline-none focus:border-campus-300"
                    placeholder="Example: Jacaranda"
                  />
                </div>

                <div className="flex flex-wrap gap-3">
                  <button
                    type="submit"
                    disabled={submitting}
                    className="rounded-xl bg-campus-300 px-6 py-3 font-semibold text-campus-900 transition hover:bg-campus-200 disabled:opacity-50"
                  >
                    {submitting ? "Saving..." : editingTreeId ? "Update record" : "Add record"}
                  </button>
                  {editingTreeId ? (
                    <button
                      type="button"
                      onClick={resetForm}
                      className="rounded-xl border border-campus-500 px-6 py-3 font-semibold text-white transition hover:bg-campus-700"
                    >
                      Cancel edit
                    </button>
                  ) : null}
                </div>
              </form>
            )}
          </div>

          <div className="rounded-3xl bg-white/90 p-6 shadow-sm">
            <SectionHeader title="My Tree Records" subtitle="Edit or delete your own records for 30 minutes." />
            {!user ? (
              <p className="text-sm text-campus-500">Sign in to see your tree history.</p>
            ) : myTrees.length === 0 ? (
              <p className="text-sm text-campus-500">No tree records yet.</p>
            ) : (
              <div className="space-y-3">
                {myTrees.map((record) => (
                  <div key={record.id} className="rounded-2xl bg-campus-50 p-4">
                    <p className="font-semibold text-campus-800">{record.tree_species}</p>
                    <p className="text-xs text-campus-500">
                      Zone #{record.zone_id} - {new Date(record.planting_date).toLocaleString()}
                    </p>
                    {canEditTree(record) ? (
                      <div className="mt-3 flex gap-3">
                        <button
                          onClick={() => startEdit(record)}
                          className="rounded-xl bg-campus-700 px-4 py-2 text-xs font-semibold text-white transition hover:bg-campus-800"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => handleDelete(record)}
                          className="rounded-xl bg-red-100 px-4 py-2 text-xs font-semibold text-red-700 transition hover:bg-red-200"
                        >
                          Delete
                        </button>
                      </div>
                    ) : null}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
}

