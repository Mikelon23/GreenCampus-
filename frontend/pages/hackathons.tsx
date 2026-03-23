import { useEffect, useMemo, useState } from "react";
import Layout from "../components/Layout";
import SectionHeader from "../components/SectionHeader";
import ProjectCard from "../components/ProjectCard";
import { api, Hackathon, Project, Team } from "../services/api";
import { useAuth } from "../contexts/AuthContext";

const EDIT_WINDOW_MS = 30 * 60 * 1000;

export default function HackathonsPage() {
  const { user } = useAuth();
  const [hackathons, setHackathons] = useState<Hackathon[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [teamName, setTeamName] = useState("");
  const [teamHackathonId, setTeamHackathonId] = useState("");
  const [teamBusy, setTeamBusy] = useState(false);

  const [projectId, setProjectId] = useState<number | null>(null);
  const [teamId, setTeamId] = useState("");
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [projectBusy, setProjectBusy] = useState(false);

  const loadData = async () => {
    try {
      setError("");
      setLoading(true);
      const [hackathonsData, projectsData] = await Promise.all([api.getHackathons(), api.getProjects()]);
      setHackathons(hackathonsData);
      setProjects(projectsData);
      if (user) {
        setTeams(await api.getTeams());
      } else {
        setTeams([]);
      }
    } catch (err: any) {
      setError(err.message || "Failed to load hackathon data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [user]);

  const memberTeams = useMemo(() => teams.filter((team) => team.is_member), [teams]);
  
  const sortedProjects = useMemo(() => {
    return [...projects].sort((a, b) => 
      new Date(b.submission_date).getTime() - new Date(a.submission_date).getTime()
    );
  }, [projects]);

  const resetProjectForm = () => {
    setProjectId(null);
    setTeamId("");
    setTitle("");
    setDescription("");
    setFile(null);
  };

  const canEditProject = (project: Project) =>
    !!user &&
    project.created_by_user_id === user.id &&
    Date.now() - new Date(project.submission_date).getTime() <= EDIT_WINDOW_MS;

  const startEditProject = (project: Project) => {
    setProjectId(project.id);
    setTeamId(project.team_id.toString());
    setTitle(project.title);
    setDescription(project.description);
    setFile(null);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleCreateTeam = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!teamName || !teamHackathonId) return;
    setTeamBusy(true);
    setError("");
    try {
      await api.createTeam({
        team_name: teamName,
        hackathon_id: parseInt(teamHackathonId, 10)
      });
      setTeamName("");
      setTeamHackathonId("");
      await loadData();
    } catch (err: any) {
      setError(err.message || "Failed to create team.");
    } finally {
      setTeamBusy(false);
    }
  };

  const handleJoinTeam = async (team: Team) => {
    if (!user) return;
    try {
      setError("");
      await api.joinTeam(team.id, { user_id: user.id });
      await loadData();
    } catch (err: any) {
      setError(err.message || "Failed to join team.");
    }
  };

  const handleSubmitProject = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !description || !teamId) return;

    setProjectBusy(true);
    setError("");
    try {
      let savedProject: Project;
      if (projectId) {
        savedProject = await api.updateProject(projectId, {
          team_id: parseInt(teamId, 10),
          title,
          description
        });
      } else {
        savedProject = await api.submitProject({
          team_id: parseInt(teamId, 10),
          title,
          description
        });
      }

      if (file) {
        await api.uploadProjectFile(savedProject.id, file);
      }

      resetProjectForm();
      await loadData();
    } catch (err: any) {
      setError(err.message || "Failed to save project.");
    } finally {
      setProjectBusy(false);
    }
  };

  const handleDeleteProject = async (project: Project) => {
    try {
      setError("");
      await api.deleteProject(project.id);
      if (projectId === project.id) {
        resetProjectForm();
      }
      await loadData();
    } catch (err: any) {
      setError(err.message || "Failed to delete project.");
    }
  };

  return (
    <Layout>
      <SectionHeader
        title="GreenHack Hub"
        subtitle="Create teams, submit projects from the top of the page, and keep a 30-minute edit window for your own submissions."
      />
      {error ? <div className="mb-6 rounded-2xl bg-red-50 p-4 text-sm text-red-700">{error}</div> : null}
      {loading ? (
        <p className="text-sm text-campus-500">Loading hackathons...</p>
      ) : (
        <>
          {user ? (
            <div className="mb-8 grid gap-6 xl:grid-cols-2">
              <div className="rounded-3xl bg-white/90 p-6 shadow-sm">
                <SectionHeader
                  title="Create or Join a Team"
                  subtitle="Social coordination sits at the start of the flow so project work stays aligned."
                />
                <form onSubmit={handleCreateTeam} className="grid gap-4 md:grid-cols-2">
                  <input
                    type="text"
                    required
                    value={teamName}
                    onChange={(e) => setTeamName(e.target.value)}
                    className="w-full rounded-xl border border-campus-200 bg-campus-50 px-4 py-3 outline-none transition focus:border-campus-400 focus:bg-white"
                    placeholder="Team name"
                  />
                  <select
                    required
                    value={teamHackathonId}
                    onChange={(e) => setTeamHackathonId(e.target.value)}
                    className="w-full rounded-xl border border-campus-200 bg-campus-50 px-4 py-3 outline-none transition focus:border-campus-400 focus:bg-white"
                  >
                    <option value="" disabled>Select a hackathon</option>
                    {hackathons.map((hackathon) => (
                      <option key={hackathon.id} value={hackathon.id}>
                        {hackathon.title}
                      </option>
                    ))}
                  </select>
                  <div className="md:col-span-2 flex justify-end">
                    <button
                      type="submit"
                      disabled={teamBusy}
                      className="rounded-xl bg-campus-700 px-5 py-3 font-semibold text-white transition hover:bg-campus-800 disabled:opacity-60"
                    >
                      {teamBusy ? "Creating..." : "Create team"}
                    </button>
                  </div>
                </form>
              </div>

              <div className="rounded-3xl bg-campus-900 p-6 text-white shadow-xl">
                <SectionHeader
                  title={projectId ? "Edit Project" : "New Project Submission"}
                  subtitle="Your project form stays at the very top, so the layout no longer shifts the content down the page."
                />
                <form onSubmit={handleSubmitProject} className="grid gap-4 md:grid-cols-2">
                  <select
                    required
                    value={teamId}
                    onChange={(e) => setTeamId(e.target.value)}
                    className="w-full rounded-xl border border-campus-700 bg-campus-800 px-4 py-3 text-white outline-none transition focus:border-campus-300"
                  >
                    <option value="" disabled>Select one of your teams</option>
                    {memberTeams.map((team) => (
                      <option key={team.id} value={team.id}>
                        {team.team_name} (Hackathon #{team.hackathon_id})
                      </option>
                    ))}
                  </select>
                  <input
                    type="text"
                    required
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="w-full rounded-xl border border-campus-700 bg-campus-800 px-4 py-3 text-white outline-none transition focus:border-campus-300"
                    placeholder="Project title"
                  />
                  <textarea
                    required
                    rows={4}
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    className="md:col-span-2 w-full rounded-xl border border-campus-700 bg-campus-800 px-4 py-3 text-white outline-none transition focus:border-campus-300"
                    placeholder="Describe your project's impact..."
                  />
                  <div className="md:col-span-2">
                    <input
                      type="file"
                      accept=".pdf,.zip,.docx"
                      onChange={handleFileChange}
                      className="w-full text-sm text-campus-100 file:mr-4 file:rounded-xl file:border-0 file:bg-campus-100 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-campus-900 hover:file:bg-campus-200"
                    />
                  </div>
                  <div className="md:col-span-2 flex flex-wrap justify-end gap-3">
                    {projectId ? (
                      <button
                        type="button"
                        onClick={resetProjectForm}
                        className="rounded-xl border border-campus-500 px-5 py-3 font-semibold text-white transition hover:bg-campus-800"
                      >
                        Cancel edit
                      </button>
                    ) : null}
                    <button
                      type="submit"
                      disabled={projectBusy || memberTeams.length === 0}
                      className="rounded-xl bg-white px-5 py-3 font-semibold text-campus-900 transition hover:bg-campus-100 disabled:opacity-60"
                    >
                      {projectBusy ? "Saving..." : projectId ? "Update project" : "Submit project"}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          ) : null}

          <div className="mb-8 grid gap-4 md:grid-cols-2">
            {sortedProjects.map((project) => (
              <div key={project.id} className="space-y-3">
                <ProjectCard project={project} />
                {canEditProject(project) ? (
                  <div className="flex gap-3 rounded-2xl bg-white/70 p-3 shadow-sm">
                    <button
                      onClick={() => startEditProject(project)}
                      className="rounded-xl bg-campus-700 px-4 py-2 text-xs font-semibold text-white transition hover:bg-campus-800"
                    >
                      Edit (30 min)
                    </button>
                    <button
                      onClick={() => handleDeleteProject(project)}
                      className="rounded-xl bg-red-100 px-4 py-2 text-xs font-semibold text-red-700 transition hover:bg-red-200"
                    >
                      Delete
                    </button>
                  </div>
                ) : null}
              </div>
            ))}
          </div>

          <div className="mb-8 grid gap-4 md:grid-cols-2">
            {hackathons.map((hackathon) => (
              <div key={hackathon.id} className="rounded-2xl bg-white/90 p-5 shadow-sm">
                <h3 className="font-display text-lg text-campus-800">{hackathon.title}</h3>
                <p className="text-sm text-campus-600">{hackathon.description}</p>
                <p className="mt-2 text-xs text-campus-500">
                  {hackathon.start_date} - {hackathon.end_date} - {hackathon.status}
                </p>
              </div>
            ))}
          </div>

          {user ? (
            <div className="mb-8 rounded-3xl bg-white/90 p-6 shadow-sm">
              <SectionHeader
                title="Hackathon Teams"
                subtitle="Competition and collaboration stay visible, inspired by the social loops highlighted in Ant Forest."
              />
              {teams.length === 0 ? (
                <p className="text-sm text-campus-500">No teams created yet.</p>
              ) : (
                <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
                  {teams.map((team) => (
                    <div key={team.id} className="rounded-2xl border border-campus-100 bg-campus-50 p-4">
                      <p className="font-semibold text-campus-800">{team.team_name}</p>
                      <p className="text-xs text-campus-500">
                        Hackathon #{team.hackathon_id} - {team.member_count} members
                      </p>
                      <div className="mt-4 flex gap-2">
                        {team.is_member ? (
                          <span className="rounded-full bg-green-100 px-3 py-2 text-xs font-semibold text-green-800">
                            Joined
                          </span>
                        ) : (
                          <button
                            onClick={() => handleJoinTeam(team)}
                            className="rounded-xl bg-campus-700 px-4 py-2 text-xs font-semibold text-white transition hover:bg-campus-800"
                          >
                            Join team
                          </button>
                        )}
                        {team.is_member ? (
                          <button
                            onClick={() => setTeamId(team.id.toString())}
                            className="rounded-xl border border-campus-300 bg-white px-4 py-2 text-xs font-semibold text-campus-800 transition hover:bg-campus-100"
                          >
                            Use in form
                          </button>
                        ) : null}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : null}
        </>
      )}
    </Layout>
  );
}
