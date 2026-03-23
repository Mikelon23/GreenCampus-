#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is required."
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "docker compose (v2) is required."
  exit 1
fi

if [[ ! -f ".env" ]]; then
  echo "No .env found. Creating one from .env.example ..."
  cp .env.example .env
fi

echo "[1/4] Building images..."
docker compose build

echo "[2/4] Starting database..."
docker compose up -d db

echo "[3/4] Running migrations + seed (backend-init)..."
docker compose up --no-deps --abort-on-container-exit backend-init

echo "[4/4] Starting backend + frontend..."
docker compose up -d backend frontend

echo ""
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8000 (Swagger: /docs)"

