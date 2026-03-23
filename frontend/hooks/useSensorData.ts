import { useCallback } from "react";
import useFetch from "./useFetch";
import { api } from "../services/api";

/** Polls sensor data every 10 seconds so the dashboard auto-updates. */
const SENSOR_REFRESH_MS = 10_000;

export default function useSensorData() {
  const fetcher = useCallback(() => api.getSensors(""), []);
  return useFetch(fetcher, SENSOR_REFRESH_MS);
}
