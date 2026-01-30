# Hier nur die Lichtsteurung

from ALT.hand_tracking_alt import clamp
from logging_system import write_log


STEP = 10 # Prozent-Schritte

# def dim_up(self, user):
#         self.light_level = min(100, self.light_level + STEP)
#         write_log(user, f"{self.name}: Licht auf {self.light_level} %")

# def dim_down(self, user):
#         self.light_level = max(0, self.light_level - STEP)
#         write_log(user, f"{self.name}: Licht auf {self.light_level} %")

# def toggle_light(self, user):
#     self.light_level = 100
#     write_log(user, f"{self.name}: Licht auf 100 %")

def control_light(self, handshape, user):
        if handshape == "index_middle":
                self["light"] = clamp(self["light"] + STEP)
                write_log(user, f"{self.name}: Licht auf {self.light_level} %")


        elif handshape == "middle":
                self["light"] = clamp(self["light"] - STEP)
                write_log(user, f"{self.name}: Licht auf {self.light_level} %")

        elif handshape == "open":
                self["light"] = 100
                write_log(user, f"{self.name}: Licht auf {self.light_level} %")

        elif handshape == "fist":
                self["light"] = 0
                write_log(user, f"{self.name}: Licht auf {self.light_level} %")