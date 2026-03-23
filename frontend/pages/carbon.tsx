import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import SectionHeader from "../components/SectionHeader";
import { api } from "../services/api";
import { useAuth } from "../contexts/AuthContext";

type CarbonRecord = {
  id: number;
  activity_type: string;
  carbon_emission_estimate: number;
  recorded_at: string;
};

const activityOptions = [
  { label: "Car commute", value: "Car commute", estimate: 4.25 },
  { label: "Motorbike commute", value: "Motorbike commute", estimate: 2.8 },
  { label: "Bus commute", value: "Bus commute", estimate: 1.15 },
  { label: "Short-haul flight", value: "Short-haul flight", estimate: 90.0 },
  { label: "High-energy lab session", value: "High-energy lab session", estimate: 6.5 }
];

export default function CarbonPage() {
  const { user, loading: authLoading } = useAuth();
  const [records, setRecords] = useState<CarbonRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [activityType, setActivityType] = useState(activityOptions[0].value);
  const [carbonEstimate, setCarbonEstimate] = useState(activityOptions[0].estimate.toString());
  const [submitting, setSubmitting] = useState(false);
  const [editingRecordId, setEditingRecordId] = useState<number | null>(null);
  const [error, setError] = useState("");

  const EDIT_WINDOW_MS = 30 * 60 * 1000;

  const loadData = async () => {
    if (!user) {
      setLoading(false);
      return;
    }
    try {
      setLoading(true);
      setError("");
      const data = (await api.getCarbon(user.id)) as CarbonRecord[];
      setRecords(data);
    } catch (err: any) {
      setError(err.message || "Failed to load carbon data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!authLoading) {
      loadData();
    }
  }, [user, authLoading]);

  const handleActivityChange = (value: string) => {
    setActivityType(value);
    const selected = activityOptions.find((option) => option.value === value);
    if (selected) {
      setCarbonEstimate(selected.estimate.toString());
    }
  };

  const resetForm = () => {
    setActivityType(activityOptions[0].value);
    setCarbonEstimate(activityOptions[0].estimate.toString());
    setEditingRecordId(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) return;

    setSubmitting(true);
    setError("");
    try {
      if (editingRecordId) {
        await api.updateCarbonRecord(editingRecordId, {
          activity_type: activityType,
          carbon_emission_estimate: parseFloat(carbonEstimate)
        });
      } else {
        await api.createCarbonRecord({
          user_id: user.id,
          activity_type: activityType,
          carbon_emission_estimate: parseFloat(carbonEstimate)
        });
      }
      resetForm();
      await loadData();
    } catch (err: any) {
      setError(err.message || "Failed to save carbon activity.");
    } finally {
      setSubmitting(false);
    }
  };

  const canEditRecord = (record: CarbonRecord) =>
    Date.now() - new Date(record.recorded_at).getTime() <= EDIT_WINDOW_MS;

  const startEdit = (record: CarbonRecord) => {
    setEditingRecordId(record.id);
    setActivityType(record.activity_type);
    setCarbonEstimate(record.carbon_emission_estimate.toString());
  };

  const handleDelete = async (record: CarbonRecord) => {
    try {
      setError("");
      await api.deleteCarbonRecord(record.id);
      if (editingRecordId === record.id) resetForm();
      await loadData();
    } catch (err: any) {
      setError(err.message || "Failed to delete carbon record.");
    }
  };

  if (authLoading) return null;

  return (
    <Layout>
      <SectionHeader
        title="Carbon Tracker"
        subtitle="Monitor personal carbon footprint activities"
      />
      <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
        <div className="rounded-3xl bg-white/90 p-6 shadow-sm">
          {!user ? (
            <div className="py-8 text-center text-campus-600">
              <p>Please log in to view your carbon footprint activities.</p>
            </div>
          ) : loading ? (
            <p className="text-sm text-campus-500">Loading carbon data...</p>
          ) : (
            <>
              <p className="text-sm text-campus-600">
                Showing records for <span className="font-semibold">{user.name}</span>
              </p>
              {error ? (
                <div className="mt-4 rounded-2xl bg-red-50 p-4 text-sm text-red-700">{error}</div>
              ) : null}
              <div className="mt-4 space-y-3">
                {records.map((record) => (
                  <div key={`${record.id}-${record.recorded_at}`} className="rounded-2xl bg-campus-50 p-4">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <p className="font-semibold text-campus-800">{record.activity_type}</p>
                        <p className="text-sm text-campus-600">
                          {record.carbon_emission_estimate.toFixed(2)} kg CO2
                        </p>
                        <p className="text-xs text-campus-500">
                          {new Date(record.recorded_at).toLocaleString()}
                        </p>
                      </div>
                    </div>
                    {canEditRecord(record) ? (
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
                {records.length === 0 ? (
                  <p className="text-sm text-campus-500">No carbon records yet.</p>
                ) : null}
              </div>
            </>
          )}
        </div>

        <div className="rounded-3xl bg-campus-800 p-6 text-white shadow-sm">
          <SectionHeader
            title={editingRecordId ? "Edit Activity" : "Register Activity"}
            subtitle="Log an activity and keep your carbon history up to date."
          />
          {!user ? (
            <p className="text-sm text-campus-100/90">Sign in to register carbon activities.</p>
          ) : (
            <form onSubmit={handleSubmit} className="mt-4 space-y-4">
              <div>
                <label className="mb-2 block text-sm font-medium text-campus-100">Activity</label>
                <select
                  value={activityType}
                  onChange={(e) => handleActivityChange(e.target.value)}
                  className="w-full rounded-xl border border-campus-600 bg-campus-700/70 px-4 py-3 text-white outline-none focus:border-campus-300"
                >
                  {activityOptions.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="mb-2 block text-sm font-medium text-campus-100">Estimated kg CO2</label>
                <input
                  type="number"
                  min="0"
                  step="0.01"
                  value={carbonEstimate}
                  onChange={(e) => setCarbonEstimate(e.target.value)}
                  className="w-full rounded-xl border border-campus-600 bg-campus-700/70 px-4 py-3 text-white outline-none focus:border-campus-300"
                />
              </div>
              <div className="flex flex-wrap gap-3">
                <button
                  type="submit"
                  disabled={submitting}
                  className="rounded-xl bg-campus-300 px-6 py-3 font-semibold text-campus-900 transition hover:bg-campus-200 disabled:opacity-50"
                >
                  {submitting ? "Saving..." : editingRecordId ? "Update activity" : "Add carbon activity"}
                </button>
                {editingRecordId ? (
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
      </div>
    </Layout>
  );
}
