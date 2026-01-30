# Hier nur die Lichtsteurung

from logging_system import write_log
from utils import clamp


STEP = 10  # Prozent-Schritte

def control_light(room, handshape, user):
    """
    Steuerung des Lichts anhand der Handgesten
    room: Dictionary mit 'light' und 'name'
    handshape: erkannte Geste
    user: aktueller Benutzer
    """
    if handshape == "thumb_up":
        room["light"] = clamp(room["light"] + STEP)
        write_log(user, f"{room['name']}: Licht auf {room['light']} %")
    elif handshape == "thumb_down":
        room["light"] = clamp(room["light"] - STEP)
        write_log(user, f"{room['name']}: Licht auf {room['light']} %")
    elif handshape == "fist":
        room["light"] = 0
        write_log(user, f"{room['name']}: Licht aus")
    elif handshape == "pinky":
        room["light"] = 100
        write_log(user, f"{room['name']}: Licht an")
