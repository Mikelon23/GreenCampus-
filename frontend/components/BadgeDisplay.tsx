type Badge = {
  badge_name: string;
  description: string;
  points_required: number;
};

export default function BadgeDisplay({ badges }: { badges: Badge[] }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {badges.map((badge) => (
        <div key={badge.badge_name} className="rounded-2xl bg-white/90 p-4 shadow-sm">
          <p className="font-display text-lg text-campus-800">{badge.badge_name}</p>
          <p className="text-sm text-campus-600">{badge.description}</p>
          <p className="mt-2 text-xs text-campus-500">
            {badge.points_required} points
          </p>
        </div>
      ))}
    </div>
  );
}
