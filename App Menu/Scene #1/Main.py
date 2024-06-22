# import the pygame module 
import pygame 
import os
from pygame.locals import*

pygame.init()
# Define the background colour 
# using RGB color coding. 
background_colour = (255, 252, 242) 
white = (255,255,255)
black = (0,0,0)
img = pygame.image.load(os.path.join('barbells.jpg'))
img2 = pygame.image.load(os.path.join('workout.jpg'))
img = pygame.transform.scale(img,(300,300))
img2 = pygame.transform.scale(img2,(300,300))

# Define the dimensions of 
# screen object(width,height) 
screen = pygame.display.set_mode((900, 700)) 

# Set the caption of the screen 
pygame.display.set_caption('The Pancake Project') 

# Fill the background colour to the screen 
screen.fill(background_colour)

# Update the display using flip 
pygame.display.flip() 

font = pygame.font.Font('freesansbold.ttf', 55)
textThe = font.render('The', True,black, background_colour)
textPan = font.render('Pancake', True,black, background_colour)
textPro = font.render('Project', True,black, background_colour)
textRect1 = textThe.get_rect()
textRect1.center = (450,250)
textRect2= textPan.get_rect()
textRect2.center = (450,300)
textRect3 = textPro.get_rect()
textRect3.center = (450,350)

# Variable to keep our game loop running 
running = True

# game loop 
while running: 

	screen.blit(textThe, textRect1)
	screen.blit(textPan, textRect2)
	screen.blit(textPro, textRect3)
	screen.blit(img,(25,100))
	screen.blit(img2,(575,100))
    # for loop through the event queue 
	for event in pygame.event.get(): 
	
		# Check for QUIT event	 
		if event.type == pygame.QUIT: 
			running = False
		pygame.display.update()
	
        
