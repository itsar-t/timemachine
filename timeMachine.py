import sys
import pygame
from pygame.locals import *
from ai_engine import get_ai_facts

# ---------------------------
# Pygame setup
# ---------------------------

pygame.init()
pygame.mixer.init()

display_info = pygame.display.Info()
screen_width = int(display_info.current_w // 1.5)
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Time Machine")

# ---------------------------
# Fonts and colors
# ---------------------------

base_font = pygame.font.Font(None, 32)
label_font = pygame.font.Font(None, 40)
hint_font = pygame.font.Font(None, 24)

color_active = pygame.Color("lightskyblue3")
color_passive = pygame.Color("gray15")
text_color = (255, 255, 255)
hint_color = (200, 200, 200)

# ---------------------------
# Input box and static labels
# ---------------------------

user_text = ""

# Input box sits roughly in the upper-middle of the screen
input_rect = pygame.Rect(
    screen_width // 4,
    screen_height // 4 + 60,
    screen_width // 2,
    32,
)
active = False
input_color = color_passive

# Main title at the top
title_text = label_font.render("Time Machine", True, text_color)
title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 6))

# Prompt above the input box
prompt_text = base_font.render(
    "Type a year, person, book, film or event:",
    True,
    text_color,
)
prompt_rect = prompt_text.get_rect(topleft=(input_rect.x, input_rect.y - 30))

# Hint under the input box
hint_text = hint_font.render(
    "Press Enter to search – Use UP / DOWN to scroll",
    True,
    hint_color,
)
hint_rect = hint_text.get_rect(midtop=(screen_width // 2, input_rect.bottom + 10))

# Everything below this y-coordinate is reserved for the scrollable results
results_area_top = hint_rect.bottom + 20

# ---------------------------
# Background and sound
# ---------------------------

background_image = pygame.image.load("bilder/timemachine.png").convert_alpha()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
background_image.set_alpha(int(255 * 0.3))

time_travel_sound = pygame.mixer.Sound("ljud/time_travel.mp3")

# ---------------------------
# Result handling
# ---------------------------

events_to_display: list[str] = []
scroll_y = 0  # Offset for vertical scrolling inside the results area
results_label_surf = None  # "Results for: <query>" label


def render_text_wrapped(
    text: str,
    font: pygame.font.Font,
    color,
    x: int,
    y: int,
    max_width: int,
    surface: pygame.Surface,
) -> int:
    """
    Render a long string as multiple lines so that it fits within max_width.
    Returns the new y-position after the last line has been drawn.
    """
    words = text.split(" ")
    line = ""
    line_height = font.get_linesize()

    for word in words:
        test_line = line + word + " "
        if font.size(test_line)[0] <= max_width:
            line = test_line
        else:
            surface.blit(font.render(line, True, color), (x, y))
            y += line_height
            line = word + " "

    if line:
        surface.blit(font.render(line, True, color), (x, y))
        y += line_height

    return y


# ---------------------------
# Main event loop
# ---------------------------

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == MOUSEBUTTONDOWN:
            # Toggle active state for the input box
            if input_rect.collidepoint(event.pos):
                active = not active
            else:
                active = False
            input_color = color_active if active else color_passive

        elif event.type == KEYDOWN:
            if active:
                if event.key == K_RETURN:
                    query = user_text.strip()
                    if query:
                        try:
                            # Ask the AI for historical bullet points
                            events_to_display = get_ai_facts(query)

                            # Play the time travel sound if we actually got something back
                            if events_to_display:
                                time_travel_sound.play()

                            results_label_surf = base_font.render(
                                f"Results for: {query}",
                                True,
                                text_color,
                            )
                            # Reset scroll whenever a new search is performed
                            scroll_y = 0

                        except Exception as e:
                            events_to_display = [
                                "Something went wrong when contacting The Archivist.",
                                f"Technical info: {e}",
                            ]
                            results_label_surf = base_font.render(
                                "Error",
                                True,
                                (255, 100, 100),
                            )
                            scroll_y = 0

                        # Clear the input field after the search
                        user_text = ""

                elif event.key == K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

            # Arrow keys scroll the results area
            if event.key == K_UP:
                # Prevent scrolling past the initial top position
                scroll_y = min(scroll_y + 20, 0)
            elif event.key == K_DOWN:
                # Scroll down; no strict bottom limit for now
                scroll_y -= 20

    # -----------------------
    # Drawing
    # -----------------------

    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))

    # Title
    screen.blit(title_text, title_rect)

    # Results label just under the title, if available
    if results_label_surf is not None:
        results_rect = results_label_surf.get_rect(
            center=(screen_width // 2, title_rect.bottom + 20)
        )
        screen.blit(results_label_surf, results_rect)

    # Prompt and input box
    screen.blit(prompt_text, prompt_rect)

    input_text_surface = base_font.render(user_text, True, text_color)
    screen.blit(input_text_surface, (input_rect.x + 5, input_rect.y + 5))
    pygame.draw.rect(screen, input_color, input_rect, 2)

    # Hint text under the input box
    screen.blit(hint_text, hint_rect)

    # -----------------------
    # Scrollable results area
    # -----------------------

    # Create a separate transparent surface for the scrollable content.
    # Anything drawn above y=0 in this surface is visible; anything below is clipped.
    results_height = screen_height - results_area_top
    results_surface = pygame.Surface((screen_width, results_height), pygame.SRCALPHA)

    max_width = screen_width - 100
    y = scroll_y  # Start drawing at the current scroll offset

    for event_text in events_to_display:
        y = render_text_wrapped(
            event_text,
            base_font,
            text_color,
            50,
            y,
            max_width,
            results_surface,
        )
        y += 10  # Extra spacing between bullet points

    # Blit the scrollable surface at the defined top region
    screen.blit(results_surface, (0, results_area_top))

    pygame.display.flip()

pygame.quit()
sys.exit()
