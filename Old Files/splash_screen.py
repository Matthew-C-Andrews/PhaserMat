# MAKE SURE PYGAME IS INSTALLED IN SOME WAY
import pygame
import time

# Initialize Pygame
pygame.init()

WAITING_INTERVAL = 3 #the amount of seconds the splash screen is displayed for.
# Set up the display
screen = pygame.display.set_mode((1920, 1080))  # You can adjust the size as needed
pygame.display.set_caption("Display Logo for 3 Seconds")
clock = pygame.time.Clock()

# Load the logo
logo = pygame.image.load("logo.jpg")

#image was too big so im scaling it
logo_scaled = pygame.transform.scale(logo, (1920, 1080))
start = pygame.time.get_ticks()
# Display the Splash Screenrunning = True
splashDisplay = True
while splashDisplay:
    screen.blit(logo_scaled, (0, 0))  #this is the position of the image
    pygame.display.flip()
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            splashDisplay = False
    # Check if 3 seconds have passed (3000 milliseconds)
    if pygame.time.get_ticks() - start > 3000:
        splashDisplay = False
clock.tick(60)
#the screen will close after this because it needs the player screen next






