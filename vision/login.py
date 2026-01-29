def handle_login(handshape, current_user):
    users = {
        "Benutzer 1": "open",
        "Benutzer 2": "fist"
    }

    if current_user is None:
        for user, gesture in users.items():
            if handshape == gesture:
                print(f"{user} eingeloggt")
                return user
    return current_user
