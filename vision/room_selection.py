# from logging_system import write_log

# def handle_room_selection(handshape, selected_room, user=None):
#     # Nur auswählen, wenn noch kein Raum aktiv ist
#     if selected_room is None:
#         # Neue Raumwahl
#         if handshape == "fist":
#             write_log(user, "Raumauswahl zurückgesetzt")
#             return None
        
#         # Wahl Raum 1
#         if handshape == "index":
#             new_room = "Raum 1"
#             write_log(user, f"Raum gewechselt zu {new_room}")
#             print("Raum 1 ausgewählt")
#             return new_room

#         # Wahl Raum 2
#         elif handshape == "thumb_up":
#             new_room = "Raum 2"
#             write_log(user, f"Raum gewechselt zu {new_room}")
#             print("Raum 2 ausgewählt")
#             return new_room

#     return selected_room