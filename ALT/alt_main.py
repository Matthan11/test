
# import pygame
# import config
# from ui.base_widget import create_rooms
# from logging_system import write_log
# from vision.hand_tracking_neu import get_gesture_action
# from ui.light_controller import control_light
# from ui.shutter_controller import control_shutter



# def main():
#     pygame.init()

#     # Fenster
#     screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
#     pygame.display.set_caption(config.WINDOW_TITLE)

#     font = pygame.font.SysFont(None, config.FONT_SIZE)
#     clock = pygame.time.Clock()

#     current_user = config.DEFAULT_USER
#     selected_room = None

#     # Räume erzeugen
#     rooms = create_rooms()

#     # Hauptloop
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#             current_user, selected_room, handshape = get_gesture_action(
#                 current_user, selected_room
#             )

#             if handshape and selected_room:
#                 room = rooms[selected_room]

#             control_light(room, handshape, current_user)
#             control_shutter(room, handshape, current_user)

#             # # Benutzer wechseln    
#             # elif target == "user":
#             #         current_user = action
#             #         write_log(current_user, f"Benutzer gewechselt zu {current_user}")

#         # Bildschirm JEDEN FRAME neu zeichnen
#         screen.fill(config.BACKGROUND)
#         for room in rooms.values():
#             room.draw(screen, font)

#         # Benutzer anzeigen
#         user_text = font.render(f"Aktueller Benutzer: {current_user}", True, (255, 255, 255))
#         screen.blit(user_text, (20, 20))

#         pygame.display.flip()
#         clock.tick(config.FPS)

#     pygame.quit()


# if __name__ == "__main__":
#     main()