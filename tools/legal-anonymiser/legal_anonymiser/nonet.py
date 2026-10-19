"""Garde reseau : coupe les connexions sortantes du processus.

Filet dans le processus, pas une garantie : du code natif ou un sous-processus
peut l'ignorer. L'isolation reelle vient du conteneur sans reseau.
"""
import socket


class NetworkBlocked(OSError):
    """Levee a toute tentative d'acces reseau."""


def _blocked(*_args, **_kwargs):
    raise NetworkBlocked("Acces reseau interdit : l'anonymiseur fonctionne hors ligne.")


class _OfflineSocket(socket.socket):
    connect = _blocked
    connect_ex = _blocked
    sendto = _blocked


def install() -> None:
    """Remplace les points d'entree reseau de `socket`. Idempotent."""
    if socket.socket is _OfflineSocket:
        return
    socket.socket = _OfflineSocket
    socket.create_connection = _blocked
    socket.getaddrinfo = _blocked
