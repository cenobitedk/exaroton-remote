"""
Ensure only one instance of the app runs at a time.

The primary instance binds a local TCP socket. Any subsequent instance
connects to that socket, asks it to show its window, then exits.
"""
import socket
import sys
import threading

_PORT = 47832
_server_sock: socket.socket | None = None


def claim() -> bool:
    """
    Try to become the primary instance.
    Returns True if we are the primary instance, False if another is already running.
    On False the existing instance has already been asked to show its window.
    """
    global _server_sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
    try:
        sock.bind(("127.0.0.1", _PORT))
        sock.listen(5)
        _server_sock = sock
        return True
    except OSError:
        # Another instance is running — signal it and give up
        try:
            c = socket.create_connection(("127.0.0.1", _PORT), timeout=2)
            c.sendall(b"show\n")
            c.close()
        except Exception:
            pass
        return False


def start_listener(on_show: callable):
    """Start the background thread that listens for 'show' signals."""
    if _server_sock is None:
        return
    t = threading.Thread(target=_listen, args=(_server_sock, on_show), daemon=True)
    t.start()


def _listen(server_sock: socket.socket, on_show: callable):
    while True:
        try:
            conn, _ = server_sock.accept()
            data = conn.recv(16).decode(errors="ignore").strip()
            if data == "show":
                on_show()
            conn.close()
        except Exception:
            break
