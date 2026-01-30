# Hier nur die Lichtsteurung

from logging_system import write_log
from utils import clamp


STEP = 10  # Prozent-Schritte


def control_light(room, action, user):
    """
    Steuerung des Lichts anhand der Handgesten
    room: Dictionary mit 'light' und 'name'
    handshape: erkannte Geste
    user: aktueller Benutzer
    """
    if action == "up":
        room["light"] = clamp(room["light"] + 10)
    elif action == "down":
        room["light"] = clamp(room["light"] - 10)
    elif action == "on":
        room["light"] = 100
    elif action == "off":
        room["light"] = 0
    write_log(user, f"{room['name']}: Licht {action}, jetzt {room['light']}%")