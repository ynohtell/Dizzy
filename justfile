# --- NATIVE COMMANDS (Fast, for "Vibecoding" and logic) ---

# Run backend: Move into the folder and start uvicorn
backend:
    cd backend && uv run uvicorn main:app --reload --port 8000

# Run frontend natively with pnpm
frontend:
	cd frontend && pnpm run dev


# Run BOTH: Uses concurrently to show both logs in one window
dev:
    @pnpm exec concurrently \
      --names "BACK,FRONT" \
      --prefix-colors "blue,magenta" \
      --kill-others \
      "just backend" \
      "just frontend"

kill:
	@echo "Killing processes on ports 8000 and 5173..."
	-fuser -k 8000/tcp
	-fuser -k 5173/tcp


# The "Restart" maneuver: Stops everything and starts fresh
restart:
	just stop
	just dev


# --- DOCKER COMMANDS (Cloud/DevOps Practice) ---

# Test the full "Cloud" setup
cloud-dev:
    docker compose up --build

# Check if the containerized versions work
cloud-stop:
    docker compose down