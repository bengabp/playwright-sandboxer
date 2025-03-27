# Sandbox
Initialize & Manage multiple playwright sandboxes.

# Building the sandbox image
The sandbox image contains code that automates playwright and wraps its dependencies together. A (base image)[https://hub.docker.com/r/bengabp/sandbox] has been used which has poetry, playwright and important packages installed. This also reduces the time it takes for the sb image to build and helps you focus on sandbox code dependencies.

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

## Reactjs Client Connection
```typescript
// Sandbox.tsx
import React from 'react';
import { useEffect, useRef, useState } from "react";

const WS_URL = "ws://localhost:3001"; // WebSocket server running in Docker
const VNC_URL = "http://localhost:6080/vnc.html"; // noVNC server

const Sandbox: React.FC = () => {
    const ws = useRef<WebSocket | null>(null);
    const [connected, setConnected] = useState(false);
  
    useEffect(() => {
      ws.current = new WebSocket(WS_URL);
      ws.current.onopen = () => {
        console.log("Connected to WebSocket server");
        setConnected(true);
      };
      ws.current.onclose = () => {
        console.log("WebSocket disconnected");
        setConnected(false);
      };
      ws.current.onerror = (error) => {
        console.error("WebSocket error:", error);
      };
      return () => {
        ws.current?.close();
      };
    }, []);
  
    return (
      <div style={{ textAlign: "center" }}>
        <h2>Remote Browser Control</h2>
        <p>Status: {connected ? "🟢 Connected" : "🔴 Disconnected"}</p>
        <iframe
          src={VNC_URL}
          width="1920px"
          height="1080px"
          style={{ border: "1px solid black" }}
        />
      </div>
    );
}
export default Sandbox;
```

# Api
The purpose of the api is to manage sandbox instances and dynamic code injection for new sandboxes.

## Tech stack
- Fastapi & Sqlalchemy - Backend & ORM
- Alembic - Database migrations
- Postgres via NeonDb - Database

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

