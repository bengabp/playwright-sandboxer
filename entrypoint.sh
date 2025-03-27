echo "Starting xdisplay server"
Xvfb :99 -screen 0 1920x1080x24 &
# sleep 30

echo "Starting x11 vnc server"
python3 -m sandbox.sb.scripts.run_x11

echo "Starting websockify server"
websockify --web /usr/share/novnc 6080 localhost:5900 &

echo "Running automate script"
python3 -m sandbox.sb.automate
