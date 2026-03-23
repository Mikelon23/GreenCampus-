import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import SectionHeader from "../components/SectionHeader";
import BadgeDisplay from "../components/BadgeDisplay";
import { api, Badge, EarnedBadge, EcoAction } from "../services/api";
import { useAuth } from "../contexts/AuthContext";

const EDIT_WINDOW_MS = 30 * 60 * 1000;

function getLevel(points: number) {
  if (points >= 700) return "Level 4 - Green Leader";
  if (points >= 300) return "Level 3 - Sustainability Advocate";
  if (points >= 100) return "Level 2 - Eco Supporter";
  return "Level 1 - Beginner";
}

export default function PointsPage() {
  const { user, loading: authLoading } = useAuth();
  const [points, setPoints] = useState<{ user_id: number; total_points: number } | null>(null);
  const [badges, setBadges] = useState<Badge[]>([]);
  const [earnedBadges, setEarnedBadges] = useState<EarnedBadge[]>([]);
  const [actions, setActions] = useState<EcoAction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [actionType, setActionType] = useState("");
  const [editingActionId, setEditingActionId] = useState<number | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const loadData = async () => {
    if (!user) return;
    try {
      setLoading(true);
      setError("");
      const [pointsData, actionsData, badgesData, earnedBadgeData] = await Promise.all([
        api.getPoints(user.id),
        api.getActions(user.id),
        api.getBadges(),
        api.getEarnedBadges(user.id)
      ]);
      setPoints(pointsData);
      setActions(actionsData);
      setBadges(badgesData);
      setEarnedBadges(earnedBadgeData);
    } catch (err: any) {
      setError(err.message || "Failed to load points data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!authLoading) {
      if (user) {
        loadData();
      } else {
        setLoading(false);
      }
    }
  }, [user, authLoading]);

  const resetForm = () => {
    setActionType("");
    setEditingActionId(null);
  };

  const handleSubmitAction = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!actionType || !user) return;

    setSubmitting(true);
    try {
      if (editingActionId) {
        await api.updateAction(editingActionId, { action_type: actionType });
      } else {
        await api.logAction({ user_id: user.id, action_type: actionType });
      }
      resetForm();
      await loadData();
    } catch (err: any) {
      setError(err.message || "Failed to save action.");
    } finally {
      setSubmitting(false);
    }
  };

  const canEditAction = (action: EcoAction) =>
    Date.now() - new Date(action.timestamp).getTime() <= EDIT_WINDOW_MS;

  const handleDeleteAction = async (action: EcoAction) => {
    try {
      await api.deleteAction(action.id);
      if (editingActionId === action.id) resetForm();
      await loadData();
    } catch (err: any) {
      setError(err.message || "Failed to delete action.");
    }
  };

  if (authLoading) return null;

  return (
    <Layout>
      <SectionHeader
        title="Green Points"
        subtitle="Track eco-actions, edit recent submissions for 30 minutes, and turn consistency into game progress."
      />
      <div className="grid gap-6 xl:grid-cols-[0.8fr_1.2fr]">
        <div className="space-y-6">
          <div className="rounded-3xl bg-white/90 p-6 shadow-sm">
            {loading ? (
              <p className="text-sm text-campus-500">Loading points...</p>
            ) : (
              <>
                <p className="text-sm text-campus-600">User</p>
                <p className="font-display text-2xl text-campus-800">{user ? user.name : "No user"}</p>
                <p className="mt-4 text-sm text-campus-600">Total points</p>
                <p className="font-display text-4xl text-campus-800">{points ? points.total_points : 0}</p>
                <p className="mt-2 text-sm text-campus-600">{getLevel(points ? points.total_points : 0)}</p>
              </>
            )}
          </div>

          {user ? (
            <div className="rounded-3xl bg-campus-800 p-8 text-white shadow-sm">
              <SectionHeader
                title={editingActionId ? "Edit Eco-Action" : "Log Eco-Action"}
                subtitle="Record daily habits to earn points, energy, and streak progress."
              />
              <form onSubmit={handleSubmitAction} className="mt-6 flex flex-col gap-4">
                <select
                  required
                  value={actionType}
                  onChange={(e) => setActionType(e.target.value)}
                  className="w-full rounded-xl border border-campus-600 bg-campus-700/50 px-4 py-3 text-white outline-none transition focus:border-campus-300"
                >
                  <option value="" disabled>Select an action...</option>
                  <option value="cycling to campus">Cycling to campus (60 pts)</option>
                  <option value="walking to campus">Walking to campus (50 pts)</option>
                  <option value="using public transport">Using public transport (40 pts)</option>
                  <option value="public transport commute">Public transport commute (45 pts)</option>
                  <option value="reusing water bottle">Reusing water bottle (20 pts)</option>
                  <option value="recycling paper">Recycling paper (30 pts)</option>
                  <option value="waste sorting">Waste sorting (35 pts)</option>
                  <option value="composting food waste">Composting food waste (35 pts)</option>
                  <option value="lab energy shutdown">Lab energy shutdown (40 pts)</option>
                  <option value="reducing energy at home">Reducing energy at home (45 pts)</option>
                </select>
                <div className="flex flex-wrap gap-3">
                  <button
                    type="submit"
                    disabled={submitting || !actionType}
                    className="rounded-xl bg-campus-300 px-6 py-3 font-semibold text-campus-900 transition hover:bg-campus-200 disabled:opacity-50"
                  >
                    {submitting ? "Saving..." : editingActionId ? "Update action" : "Log Action"}
                  </button>
                  {editingActionId ? (
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
            </div>
          ) : null}
        </div>

        <div className="space-y-6">
          <div className="rounded-3xl bg-white/90 p-6 shadow-sm">
            <SectionHeader title="Recent Eco-Actions" subtitle="You can edit or delete your own actions for 30 minutes." />
            {error ? <p className="mb-3 text-sm text-red-700">{error}</p> : null}
            {actions.length === 0 ? (
              <p className="text-sm text-campus-500">No actions recorded yet.</p>
            ) : (
              <div className="space-y-3">
                {actions.map((action) => (
                  <div key={action.id} className="rounded-2xl bg-campus-50 p-4">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <p className="font-semibold text-campus-800">{action.action_type}</p>
                        <p className="text-xs text-campus-500">{new Date(action.timestamp).toLocaleString()}</p>
                      </div>
                      <div className="rounded-full bg-green-100 px-3 py-1 text-sm font-semibold text-green-800">
                        +{action.points_awarded} pts
                      </div>
                    </div>
                    {canEditAction(action) ? (
                      <div className="mt-3 flex gap-3">
                        <button
                          onClick={() => {
                            setEditingActionId(action.id);
                            setActionType(action.action_type);
                          }}
                          className="rounded-xl bg-campus-700 px-4 py-2 text-xs font-semibold text-white transition hover:bg-campus-800"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => handleDeleteAction(action)}
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

          {earnedBadges.length > 0 ? (
            <div className="rounded-3xl bg-white/90 p-6 shadow-sm">
              <SectionHeader title="Earned Badges" subtitle="Achievements you have already unlocked." />
              <div className="grid gap-4 sm:grid-cols-2">
                {earnedBadges.map((badge) => (
                  <div key={`${badge.badge_name}-${badge.earned_at}`} className="rounded-2xl border border-campus-200 bg-campus-50 p-4">
                    <p className="font-display text-lg text-campus-800">{badge.badge_name}</p>
                    <p className="text-sm text-campus-600">{badge.description}</p>
                    <p className="mt-2 text-xs text-campus-500">
                      Earned on {new Date(badge.earned_at).toLocaleDateString()}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          ) : null}

          <div className="rounded-3xl bg-white/90 p-6 shadow-sm">
            <SectionHeader title="Available Badges" />
            <BadgeDisplay badges={badges} />
          </div>
        </div>
      </div>
    </Layout>
  );
}
