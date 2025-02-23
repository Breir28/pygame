# https://www.youtube.com/watch?v=jO6qQDNa2UY

import pygame
import os

pygame.font.init() # Initialisierung der Fonts
pygame.mixer.init() # Initialisierung des Sounds

# Konstanten
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 900, 500
FPS = 60
SPACESHIP_HEIGHT, SPACESHIP_WIDTH = 55, 40
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3

# Fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# Sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

# Trennlinie
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT) 

# Benutzer-Events definieren (müssen eindeutige Nummer haben)
YELLOW_HIT = pygame.USEREVENT + 1 
RED_HIT = pygame.USEREVENT + 2

# Definition des Screens
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) 

# Bilder laden und transformieren
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png')) # Bild laden
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT, SPACESHIP_WIDTH)), 90) # Bild skalieren und drehen
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png')) # Bild laden
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT, SPACESHIP_WIDTH)), 270) # Bild skalieren und drehen
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT)) 

# Window-Titel setzen
pygame.display.set_caption("First Game!") 

#####################################################################################
# draw_window 
#####################################################################################
def draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health):
    #WIN.fill(WHITE)
    WIN.blit(SPACE, (0, 0)) # Hintergrund       
    pygame.draw.rect(WIN, BLACK, BORDER) # Trennlinie
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(yellow_health_text, (10, 10)) # Health Text
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10)) # Health Text
    
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) # Koordinaten aus übergebenen Rectangles übernehmen <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    WIN.blit(RED_SPACESHIP, (red.x, red.y)) # Koordinaten aus übergebenen Rectangles übernehmen
    
    # Schüsse ausgeben
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)    
        
    
    pygame.display.update()        

#####################################################################################
# yellow_handle_movement
#####################################################################################
def yellow_handle_movement(keys_pressed, yellow):
        if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT
            yellow.x -= VEL  
        if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # RIGHT
            yellow.x += VEL              
        if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # UP
            yellow.y -= VEL  
        if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT: # DOWN
            yellow.y += VEL   

#####################################################################################
# red_handle_movement
#####################################################################################            
def red_handle_movement(keys_pressed, red):
        if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # LEFT
            red.x -= VEL  
        if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # RIGHT
            red.x += VEL              
        if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # UP
            red.y -= VEL  
        if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: # DOWN
            red.y += VEL               

#####################################################################################
# handle_bullets
#####################################################################################
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet): # Kollision
            pygame.event.post(pygame.event.Event(RED_HIT)) # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)        
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet): # Kollision
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.y < 0:
            red_bullets.remove(bullet) 
            
#####################################################################################
# draw_winner
#####################################################################################            
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))           
    pygame.display.update()
    pygame.time.delay(5000)

#####################################################################################
# dmain
#####################################################################################           
def main():
    
    # Rectangles
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    yellow_bullets = []
    red_bullets = []
    
    yellow_health = 10
    red_health = 10
    
    clock = pygame.time.Clock() # FPS
    
    run = True
    while run: # Game-Loop
        
        clock.tick(FPS) # FPS
        
        # Events abfragen
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            # Schiessen
            if event.type == pygame.KEYDOWN: # Tasten müssen immer neu gedrücht werden <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:     
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet) 
                    BULLET_FIRE_SOUND.play()  
            
            # Treffer
            if event.type == YELLOW_HIT: # User-Event
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
                        
            # Treffer
            if event.type == RED_HIT: # User-Event                
                red_health -= 1
                BULLET_HIT_SOUND.play()
        
        # Helth-Text noch mal aktualisieren bevor Gewinner-Text ausgegeben wird        
        if yellow_health == 0 or red_health == 0:
            draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health) # Screen zeichnen            
        
        winner_text = ""
        
        if yellow_health <= 0:
            winner_text = "Red wins"
            
        if red_health <= 0:
            winner_text = "Yellow wins"               
            
        if winner_text != "":
            draw_winner(winner_text)  
            run = False      
                              
        keys_pressed = pygame.key.get_pressed() # Ermittlung aller gleichzeitig gedrückter Tasten (andere Methode als über Events) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
           
        draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health) # Screen zeichnen
        
    main()    
    
if __name__ == "__main__":
    main()    
