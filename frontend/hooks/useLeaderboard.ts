import { useCallback } from "react";
import useFetch from "./useFetch";
import { api } from "../services/api";

export default function useLeaderboard() {
  const fetcher = useCallback(() => api.getLeaderboard(), []);
  return useFetch(fetcher);
}
