const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  let headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(options?.headers || {})
  };

  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) {
      headers = {
        ...headers,
        Authorization: `Bearer ${token}`
      };
    }
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers
  });

  if (!response.ok) {
    let message = `API error: ${response.status}`;
    try {
      const payload = await response.json();
      if (payload?.error) {
        message = payload.error;
      } else if (payload?.detail) {
        message = payload.detail;
      }
    } catch {
      // Ignore non-JSON payloads and keep the fallback message.
    }
    throw new Error(message);
  }

  if (response.status === 204) {
    return undefined as T;
  }
  return (await response.json()) as T;
}

export interface SensorData {
  id: number;
  zone_id: number;
  temperature: number;
  humidity: number;
  co2_level: number;
  energy_usage: number;
  timestamp: string;
}

export interface SustainabilityScore {
  zone_id: number;
  sustainability_score: number;
  energy_efficiency_index: number;
  carbon_index: number;
  calculated_at: string;
}

export interface Zone {
  id: number;
  name: string;
  description: string | null;
  location_coordinates: string | null;
}

export interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  created_at: string;
  current_streak?: number;
  best_streak?: number;
}

export interface LeaderboardEntry {
  user_id: number;
  name: string;
  total_points: number;
}

export interface Badge {
  id?: number;
  badge_name: string;
  description: string;
  points_required: number;
}

export interface EarnedBadge extends Badge {
  earned_at: string;
}

export interface Hackathon {
  id: number;
  title: string;
  description: string;
  start_date: string;
  end_date: string;
  status: string;
}

export interface Project {
  id: number;
  team_id: number;
  title: string;
  description: string;
  submission_date: string;
  impact_score: number | null;
  file_url?: string | null;
  created_by_user_id?: number | null;
}

export interface TreePlanted {
  id: number;
  user_id: number;
  zone_id: number;
  tree_species: string;
  planting_date: string;
}

export interface Team {
  id: number;
  team_name: string;
  hackathon_id: number;
  created_at: string;
  member_count: number;
  is_member: boolean;
  created_by_user_id?: number | null;
}

export interface EcoAction {
  id: number;
  user_id: number;
  action_type: string;
  points_awarded: number;
  timestamp: string;
}

export interface CarbonRecord {
  id: number;
  user_id: number;
  activity_type: string;
  carbon_emission_estimate: number;
  recorded_at: string;
}

export interface EcoEnergy {
  id: number;
  owner_user_id: number;
  source_type: string;
  source_ref_id?: number | null;
  amount: number;
  status: string;
  available_at: string;
  expires_at: string;
  collected_at?: string | null;
}

export interface UserTree {
  user_id: number;
  species: string;
  nickname: string;
  stage: string;
  growth_points: number;
  total_energy_contributed: number;
}

export interface CampusGoal {
  id: number;
  title: string;
  description: string;
  target_energy: number;
  current_energy: number;
  reward_points: number;
  start_date: string;
  end_date: string;
  status: string;
}

export interface ForestFriend {
  user_id: number;
  name: string;
  tree_stage: string;
  available_energy: number;
  current_streak: number;
}

export interface SocialEnergy extends EcoEnergy {
  owner_name: string;
}

export interface EcoverseOverview {
  user_id: number;
  current_streak: number;
  best_streak: number;
  available_energy_total: number;
  collectable_energy: EcoEnergy[];
  tree: UserTree;
  campus_goals: CampusGoal[];
  social_forest: ForestFriend[];
  social_energy: SocialEnergy[];
}

export type AdminResource =
  | "users"
  | "zones"
  | "sensors"
  | "carbon-records"
  | "eco-actions"
  | "badges"
  | "hackathons"
  | "teams"
  | "projects"
  | "trees"
  | "campus-goals";

export const api = {
  getUsers: (): Promise<User[]> => apiFetch<User[]>("/api/users"),
  getZones: (): Promise<Zone[]> => apiFetch<Zone[]>("/api/zones"),
  getSensors: (query = ""): Promise<SensorData[]> => apiFetch<SensorData[]>(`/api/sensors${query}`),
  getSustainability: (): Promise<SustainabilityScore[]> =>
    apiFetch<SustainabilityScore[]>("/api/sustainability"),
  getCarbon: (userId: number): Promise<CarbonRecord[]> => apiFetch<CarbonRecord[]>(`/api/carbon/${userId}`),
  getActions: (userId: number): Promise<EcoAction[]> => apiFetch<EcoAction[]>(`/api/actions/${userId}`),
  getPoints: (userId: number): Promise<{ user_id: number; total_points: number }> =>
    apiFetch(`/api/points/${userId}`),
  getLeaderboard: (): Promise<LeaderboardEntry[]> => apiFetch<LeaderboardEntry[]>("/api/leaderboard"),
  getBadges: (): Promise<Badge[]> => apiFetch<Badge[]>("/api/badges"),
  getEarnedBadges: (userId: number): Promise<EarnedBadge[]> =>
    apiFetch<EarnedBadge[]>(`/api/badges/earned/${userId}`),
  getHackathons: (): Promise<Hackathon[]> => apiFetch<Hackathon[]>("/api/hackathons"),
  getProjects: (): Promise<Project[]> => apiFetch<Project[]>("/api/projects"),
  getTrees: (): Promise<TreePlanted[]> => apiFetch<TreePlanted[]>("/api/trees"),
  getTeams: (hackathonId?: number): Promise<Team[]> =>
    apiFetch<Team[]>(`/api/teams${hackathonId ? `?hackathon_id=${hackathonId}` : ""}`),
  getEcoverseOverview: (userId: number): Promise<EcoverseOverview> =>
    apiFetch<EcoverseOverview>(`/api/ecoverse/overview/${userId}`),

  login: (credentials: { email: string; password: string }) =>
    apiFetch<{ access_token: string; user: User }>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify(credentials)
    }),
  register: (userData: { name: string; email: string; password: string; role: string }) =>
    apiFetch<{ access_token: string; user: User }>("/api/auth/register", {
      method: "POST",
      body: JSON.stringify(userData)
    }),

  logAction: (payload: { user_id: number; action_type: string }) =>
    apiFetch<EcoAction>("/api/actions", {
      method: "POST",
      body: JSON.stringify(payload)
    }),
  updateAction: (actionId: number, payload: { action_type: string }) =>
    apiFetch<EcoAction>(`/api/actions/${actionId}`, {
      method: "PUT",
      body: JSON.stringify(payload)
    }),
  deleteAction: (actionId: number) =>
    apiFetch<void>(`/api/actions/${actionId}`, {
      method: "DELETE"
    }),

  createCarbonRecord: (payload: {
    user_id: number;
    activity_type: string;
    carbon_emission_estimate: number;
  }) =>
    apiFetch<CarbonRecord>("/api/carbon", {
      method: "POST",
      body: JSON.stringify(payload)
    }),
  updateCarbonRecord: (recordId: number, payload: { activity_type: string; carbon_emission_estimate: number }) =>
    apiFetch<CarbonRecord>(`/api/carbon/${recordId}`, {
      method: "PUT",
      body: JSON.stringify(payload)
    }),
  deleteCarbonRecord: (recordId: number) =>
    apiFetch<void>(`/api/carbon/${recordId}`, {
      method: "DELETE"
    }),

  createTreeRecord: (payload: { user_id: number; zone_id: number; tree_species: string }) =>
    apiFetch<TreePlanted>("/api/trees", {
      method: "POST",
      body: JSON.stringify(payload)
    }),
  updateTreeRecord: (treeId: number, payload: { zone_id: number; tree_species: string }) =>
    apiFetch<TreePlanted>(`/api/trees/${treeId}`, {
      method: "PUT",
      body: JSON.stringify(payload)
    }),
  deleteTreeRecord: (treeId: number) =>
    apiFetch<void>(`/api/trees/${treeId}`, {
      method: "DELETE"
    }),

  submitProject: (payload: { team_id: number; title: string; description: string }) =>
    apiFetch<Project>("/api/projects", {
      method: "POST",
      body: JSON.stringify(payload)
    }),
  updateProject: (projectId: number, payload: { team_id: number; title: string; description: string }) =>
    apiFetch<Project>(`/api/projects/${projectId}`, {
      method: "PUT",
      body: JSON.stringify(payload)
    }),
  deleteProject: (projectId: number) =>
    apiFetch<void>(`/api/projects/${projectId}`, {
      method: "DELETE"
    }),
  uploadProjectFile: async (projectId: number, file: File) => {
    const formData = new FormData();
    formData.append("file", file);

    let headers: HeadersInit = {};
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("token");
      if (token) headers = { Authorization: `Bearer ${token}` };
    }

    const response = await fetch(`${API_BASE}/api/projects/${projectId}/upload`, {
      method: "POST",
      body: formData,
      headers
    });
    if (!response.ok) {
      throw new Error("Upload failed");
    }
    return response.json();
  },

  createHackathon: (payload: {
    title: string;
    description: string;
    start_date: string;
    end_date: string;
    status: string;
  }) =>
    apiFetch<Hackathon>("/api/hackathons", {
      method: "POST",
      body: JSON.stringify(payload)
    }),

  createZone: (payload: {
    name: string;
    description: string | null;
    location_coordinates: string | null;
  }) =>
    apiFetch<Zone>("/api/zones", {
      method: "POST",
      body: JSON.stringify(payload)
    }),

  createTeam: (payload: { team_name: string; hackathon_id: number }) =>
    apiFetch<Team>("/api/teams", {
      method: "POST",
      body: JSON.stringify(payload)
    }),
  updateTeam: (teamId: number, payload: { team_name: string; hackathon_id: number }) =>
    apiFetch<Team>(`/api/teams/${teamId}`, {
      method: "PUT",
      body: JSON.stringify(payload)
    }),
  deleteTeam: (teamId: number) =>
    apiFetch<void>(`/api/teams/${teamId}`, {
      method: "DELETE"
    }),
  joinTeam: (teamId: number, payload: { user_id: number }) =>
    apiFetch<{ team_id: number; user_id: number }>(`/api/teams/${teamId}/join`, {
      method: "POST",
      body: JSON.stringify(payload)
    }),

  collectEnergy: (energyId: number) =>
    apiFetch<{ energy_id: number; status: string; amount: number }>(`/api/ecoverse/energy/${energyId}/collect`, {
      method: "POST"
    }),
  helpEnergy: (energyId: number) =>
    apiFetch<{ energy_id: number; status: string; amount: number }>(`/api/ecoverse/energy/${energyId}/help`, {
      method: "POST"
    }),
  rescueEnergy: (energyId: number) =>
    apiFetch<{ energy_id: number; status: string; amount: number }>(`/api/ecoverse/energy/${energyId}/rescue`, {
      method: "POST"
    }),

  getAdminResource: <T = Record<string, unknown>>(resource: AdminResource): Promise<T[]> =>
    apiFetch<T[]>(`/api/admin/${resource}`),
  createAdminResource: <T = Record<string, unknown>>(resource: AdminResource, payload: Record<string, unknown>) =>
    apiFetch<T>(`/api/admin/${resource}`, {
      method: "POST",
      body: JSON.stringify(payload)
    }),
  updateAdminResource: <T = Record<string, unknown>>(
    resource: AdminResource,
    itemId: number,
    payload: Record<string, unknown>
  ) =>
    apiFetch<T>(`/api/admin/${resource}/${itemId}`, {
      method: "PUT",
      body: JSON.stringify(payload)
    }),
  deleteAdminResource: (resource: AdminResource, itemId: number) =>
    apiFetch<void>(`/api/admin/${resource}/${itemId}`, {
      method: "DELETE"
    })
};
