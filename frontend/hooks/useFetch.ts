import { useEffect, useState } from "react";

/**
 * Fetches data from an async function and optionally re-fetches on an interval.
 *
 * @param fn             - Async fetcher function.
 * @param refreshInterval - Optional polling interval in milliseconds.
 *                         If provided, the data will be refreshed automatically.
 */
export default function useFetch<T>(fn: () => Promise<T>, refreshInterval?: number) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;

    const fetchData = () => {
      fn()
        .then((result) => {
          if (active) {
            setData(result);
            setError(null);
          }
        })
        .catch((err) => {
          if (active) {
            setError(err.message);
          }
        })
        .finally(() => {
          if (active) {
            setLoading(false);
          }
        });
    };

    fetchData();

    if (refreshInterval && refreshInterval > 0) {
      const interval = setInterval(fetchData, refreshInterval);
      return () => {
        active = false;
        clearInterval(interval);
      };
    }

    return () => {
      active = false;
    };
  }, [fn, refreshInterval]);

  return { data, error, loading };
}
