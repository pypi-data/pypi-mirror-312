import os
import socket
import subprocess
import sys
import threading
from logging import getLogger
from pathlib import Path
from typing import Literal

from uvicorn import Config, Server

logger = getLogger(__name__)

def is_port_in_use(port: int) -> bool:
    """Check if a port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0
    

def start_server(port: int = 8000, method: Literal["new_terminal", "same_terminal"] = "new_terminal") -> None:
    print("Start server called with method: ", method)
    if is_port_in_use(port):
        print("Server is already running.")
        return
    if method == "new_terminal":
        _start_server_in_new_terminal(port)
    elif method == "same_terminal":
        _start_server_in_same_terminal(port)
    else:
        print(f"Invalid method: {method}")


def _start_server_in_new_terminal(port: int = 8000):
    """Starts the server in a new terminal."""
    path_uvicorn="uvicorn"
    if os.name == "nt":
        path_uvicorn=os.path.dirname(sys.executable)
        path_uvicorn=path_uvicorn.replace("\\","/")
        path_uvicorn+="/Scripts/uvicorn.exe"
        if not os.path.isfile(path_uvicorn):
            path_uvicorn="uvicorn"
    command = f"{path_uvicorn} main:app --port {port}"
    path = Path(__file__).parent
    server_process = subprocess.Popen(['cmd.exe', '/c', f'start', 'cmd', '/k', command], cwd=path)

if __name__ == "__main__":
    start_server()


def _start_server_in_same_terminal(port: int = 8000) -> None:
    """Starts the server in a separate thread."""
    def run_server():
        """Internal function to configure and run the Uvicorn server."""

        upper_folder = Path(__file__).parent
        sys.path.append(str(upper_folder))
        config = Config(app="main:app", port=port)
        server = Server(config)

        try:
            server.run()
        except Exception as e:
            print(f"Error: {e}")
    
    # Start the server in a new daemon thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.daemon = True
    server_thread.start()

    print("Server started on a separate thread.")