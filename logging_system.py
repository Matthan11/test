import csv
from datetime import datetime
import os

LOG_ORDNER = "logs"

def write_log(user, action):
    if not os.path.isdir(LOG_ORDNER):
        os.makedirs(LOG_ORDNER)

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    filename = os.path.join(LOG_ORDNER, f"{date}.csv")
    file_exist = os.path.isfile(filename)

    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exist:
            writer.writerow(["UserLogin", "Aktion", "Datum", "Zeit"])

        writer.writerow([user, action, date, time])
