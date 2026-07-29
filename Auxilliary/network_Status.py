# network_status.py

import socket

def is_online(host="8.8.8.8", port=53, timeout=3):
    """
    Returns True if an internet connection is available, otherwise False.

    Args:
        host (str): Host to test against (default: Google's DNS).
        port (int): Port number (default: 53).
        timeout (int): Timeout in seconds.

    Returns:
        bool
    """
    try:
        socket.setdefaulttimeout(timeout)
        with socket.create_connection((host, port)):
            return True
    except OSError:
        return False


def get_status():
    """Returns 'Online' or 'Offline'."""
    return "Online" if is_online() else "Offline"


if __name__ == "__main__":
    print(get_status())
