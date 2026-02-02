# Erstellt von Jannik Langhammer
# Hier werden nur die Minimal und Maximal werte definiert, welche für die Steuerungen benutzt werden

def clamp_shutter(value):   # Maximal und Minimal wert des Rollos 
    return max(0, min(50, value))

def clamp_light(value):   # Maximal und Minimal wert des Rollos 
    return max(0, min(100, value))