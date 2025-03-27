# Sandbox

Initialize & Manage multiple playwright sandboxes.

## Running playwright in a sandbox

```bash
# Start xvfb virtual display server, you have to wait a bit for the server to startup
Xvfb :99 -screen 0 1920x1080x24 &

# Set the DISPLAY environment variable
export DISPLAY=:99

# Start the VNC server with x11vnc
x11vnc -display :99 -forever -shared -nopw -rfbport 5900 &

# Start websockify to convert VNC to WebSocket (for noVNC)
websockify --web /usr/share/novnc 6080 localhost:5900 &

# Finally, start your playwright automator, remember to set playwright to not run in headless mode
# Node js playwright
node /app/server.js

# Python script
python3 /app/server.py
```

## Running alembic migration
```bash
# Init alembic
alembic init alembic

# generate migration scripts
alembic revision --autogenerate -m "optional custom name"

# Apply migration
poetry run alembic upgrade head
```

## Running the api
```bash
# Install dependencies
poetry update

# Run api
uvicorn sandbox.main:app --host 0.0.0.0
```

# Building the sandbox image
The sandbox image contains code that automates playwright and wraps its dependencies together. A base image has been used which has poetry, playwright and important packages installed. This also reduces the time it takes for the sb image to build and helps you focus on sandbox code dependencies.

## Libraries in base image
- x11vnc
- xvfb
- poetry
- playwright (with system dependencies and browsers installed)
- python 3.11
- novnc
- websockify

You can extend the base image to install additional system dependencies and packages

```bash
# Building base image
docker buildx build -t docker.io/<YOUR-DOCKER-HUB-USERNAME>/sandbox:base

# Building sb(sandbox) image
docker buildx build -t sb .
```

