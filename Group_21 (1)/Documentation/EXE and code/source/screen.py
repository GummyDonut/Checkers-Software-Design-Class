#screen- window screen more specifically
import pygame
#extra view implementation- just windows 
def makewindow(width): #width of board in pixels
    window = pygame.display.set_mode((width + 150, width), 0, 32)
    pygame.display.set_caption('checkers')  # the creation of our window
    return window


    
