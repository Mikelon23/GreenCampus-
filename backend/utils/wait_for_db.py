from __future__ import annotations

import os
import time
from urllib.parse import urlparse

import psycopg2


def _connect_once(database_url: str) -> None:
    parsed = urlparse(database_url)
    if parsed.scheme not in ("postgresql", "postgres"):
        raise RuntimeError("DATABASE_URL must be a PostgreSQL URL")

    host = parsed.hostname or "localhost"
    port = parsed.port or 5432
    user = parsed.username or "postgres"
    password = parsed.password or ""
    dbname = (parsed.path or "").lstrip("/") or "postgres"

    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname=dbname,
        connect_timeout=3,
    )
    conn.close()


def main() -> int:
    database_url = os.getenv("DATABASE_URL", "").strip()
    if not database_url:
        raise RuntimeError("DATABASE_URL is required")

    timeout_seconds = int(os.getenv("DB_WAIT_TIMEOUT_SECONDS", "60"))
    start = time.time()
    last_error: Exception | None = None

    while time.time() - start < timeout_seconds:
        try:
            _connect_once(database_url)
            print("[wait_for_db] Database is ready.")
            return 0
        except Exception as exc:  # pragma: no cover
            last_error = exc
            print("[wait_for_db] Waiting for database...")
            time.sleep(2)

    raise RuntimeError(f"Database not ready after {timeout_seconds}s: {last_error}")


if __name__ == "__main__":
    raise SystemExit(main())

