import { useCallback } from "react";
import useFetch from "./useFetch";
import { api } from "../services/api";

export default function useUserPoints(userId: number) {
  const fetcher = useCallback(() => api.getPoints(userId), [userId]);
  return useFetch(fetcher);
}
