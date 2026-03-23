type LeaderboardEntry = {
  user_id: number;
  name: string;
  total_points: number;
};

export default function LeaderboardTable({
  entries
}: {
  entries: LeaderboardEntry[];
}) {
  return (
    <div className="overflow-hidden rounded-2xl bg-white/90 shadow-sm">
      <table className="w-full text-left text-sm">
        <thead className="bg-campus-50 text-campus-600">
          <tr>
            <th className="px-4 py-3">Rank</th>
            <th className="px-4 py-3">User</th>
            <th className="px-4 py-3">Points</th>
          </tr>
        </thead>
        <tbody>
          {entries.map((entry, index) => (
            <tr key={entry.user_id} className="border-t border-campus-100">
              <td className="px-4 py-3 font-semibold text-campus-700">
                {index + 1}
              </td>
              <td className="px-4 py-3">{entry.name}</td>
              <td className="px-4 py-3">{entry.total_points}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
