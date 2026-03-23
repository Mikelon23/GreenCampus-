type StatCardProps = {
  title: string;
  value: string;
  subtitle: string;
};

export default function StatCard({ title, value, subtitle }: StatCardProps) {
  return (
    <div className="rounded-2xl bg-white/90 p-5 shadow-sm">
      <p className="text-sm uppercase tracking-wide text-campus-500">{title}</p>
      <p className="mt-2 font-display text-3xl font-semibold text-campus-800">
        {value}
      </p>
      <p className="mt-1 text-sm text-campus-500">{subtitle}</p>
    </div>
  );
}
