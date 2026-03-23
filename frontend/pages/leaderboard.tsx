import Layout from "../components/Layout";
import SectionHeader from "../components/SectionHeader";
import LeaderboardTable from "../components/LeaderboardTable";
import useLeaderboard from "../hooks/useLeaderboard";

type LeaderboardEntry = {
  user_id: number;
  name: string;
  total_points: number;
};

export default function LeaderboardPage() {
  const { data, loading } = useLeaderboard();
  const entries = (data as LeaderboardEntry[]) || [];

  return (
    <Layout>
      <SectionHeader
        title="Leaderboard"
        subtitle="Top sustainability champions on campus"
      />
      {loading ? (
        <p className="text-sm text-campus-500">Loading leaderboard...</p>
      ) : (
        <LeaderboardTable entries={entries} />
      )}
    </Layout>
  );
}
