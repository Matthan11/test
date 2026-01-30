# Hier nur Rollosteuerung

from logging_system import write_log
from utils import clamp_shutter

STEP = 5 # Umgerechnet sind das 10 %

def control_shutter(room, action, user):
    """
    Steuerung des Rollos anhand der Handgesten
    room: Dictionary mit 'blind' und 'name'
    handshape: erkannte Geste
    user: aktueller Benutzer
    """
    if action == "up":
        room.rollo_height = clamp_shutter(room.rollo_height - STEP)
    elif action == "down":
        room.rollo_height = clamp_shutter(room.rollo_height + STEP)
    elif action == "open":
        room.rollo_height = 0
    elif action == "close":
        room.rollo_height = 50
    write_log(user, f"{room.name}: Shutter {action}, now {room.rollo_height}%")