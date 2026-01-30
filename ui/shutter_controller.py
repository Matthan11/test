# Hier nur Rollosteuerung

from logging_system import write_log
from ALT.hand_tracking_alt import clamp

STEP = 5 # Umgerechnet sind das 10 %

# def rollo_up(self, user):
#         self.rollo_height = max(0, self.rollo_height - STEP)
#         write_log(user, f"{self.name}: Rollo auf {self.rollo_height} %")

# def rollo_down(self, user):
#         self.rollo_height = min(self.window.height, self.rollo_height + STEP)
#         write_log(user, f"{self.name}: Rollo auf {self.rollo_height} %")

# def toggle_close(self,user):
#         self.rollo_height = self.window.height
#         write_log(user, f"{self.name}: Rollo auf 100 %")


def control_shutter(self, handshape, user):
    if handshape == "thumb_up":
        self["blind"] = clamp(self["blind"] + STEP)
        write_log(user, f"{self.name}: Rollo auf {self.rollo_height} %")

    elif handshape == "thumb_index":
        self["blind"] = clamp(self["blind"] - STEP)
        write_log(user, f"{self.name}: Rollo auf {self.rollo_height} %")

    elif handshape == "index":
        self["blind"] = 100
        write_log(user, f"{self.name}: Rollo auf {self.rollo_height} %")

    elif handshape == "pinky":
        self["blind"] = 0
        write_log(user, f"{self.name}: Rollo auf {self.rollo_height} %")