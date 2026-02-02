# Gesture Control Smart Home – Schulprojekt IT

## Projektbeschreibung
Dieses Projekt simuliert eine Smart-Home-Steuerung mittels Handgesten.
Über eine Webcam werden Gesten erkannt, mit denen Benutzer, Räume,
Licht und Rollos gesteuert werden können.

## Verwendete Technologien
- Python 3
- Pygame (UI)
- OpenCV (Kamera)
- MediaPipe (Handtracking)

## Programmstruktur
- main.py → Hauptprogramm
- config.py → Einstellungen & Konstanten
- utils.py → Hilfsfunktionen
- logging_system.py → CSV-Logging
- vision/ → Handtracking & State-Machine
