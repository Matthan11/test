# from logging_system import write_log

# def handle_login(handshape, current_user):
#     users = {
#         "Benutzer 1": "open",
#         "Benutzer 2": "fist"
#     }

#     if current_user is None:
#         for user, gesture in users.items():

#             # Abmelden des Users
#             if handshape == "pinky" and current_user is not None:
#                 write_log(current_user, f"{current_user} ausgeloggt")
#                 print(f"{current_user} ausgeloggt")
#                 return None
            
#             # User Auswahl
#             if handshape == gesture:
#                 print(f"{user} eingeloggt")
#                 write_log(user, f"Benutzer gewechselt zu {user}")
#                 return user
            
#     return current_user
