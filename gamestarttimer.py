import pygame
import os

def load_images():
    images = {}
    for i in range(31):  # 0 to 30
        filename = f"countdown_images/{i}.tif"
        if os.path.exists(filename):
            images[i] = pygame.image.load(filename)
        else:
            print(f"Warning: {filename} not found")
    return images

def main():
    pygame.init()
    print("Pygame initialized")
    screen = pygame.display.set_mode((586, 445))
    pygame.display.set_caption("Countdown Timer")
    
    font = pygame.font.Font(None, 36)
    start_button = pygame.Rect(243, 350, 100, 50) #test button for the timer, will be replaced.
    
    images = load_images()

    background = pygame.image.load("countdown_images/background.tif")  # Load background image
    running = True
    countdown = False
    start_time = None
    clock = pygame.time.Clock()
    
    while running:
        screen.blit(background, (0, 0)) # the background image drawn
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    countdown = True
                    start_time = pygame.time.get_ticks()
        
        if countdown and start_time:
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            remaining_time = max(30 - elapsed_time, 0)
            if remaining_time in images:
                image = images[remaining_time]
                image_x = 171
                image_y = 204
                screen.blit(image, (image_x, image_y))
            if elapsed_time >= 30:
                countdown = False
        
        pygame.draw.rect(screen, (0, 255, 0), start_button) #test button for the timer, will be replaced.
        text = font.render("Start", True, (0, 0, 0))
        screen.blit(text, (263, 365)) 
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
   

if __name__ == "__main__":
    main()


