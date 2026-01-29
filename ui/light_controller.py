# Hier nur die Lichtsteurung


from logging_system import write_log

STEP = 10 # Prozent-Schritte

def dim_up(self, user):
        self.light_level = min(100, self.light_level + STEP)
        write_log(user, f"{self.name}: Licht auf {self.light_level} %")

def dim_down(self, user):
        self.light_level = max(0, self.light_level - STEP)
        write_log(user, f"{self.name}: Licht auf {self.light_level} %")

def toggle_light(self, user):
    self.light_level = 100
    write_log(user, f"{self.name}: Licht auf 100 %")