import { useEffect, useMemo, useState } from "react";
import Layout from "../components/Layout";
import SectionHeader from "../components/SectionHeader";
import { AdminResource, api } from "../services/api";
import { useAuth } from "../contexts/AuthContext";

const resourceConfigs: {
  key: AdminResource;
  label: string;
  template: Record<string, unknown>;
}[] = [
  {
    key: "users",
    label: "Users",
    template: { name: "New User", email: "user@campus.edu", role: "student", password: "ChangeMe123!" }
  },
  {
    key: "zones",
    label: "Zones",
    template: { name: "New Zone", description: "Description", location_coordinates: "0,0" }
  },
  {
    key: "sensors",
    label: "Sensors",
    template: {
      zone_id: 1,
      temperature: 22,
      humidity: 55,
      co2_level: 410,
      energy_usage: 115,
      timestamp: new Date().toISOString()
    }
  },
  {
    key: "carbon-records",
    label: "Carbon Records",
    template: {
      user_id: 1,
      activity_type: "Car commute",
      carbon_emission_estimate: 4.25,
      recorded_at: new Date().toISOString()
    }
  },
  {
    key: "eco-actions",
    label: "Eco Actions",
    template: {
      user_id: 1,
      action_type: "cycling to campus",
      points_awarded: 60,
      timestamp: new Date().toISOString()
    }
  },
  {
    key: "badges",
    label: "Badges",
    template: { badge_name: "New Badge", description: "Achievement description", points_required: 150 }
  },
  {
    key: "hackathons",
    label: "Hackathons",
    template: {
      title: "New Hackathon",
      description: "Hackathon description",
      start_date: "2026-03-20",
      end_date: "2026-03-22",
      status: "open"
    }
  },
  {
    key: "teams",
    label: "Teams",
    template: {
      team_name: "New Team",
      hackathon_id: 1,
      created_by_user_id: 1,
      created_at: new Date().toISOString()
    }
  },
  {
    key: "projects",
    label: "Projects",
    template: {
      team_id: 1,
      title: "New Project",
      description: "Project description",
      created_by_user_id: 1,
      submission_date: new Date().toISOString(),
      impact_score: 0,
      file_url: null
    }
  },
  {
    key: "trees",
    label: "Trees",
    template: {
      user_id: 1,
      zone_id: 1,
      tree_species: "Campus Oak",
      planting_date: new Date().toISOString()
    }
  },
  {
    key: "campus-goals",
    label: "Campus Goals",
    template: {
      title: "Collect 5000 energy",
      description: "Shared eco target",
      target_energy: 5000,
      current_energy: 0,
      reward_points: 200,
      start_date: "2026-03-18",
      end_date: "2026-04-18",
      status: "active"
    }
  }
];

export default function AdminPage() {
  const { user, loading: authLoading } = useAuth();
  const [selectedResource, setSelectedResource] = useState<AdminResource>("users");
  const [records, setRecords] = useState<Record<string, unknown>[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [formData, setFormData] = useState<Record<string, any>>({});
  const [editingId, setEditingId] = useState<number | null>(null);

  const currentConfig = useMemo(
    () => resourceConfigs.find((config) => config.key === selectedResource)!,
    [selectedResource]
  );

  const loadResource = async (resource: AdminResource) => {
    try {
      setLoading(true);
      setError("");
      const data = await api.getAdminResource(resource);
      setRecords(data);
      setFormData({ ...currentConfig.template });
      setEditingId(null);
    } catch (err: any) {
      setError(err.message || "Failed to load admin data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!authLoading && user?.role?.toLowerCase() === "admin") {
      loadResource(selectedResource);
    }
  }, [authLoading, user, selectedResource]);

  useEffect(() => {
    setFormData({ ...currentConfig.template });
    setEditingId(null);
  }, [currentConfig]);

  const handleInputChange = (key: string, value: string) => {
    setFormData((prev) => ({ ...prev, [key]: value }));
  };

  const submitEditor = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    try {
      setSaving(true);
      setError("");
      const payload = { ...formData };
      
      // Convert specific types back if needed, based on template defaults
      Object.keys(currentConfig.template).forEach((key) => {
        const defaultVal = currentConfig.template[key];
        if (typeof defaultVal === "number" && payload[key]) {
          payload[key] = Number(payload[key]);
        }
      });

      if (editingId) {
        await api.updateAdminResource(selectedResource, editingId, payload);
      } else {
        await api.createAdminResource(selectedResource, payload);
      }
      await loadResource(selectedResource);
    } catch (err: any) {
      setError(err.message || "Failed to save resource.");
    } finally {
      setSaving(false);
    }
  };

  const startEdit = (record: Record<string, unknown>) => {
    setEditingId(Number(record.id));
    
    // Extract only keys that exist in the template
    const editData: Record<string, any> = {};
    Object.keys(currentConfig.template).forEach(key => {
      editData[key] = record[key] !== undefined ? record[key] : currentConfig.template[key];
    });
    setFormData(editData);
  };

  const resetEditor = () => {
    setEditingId(null);
    setFormData({ ...currentConfig.template });
  };

  const handleDelete = async (recordId: number) => {
    try {
      setError("");
      await api.deleteAdminResource(selectedResource, recordId);
      await loadResource(selectedResource);
    } catch (err: any) {
      setError(err.message || "Failed to delete resource.");
    }
  };

  if (authLoading) return null;

  return (
    <Layout>
      <SectionHeader
        title="Admin Control Center"
        subtitle="Full CRUD across operational modules with a single management workspace."
      />
      {!user ? (
        <div className="rounded-3xl bg-white/90 p-8 text-center shadow-sm">
          <p className="text-campus-700">Please sign in with an admin account to manage the platform.</p>
        </div>
      ) : user.role.toLowerCase() !== "admin" ? (
        <div className="rounded-3xl bg-white/90 p-8 text-center shadow-sm">
          <p className="text-campus-700">This page is restricted to admin users.</p>
        </div>
      ) : (
        <>
          {error ? <div className="mb-6 rounded-2xl bg-red-50 p-4 text-sm text-red-700">{error}</div> : null}
          <div className="grid gap-6 xl:grid-cols-[260px_1fr_1.2fr]">
            <div className="rounded-3xl bg-campus-900 p-4 text-white shadow-xl">
              <p className="mb-4 text-xs uppercase tracking-[0.25em] text-campus-200">Modules</p>
              <div className="space-y-2">
                {resourceConfigs.map((config) => (
                  <button
                    key={config.key}
                    onClick={() => setSelectedResource(config.key)}
                    className={`w-full rounded-2xl px-4 py-3 text-left text-sm font-semibold transition ${
                      selectedResource === config.key
                        ? "bg-white text-campus-900"
                        : "bg-campus-800/60 text-campus-50 hover:bg-campus-700"
                    }`}
                  >
                    {config.label}
                  </button>
                ))}
              </div>
            </div>

            <div className="rounded-3xl bg-white/90 p-6 shadow-sm">
              <SectionHeader
                title={`${currentConfig.label} Records`}
                subtitle="Select a record to edit or delete it directly from the module list."
              />
              {loading ? (
                <p className="text-sm text-campus-500">Loading records...</p>
              ) : (
                <div className="max-h-[70vh] space-y-3 overflow-y-auto pr-1">
                  {records.length === 0 ? (
                    <p className="text-sm text-campus-500">No records in this module yet.</p>
                  ) : (
                    records.map((record) => (
                      <div key={String(record.id)} className="rounded-2xl border border-campus-100 bg-campus-50 p-4">
                        <div className="flex items-start justify-between gap-3">
                          <div>
                            <p className="font-semibold text-campus-800">
                              #{String(record.id)}{" "}
                              {String(record.name || record.title || record.team_name || record.badge_name || record.activity_type || record.action_type || record.tree_species || "Record")}
                            </p>
                            <pre className="mt-2 overflow-x-auto text-xs text-campus-600">
                              {JSON.stringify(record, null, 2)}
                            </pre>
                          </div>
                          <div className="flex flex-col gap-2">
                            <button
                              onClick={() => startEdit(record)}
                              className="rounded-xl bg-campus-700 px-3 py-2 text-xs font-semibold text-white transition hover:bg-campus-800"
                            >
                              Edit
                            </button>
                            <button
                              onClick={() => handleDelete(Number(record.id))}
                              className="rounded-xl bg-red-100 px-3 py-2 text-xs font-semibold text-red-700 transition hover:bg-red-200"
                            >
                              Delete
                            </button>
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}
            </div>

            <div className="rounded-3xl bg-white/90 p-6 shadow-sm">
              <SectionHeader
                title={editingId ? `Edit ${currentConfig.label}` : `Create ${currentConfig.label}`}
                subtitle="Admin CRUD editor with dynamic forms based on the module structure."
              />
              <form onSubmit={submitEditor} className="space-y-4">
                <div className="grid gap-4 md:grid-cols-2">
                  {Object.entries(currentConfig.template).map(([key, defaultVal]) => {
                    const type = typeof defaultVal === "number" ? "number" 
                      : (key.includes("date") || key.includes("timestamp") || key.includes("at")) ? "text" 
                      : "text";
                    return (
                      <div key={key} className={key === "description" ? "md:col-span-2" : ""}>
                        <label className="mb-1 block text-sm font-medium capitalize text-campus-700">
                          {key.replace(/_/g, " ")}
                        </label>
                        {key === "description" ? (
                          <textarea
                            value={formData[key] || ""}
                            onChange={(e) => handleInputChange(key, e.target.value)}
                            required
                            rows={3}
                            className="w-full rounded-xl border border-campus-200 bg-campus-50 px-4 py-3 outline-none transition focus:border-campus-400 focus:bg-white focus:ring-2 focus:ring-campus-400/20"
                          />
                        ) : (
                          <input
                            type={type}
                            value={formData[key] || ""}
                            onChange={(e) => handleInputChange(key, e.target.value)}
                            required
                            step={type === "number" ? "any" : undefined}
                            className="w-full rounded-xl border border-campus-200 bg-campus-50 px-4 py-3 outline-none transition focus:border-campus-400 focus:bg-white focus:ring-2 focus:ring-campus-400/20"
                          />
                        )}
                      </div>
                    );
                  })}
                </div>
                <div className="mt-6 flex gap-3">
                  <button
                    type="submit"
                    disabled={saving}
                    className="rounded-xl bg-campus-700 px-5 py-3 font-semibold text-white transition hover:bg-campus-800 disabled:opacity-60"
                  >
                    {saving ? "Saving..." : editingId ? "Update record" : "Create record"}
                  </button>
                  <button
                    type="button"
                    onClick={resetEditor}
                    className="rounded-xl border border-campus-300 bg-white px-5 py-3 font-semibold text-campus-800 transition hover:bg-campus-50"
                  >
                    Reset form
                  </button>
                </div>
              </form>
            </div>
          </div>
        </>
      )}
    </Layout>
  );
}
