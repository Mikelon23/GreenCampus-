# Deployment Notes

## Backend (Render/Railway)

- Build command: `pip install -r backend/requirements.txt`
- Start command: `uvicorn backend.main:app --host 0.0.0.0 --port 8000`
- Environment variables:
  - `DATABASE_URL`
  - `JWT_SECRET`
  - `JWT_ALGORITHM`
  - `ACCESS_TOKEN_EXPIRE_MINUTES`

## Frontend (Vercel)

- Root directory: `frontend/`
- Build command: `npm run build`
- Output: Next.js default
- Environment variable:
  - `NEXT_PUBLIC_API_BASE_URL`

## Database (Supabase)

- Use Supabase PostgreSQL and set `DATABASE_URL`.
- Apply migrations using Alembic:
  - `alembic -c backend/alembic.ini upgrade head`

## Docker

- Backend image: `infrastructure/docker/Dockerfile.backend`
- Frontend image: `infrastructure/docker/Dockerfile.frontend`
