import multiprocessing
from loguru import logger

def run_in_background(cmd):
    def run():
        import subprocess
        p = subprocess.Popen(cmd, shell=True)
        p.wait()

    p = multiprocessing.Process(target=run, daemon=True)
    p.start()
    p.join(timeout=3)
    if p.is_alive():
        logger.debug("Background process is running")
    else:
        logger.debug("Background process failed to start")

if __name__=="__main__":
    run_in_background("x11vnc -display :99 -forever -shared -nopw -ncache -rfbport 5900")
