type Project = {
  id: number;
  title: string;
  description: string;
  submission_date: string;
  impact_score?: number | null;
  file_url?: string | null;
};

export default function ProjectCard({ project }: { project: Project }) {
  const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  return (
    <div className="rounded-2xl bg-white/90 p-5 shadow-sm">
      <h3 className="font-display text-lg text-campus-800">{project.title}</h3>
      <p className="mt-1 text-sm text-campus-600">{project.description}</p>
      <div className="mt-3 text-xs text-campus-500">
        Submitted {new Date(project.submission_date).toLocaleDateString()}
      </div>
      
      <div className="mt-4 flex items-center justify-between">
        {project.impact_score !== null && project.impact_score !== undefined ? (
          <div className="text-sm font-semibold text-campus-700">
            Impact score: {project.impact_score}
          </div>
        ) : <div />}
        
        {project.file_url && (
          <a
            href={`${API_BASE}${project.file_url}`}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm font-semibold text-campus-600 transition hover:text-campus-900 underline underline-offset-2"
          >
            Download file
          </a>
        )}
      </div>
    </div>
  );
}
