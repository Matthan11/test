def handle_room_selection(handshape, selected_room):
    if selected_room is None:
        if handshape == "index":
            print("Raum 1 ausgewählt")
            return "Raum 1"
        elif handshape == "thumb_up":
            print("Raum 2 ausgewählt")
            return "Raum 2"
    return selected_room
