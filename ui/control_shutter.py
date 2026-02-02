# Erstellt von Jannik Langhammer
# Hier nur Rollosteuerung

from logging_system import write_log
from ui.utils import clamp_shutter

STEP = 5 # Umgerechnet sind das 10 %

def control_shutter(room, action, user):
    """
    Steuerung des Rollos anhand der Handgesten
    room: Dictionary mit 'blind' und 'name'
    handshape: erkannte Geste
    user: aktueller Benutzer
    """
    if action == "up":                                                              # wenn Aktion up, dann Rollo einen Step hochfahren
        room.rollo_height = clamp_shutter(room.rollo_height - STEP)
    elif action == "down":                                                          # wenn Aktion down, dann Rollo einen Step runterfahren
        room.rollo_height = clamp_shutter(room.rollo_height + STEP)
    elif action == "open":                                                          # wenn Aktion open, dann Rollo komplett auf fahren
        room.rollo_height = 0
    elif action == "close":                                                         # wenn Aktion close, dann Rollo komplett zu 
        room.rollo_height = 50
    write_log(user, f"{room.name}: Shutter {action}, now {room.rollo_height}%")