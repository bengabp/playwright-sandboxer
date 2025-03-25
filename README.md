# Playwright Sandboxer

Initialize & Manage multiple playwright sandboxes.

## Running playwright in a sandbox

Start xvfb virtual display server, you have to wait a bit for the server to startup
```bash
Xvfb :99 -screen 0 1920x1080x24 &
```

Set the DISPLAY environment variable
```bash
export DISPLAY=:99
```

Start the VNC server with x11vnc
```bash
x11vnc -display :99 -forever -shared -nopw -rfbport 5900 &
```

Start websockify to convert VNC to WebSocket (for noVNC)
```bash
websockify --web /usr/share/novnc 6080 localhost:5900 &
```

Finally, start your playwright automator, remember to set playwright to not run in headless mode
```bash
# Node js playwright
node /app/server.js

# Python script
python3 /app/server.py
```

