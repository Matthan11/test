# def clamp(value):
#     return max(0, min(100, value))

# def control_light(room, handshape):
#     if handshape == "index_middle":
#         room["light"] = clamp(room["light"] + 10)
#     elif handshape == "middle":
#         room["light"] = clamp(room["light"] - 10)
#     elif handshape == "open":
#         room["light"] = 100
#     elif handshape == "fist":
#         room["light"] = 0

# def control_blind(room, handshape):
#     if handshape == "thumb_up":
#         room["blind"] = clamp(room["blind"] + 10)
#     elif handshape == "thumb_index":
#         room["blind"] = clamp(room["blind"] - 10)
#     elif handshape == "index":
#         room["blind"] = 100
#     elif handshape == "pinky":
#         room["blind"] = 0
