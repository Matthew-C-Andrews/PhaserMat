import pygame

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Team Interface")

# Colors
GREEN = (0, 128, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Timer settings
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    screen.fill(BLACK)
    
    # Draw green box (left side)
    pygame.draw.rect(screen, GREEN, (0, 0, WIDTH // 3, HEIGHT))
    
    # Draw red box (right side)
    pygame.draw.rect(screen, RED, (WIDTH * 2 // 3, 0, WIDTH // 3, HEIGHT))
    
    # Draw team labels
    green_team_text = font.render("Green Team", True, WHITE)
    screen.blit(green_team_text, (WIDTH // 6 - 75, 20))
    
    red_team_text = font.render("Red Team", True, WHITE)
    screen.blit(red_team_text, (WIDTH * 5 // 6 - 50, 20))
    
    # Draw black screen in the middle (automatically black due to screen.fill(BLACK))
    
    # Draw timer at the bottom
    timer_text = font.render(f"Timer", True, WHITE)
    screen.blit(timer_text, (WIDTH // 2 - 40, HEIGHT - 40))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update display
    pygame.display.flip()

pygame.quit()