import math
import os
import pathlib
import random
import time
from datetime import datetime

import requests


def _load_env_file() -> None:
    """Load key=value pairs from simulation/.env into os.environ."""
    env_file = pathlib.Path(__file__).parent / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        # Only set vars that are not already in the environment
        os.environ.setdefault(key.strip(), value.strip())


def _load_zone_ids(api_base: str) -> list[int]:
    """Retrieve zone IDs from the backend if not provided."""
    response = requests.get(f"{api_base}/api/zones", timeout=10)
    response.raise_for_status()
    zones = response.json()
    return [zone["id"] for zone in zones]


def _generate_reading(zone_id: int) -> dict:
    """Generate a simulated environmental reading for a zone."""
    now = datetime.utcnow()
    hour = now.hour + now.minute / 60
    temp_base = 20 + 5 * math.sin((hour / 24) * 2 * math.pi)
    humidity_base = 55 + 10 * math.sin((hour / 24) * 2 * math.pi + 1)
    co2_base = 380 + 30 * math.sin((hour / 24) * 2 * math.pi + 2)
    energy_base = 120 + 40 * math.sin((hour / 24) * 2 * math.pi + 0.5)

    return {
        "zone_id": zone_id,
        "temperature": round(temp_base + random.uniform(-1.5, 1.5), 2),
        "humidity": round(humidity_base + random.uniform(-4, 4), 2),
        "co2_level": round(co2_base + random.uniform(-8, 8), 2),
        "energy_usage": round(energy_base + random.uniform(-12, 12), 2),
    }


def main() -> None:
    """Run the simulation loop."""
    _load_env_file()

    api_base = os.getenv("SIM_API_BASE_URL", "http://localhost:8000").rstrip("/")
    interval = float(os.getenv("SIM_INTERVAL_SECONDS", "5"))
    zone_ids_env = os.getenv("SIM_ZONE_IDS", "")
    auth_token = os.getenv("SIM_AUTH_TOKEN", "")

    if not auth_token:
        print("⚠️  WARNING: SIM_AUTH_TOKEN not set. POST /api/sensors requires authentication.")

    if zone_ids_env.strip():
        zone_ids = [int(zone_id) for zone_id in zone_ids_env.split(",") if zone_id.strip()]
    else:
        print(f"📡 Fetching zones from {api_base}/api/zones ...")
        zone_ids = _load_zone_ids(api_base)
        print(f"   Found zones: {zone_ids}")

    if not zone_ids:
        raise RuntimeError("No campus zones available for simulation.")

    headers = {"Content-Type": "application/json"}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    print(f"🚀 Simulator running — sending readings every {interval}s to {zone_ids} zones")
    cycle = 0
    while True:
        cycle += 1
        for zone_id in zone_ids:
            payload = _generate_reading(zone_id)
            response = requests.post(f"{api_base}/api/sensors", json=payload, headers=headers, timeout=10)
            response.raise_for_status()
        ts = datetime.utcnow().strftime("%H:%M:%S")
        print(f"  [{ts}] Cycle {cycle}: sent {len(zone_ids)} readings ✓")
        time.sleep(interval)


if __name__ == "__main__":
    main()
