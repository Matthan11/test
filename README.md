
# Gesture-Controlled Smart Home Simulation

**Erstellt von:**
Jannik Langhammer & Nico Lippl

Dieses Projekt ist eine interaktive Smart-Home-Simulation, die mithilfe von Handgesten über eine Webcam gesteuert wird.
Unter Verwendung von MediaPipe, OpenCV und Pygame können Benutzer Räume auswählen und dort Licht sowie Rollos kontaktlos steuern.

---

## Projektübersicht

Das Programm simuliert zwei Räume:

* Kitchen
* Sleepingroom

Jeder Raum besitzt:

* ein Fenster mit Rollo
* eine Lichtquelle mit dimmbarer Helligkeit
* einfache Möbel zur besseren Visualisierung

Die komplette Bedienung erfolgt über Handgesten.

---

## Grundidee und Aufbau

Das Projekt ist modular aufgebaut und trennt klar:

* Programmlogik
* Benutzeroberfläche (UI)
* Gestenerkennung
* Konfiguration
* Logging

Die Steuerung erfolgt über eine zentrale State-Machine, die abhängig vom aktuellen Zustand unterschiedliche Gesten interpretiert.

---

## Programmstart (`main.py`)

`main.py` ist der Einstiegspunkt des Programms.

Aufgaben:

* Initialisierung von Pygame, Fenster, Schrift und Clock
* Öffnen der Webcam (ausschließlich in dieser Datei)
* Erzeugen der Räume
* Laden und Verwalten der Avatare
* Zentrale Hauptschleife
* Anzeigen des Live-Kamerabildes
* Übergabe jedes Kamera-Frames an die Gestenlogik

---

## Avatare (`avatars.py`)

Jeder Benutzer wird durch einen Avatar dargestellt.

Eigenschaften:

* Name
* Farbe
* Stil (hair oder cap)
* Aktiv-Status

Der aktuell aktive Benutzer wird visuell hervorgehoben.

---

## Räume und UI (`base_widget.py`)

Die Klasse `Room` beschreibt einen Raum mit:

* Wänden und Boden
* Fenster und Rollo
* Lichtstärke (0–100 %)
* Möbeln abhängig vom Raumtyp

Die Funktion `create_rooms()` erzeugt:

* Kitchen
* Sleepingroom

---

## Hand- und Gestenerkennung (`hand_tracking.py`)

Dieses Modul übernimmt die komplette Gestensteuerung.

Verwendete Technologien:

* MediaPipe Hands
* OpenCV

Funktionen:

* Erkennung einzelner Finger
* Ableitung einer Handgeste (Handshape)
* Umsetzung der Gesten in Aktionen
* Verwaltung der State-Machine
* Cooldown-System gegen Mehrfachauslösungen
* Logging aller Aktionen

---

## State-Machine (Zustände)

| Zustand         | Beschreibung                     |
| --------------- | -------------------------------- |
| USER_SELECT     | Benutzerauswahl                  |
| ROOM_SELECT     | Raumauswahl                      |
| CONTROL_SELECT  | Auswahl zwischen Licht und Rollo |
| LIGHT_CONTROL   | Lichtsteuerung                   |
| SHUTTER_CONTROL | Rollosteuerung                   |

---

## Gestensteuerung (Auswahl)

### Benutzer auswählen

* Zeigefinger → User 1
* Zeige- und Mittelfinger → User 2

### Raum auswählen

* Zeigefinger → Kitchen
* Zeige- und Mittelfinger → Sleepingroom
* Daumen + Mittel- + Kleinerfinger → Zurück

### Lichtsteuerung

* Zeigefinger → Licht heller
* Zeige- und Mittelfinger → Licht dunkler
* Alle Finger → Licht aus
* Kleinerfinger → Licht an

### Rollosteuerung

* Zeigefinger → Rollo hoch
* Zeige- und Mittelfinger → Rollo runter
* Alle Finger → Rollo vollständig offen
* Kleinerfinger → Rollo vollständig geschlossen

---

## Lichtsteuerung (`control_light.py`)

* Dimmen in 10-Prozent-Schritten
* Maximalwert: 100 %
* Minimalwert: 0 %
* Jede Änderung wird im Log gespeichert

---

## Rollosteuerung (`control_shutter.py`)

* Steuerung der Rollo-Höhe
* Begrenzung der Werte über `clamp_shutter()`
* Jede Aktion wird protokolliert

---

## Logging (`logging_system.py`)

Alle Benutzeraktionen werden in CSV-Dateien gespeichert.

* Speicherort: Ordner `logs/`
* Eine Datei pro Tag
* Enthaltene Informationen:

  * Benutzer
  * Aktion
  * Datum
  * Uhrzeit

---

## Konfiguration (`config.py`)

Zentrale Konfigurationsdatei für:

* Fenstergröße
* Bildrate (FPS)
* Farben
* Schriftgröße
* Fenstertitel

Dies sorgt für eine saubere Trennung von Logik und Einstellungen.

---

## Hilfsfunktionen (`utils.py`)

* `clamp_light()` begrenzt die Lichtwerte
* `clamp_shutter()` begrenzt die Rollo-Werte

---

## Live-Kamera (`live_camera.py`)

Optionales Test- und Debug-Modul:

* Anzeige des Kamerabildes mit eingezeichneten Hand-Landmarks
* Wird nicht im Hauptprogramm benötigt