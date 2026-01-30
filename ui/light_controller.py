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
        room.light_level = clamp(room.light_level + 10)
    elif action == "down":
        room.light_level = clamp(room.light_level - 10)
    elif action == "on":
        room.light_level = 100
    elif action == "off":
        room.light_level = 0
    write_log(user, f"{room.name}: Licht {action}, jetzt {room.light_level}%")