import { useCallback } from "react";
import useFetch from "./useFetch";
import { api } from "../services/api";

export default function useCarbonData(userId: number) {
  const fetcher = useCallback(() => api.getCarbon(userId), [userId]);
  return useFetch(fetcher);
}
