import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import SectionHeader from "../components/SectionHeader";
import { api, EcoverseOverview, SocialEnergy } from "../services/api";
import { useAuth } from "../contexts/AuthContext";

const stageStyles: Record<string, string> = {
  seed: "from-amber-100 to-amber-300",
  sprout: "from-lime-100 to-lime-300",
  sapling: "from-green-100 to-green-300",
  "young-canopy": "from-emerald-100 to-emerald-300",
  "forest-guardian": "from-campus-100 to-campus-300"
};

export default function ForestPage() {
  const { user, loading: authLoading } = useAuth();
  const [overview, setOverview] = useState<EcoverseOverview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [busyId, setBusyId] = useState<number | null>(null);

  const loadOverview = async () => {
    if (!user) {
      setLoading(false);
      return;
    }
    try {
      setLoading(true);
      setError("");
      setOverview(await api.getEcoverseOverview(user.id));
    } catch (err: any) {
      setError(err.message || "Failed to load the eco forest.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!authLoading) {
      loadOverview();
    }
  }, [user, authLoading]);

  const handleEnergyAction = async (
    energy: SocialEnergy | { id: number },
    action: "collect" | "help" | "rescue"
  ) => {
    setBusyId(energy.id);
    setError("");
    try {
      if (action === "collect") {
        await api.collectEnergy(energy.id);
      } else if (action === "help") {
        await api.helpEnergy(energy.id);
      } else {
        await api.rescueEnergy(energy.id);
      }
      await loadOverview();
    } catch (err: any) {
      setError(err.message || "Energy interaction failed.");
    } finally {
      setBusyId(null);
    }
  };

  if (authLoading) return null;

  return (
    <Layout>
      <SectionHeader
        title="Eco Forest"
        subtitle="Ant-Forest-inspired game loops for daily green habits, social energy, and campus impact."
      />
      {error ? <div className="mb-6 rounded-2xl bg-red-50 p-4 text-sm text-red-700">{error}</div> : null}
      {!user ? (
        <div className="rounded-3xl bg-white/90 p-8 text-center shadow-sm">
          <p className="text-campus-700">Sign in to generate energy, grow your tree, and join campus goals.</p>
        </div>
      ) : loading ? (
        <p className="text-sm text-campus-500">Growing your forest...</p>
      ) : overview ? (
        <>
          <style jsx>{`
            @keyframes floatBubble {
              0%, 100% { transform: translateY(0px) scale(1); }
              50% { transform: translateY(-15px) scale(1.05); }
            }
            .energy-bubble {
              animation: floatBubble 4s ease-in-out infinite;
            }
          `}</style>
          <div className="grid gap-6 xl:grid-cols-[1.25fr_0.75fr]">
            <div className="space-y-6">
              <div className={`relative min-h-[420px] rounded-[2rem] bg-gradient-to-br ${stageStyles[overview.tree.stage] || stageStyles.seed} p-8 shadow-xl overflow-hidden`}>
                
                {/* Floating Energy Bubbles */}
                <div className="absolute inset-0 pointer-events-none z-10">
                  {overview.collectable_energy.map((energy, index) => {
                    // pseudo-random but stable layout based on index
                    const top = 15 + ((index * 17) % 50); 
                    const left = 10 + ((index * 23) % 70);
                    const delay = (index % 5) * 0.5;
                    
                    return (
                      <button
                        key={energy.id}
                        onClick={() => handleEnergyAction(energy, "collect")}
                        disabled={busyId === energy.id}
                        className={`energy-bubble pointer-events-auto absolute flex h-20 w-20 flex-col items-center justify-center rounded-full border-2 border-white/40 bg-white/30 text-campus-900 shadow-xl backdrop-blur-md transition-all hover:scale-110 hover:bg-white/60 hover:shadow-2xl disabled:pointer-events-none disabled:opacity-0 disabled:scale-50 disabled:duration-700`}
                        style={{
                          top: `${top}%`,
                          left: `${left}%`,
                          animationDelay: `${delay}s`
                        }}
                      >
                        <span className="font-display text-2xl font-bold">{energy.amount}</span>
                        <span className="text-[10px] font-bold uppercase tracking-wider text-campus-800">Energy</span>
                      </button>
                    );
                  })}
                </div>

                <div className="relative z-20 flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-[0.3em] text-campus-700/70">Your Tree</p>
                    <h2 className="mt-2 font-display text-4xl font-bold text-campus-900">{overview.tree.nickname}</h2>
                    <p className="mt-2 text-campus-800">
                      {overview.tree.species} - Stage: <span className="font-semibold capitalize">{overview.tree.stage}</span>
                    </p>
                  </div>
                  <div className="rounded-3xl bg-white/70 px-5 py-4 text-campus-900 shadow-sm backdrop-blur">
                    <p className="text-sm">Total energy contributed</p>
                    <p className="font-display text-3xl font-bold">{overview.tree.total_energy_contributed}</p>
                  </div>
                </div>
                
                <div className="absolute bottom-8 left-8 right-8 z-20">
                  <div className="overflow-hidden rounded-full bg-white/60 shadow-inner">
                    <div
                      className="h-4 rounded-full bg-campus-800 transition-all duration-1000 ease-out"
                      style={{ width: `${Math.min(100, (overview.tree.growth_points % 220) / 2.2)}%` }}
                    />
                  </div>
                  <p className="mt-3 text-sm font-medium text-campus-800/80 drop-shadow-sm">
                    {overview.collectable_energy.length > 0 
                      ? "Tap the floating bubbles to collect your energy!" 
                      : "Every collected energy drop grows your virtual tree and pushes campus goals forward."}
                  </p>
                </div>
              </div>

              <div className="grid gap-4 md:grid-cols-3">
                <div className="rounded-3xl bg-white/90 p-5 shadow-sm">
                  <p className="text-sm uppercase tracking-wide text-campus-500">Ready to collect</p>
                  <p className="mt-2 font-display text-4xl text-campus-800">{overview.available_energy_total}</p>
                  <p className="mt-1 text-sm text-campus-500">Energy waiting in your forest</p>
                </div>
                <div className="rounded-3xl bg-white/90 p-5 shadow-sm">
                  <p className="text-sm uppercase tracking-wide text-campus-500">Current streak</p>
                  <p className="mt-2 font-display text-4xl text-campus-800">{overview.current_streak}</p>
                  <p className="mt-1 text-sm text-campus-500">Daily green action chain</p>
                </div>
                <div className="rounded-3xl bg-white/90 p-5 shadow-sm">
                  <p className="text-sm uppercase tracking-wide text-campus-500">Best streak</p>
                  <p className="mt-2 font-display text-4xl text-campus-800">{overview.best_streak}</p>
                  <p className="mt-1 text-sm text-campus-500">Your longest consistency run</p>
                </div>
              </div>
            </div>

            <div className="space-y-6">
              <div className="rounded-3xl bg-campus-900 p-6 text-white shadow-xl">
                <SectionHeader
                  title="Social Canopy"
                  subtitle="Help friends, rescue unused energy, and keep competition alive."
                />
                <div className="space-y-4">
                  {overview.social_energy.length === 0 ? (
                    <p className="text-sm text-campus-100/75">No nearby energy from other players right now.</p>
                  ) : (
                    overview.social_energy.map((energy) => (
                      <div key={energy.id} className="rounded-2xl bg-campus-800/80 p-4">
                        <div className="flex items-start justify-between gap-3">
                          <div>
                            <p className="font-semibold text-white">{energy.owner_name}</p>
                            <p className="text-xs uppercase tracking-[0.2em] text-campus-200">{energy.source_type}</p>
                          </div>
                          <span className="rounded-full bg-white/10 px-3 py-1 text-xs font-semibold text-campus-100">
                            {energy.amount} energy
                          </span>
                        </div>
                        <div className="mt-4 flex gap-2">
                          <button
                            onClick={() => handleEnergyAction(energy, "help")}
                            disabled={busyId === energy.id}
                            className="flex-1 rounded-xl bg-white px-3 py-2 text-xs font-semibold text-campus-900 transition hover:bg-campus-100 disabled:opacity-60"
                          >
                            Help collect
                          </button>
                          <button
                            onClick={() => handleEnergyAction(energy, "rescue")}
                            disabled={busyId === energy.id}
                            className="flex-1 rounded-xl border border-campus-500 px-3 py-2 text-xs font-semibold text-white transition hover:bg-campus-700 disabled:opacity-60"
                          >
                            Rescue unused
                          </button>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>

              <div className="rounded-3xl bg-white/90 p-6 shadow-sm">
                <SectionHeader title="Campus Goals" subtitle="Shared targets turn solo actions into collective momentum." />
                <div className="space-y-4">
                  {overview.campus_goals.map((goal) => {
                    const progress = goal.target_energy > 0 ? Math.round((goal.current_energy / goal.target_energy) * 100) : 0;
                    return (
                      <div key={goal.id} className="rounded-2xl border border-campus-100 bg-campus-50 p-4">
                        <div className="flex items-start justify-between gap-3">
                          <div>
                            <p className="font-semibold text-campus-800">{goal.title}</p>
                            <p className="text-sm text-campus-600">{goal.description}</p>
                          </div>
                          <span className="rounded-full bg-campus-100 px-3 py-1 text-xs font-semibold text-campus-700">
                            {goal.status}
                          </span>
                        </div>
                        <div className="mt-4 overflow-hidden rounded-full bg-white">
                          <div className="h-3 rounded-full bg-campus-700" style={{ width: `${Math.min(100, progress)}%` }} />
                        </div>
                        <p className="mt-2 text-xs text-campus-500">
                          {goal.current_energy} / {goal.target_energy} energy - Reward {goal.reward_points} pts
                        </p>
                      </div>
                    );
                  })}
                </div>
              </div>

              <div className="rounded-3xl bg-white/90 p-6 shadow-sm">
                <SectionHeader title="Forest Circle" subtitle="Visible peer progress strengthens social proof and retention." />
                <div className="space-y-3">
                  {overview.social_forest.map((friend) => (
                    <div key={friend.user_id} className="flex items-center justify-between rounded-2xl bg-campus-50 px-4 py-3">
                      <div>
                        <p className="font-semibold text-campus-800">{friend.name}</p>
                        <p className="text-xs capitalize text-campus-500">
                          {friend.tree_stage} - streak {friend.current_streak}
                        </p>
                      </div>
                      <span className="rounded-full bg-white px-3 py-1 text-xs font-semibold text-campus-700">
                        {friend.available_energy} energy open
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </>
      ) : (
        <div className="rounded-3xl bg-white/90 p-8 text-center shadow-sm">
          <p className="text-campus-700">Eco Forest data is not available right now.</p>
        </div>
      )}
    </Layout>
  );
}
