import { useCallback } from "react";
import useFetch from "./useFetch";
import { api } from "../services/api";

export default function useHackathons() {
  const fetcher = useCallback(() => api.getHackathons(), []);
  return useFetch(fetcher);
}
