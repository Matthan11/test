# Hier nur Rollosteuerung

from logging_system import write_log
from utils import clamp


STEP = 5  # Prozent-Schritte

def control_shutter(room, handshape, user):
    """
    Steuerung des Rollos anhand der Handgesten
    room: Dictionary mit 'blind' und 'name'
    handshape: erkannte Geste
    user: aktueller Benutzer
    """
    if handshape == "thumb_up":
        room["blind"] = clamp(room["blind"] - STEP)  # hochfahren = kleiner Wert
        write_log(user, f"{room['name']}: Rollo auf {room['blind']} %")
    elif handshape == "thumb_down":
        room["blind"] = clamp(room["blind"] + STEP)  # runterfahren = größerer Wert
        write_log(user, f"{room['name']}: Rollo auf {room['blind']} %")
    elif handshape == "fist":
        room["blind"] = 0  # Rollo ganz auf
        write_log(user, f"{room['name']}: Rollo ganz auf")
    elif handshape == "pinky":
        room["blind"] = 100  # Rollo ganz zu
        write_log(user, f"{room['name']}: Rollo ganz zu")
