type SectionHeaderProps = {
  title: string;
  subtitle?: string;
};

export default function SectionHeader({ title, subtitle }: SectionHeaderProps) {
  return (
    <div className="mb-4">
      <h2 className="font-display text-2xl font-semibold text-campus-800">
        {title}
      </h2>
      {subtitle ? <p className="text-sm text-campus-600">{subtitle}</p> : null}
    </div>
  );
}
