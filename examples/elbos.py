import pygame
from pygame.color import Color
from pygame.rect import Rect
import LCARS
from LCARS.Controls import *

background = Color("grey10")
borders = Color("black")
buttontext = Color("black")
gold = Color("gold")
red = Color("orangered")

#=======================================

def main(gui):
	clock = pygame.time.Clock()
	while gui.running:
		clock.tick(60)
		gui.repaint()
		gui.dispatch_events()

def create_gui(width, height):
	pygame.display.set_mode((width, height))
	pygame.display.set_caption("LCARS Terminal")
	midx, midy = (width/2-5, height/2-5)
	orgx, orgy = (midx+10, midy+10)
	gui = LCARS.Main(width, height)
	gui.add_control("elbo1", Elbo(pygame.Rect(0,    0,    midx,  midy),   Corner.BOTTOM_RIGHT, 20, 40, 4, red, background, borders, True))
	gui.add_control("elbo2", Elbo(pygame.Rect(orgx, 0,    width, midy),   Corner.BOTTOM_LEFT,  20, 40, 4, gold,  background, borders, True))
	gui.add_control("elbo3", Elbo(pygame.Rect(0,    orgy, midx,  height), Corner.TOP_RIGHT,    20, 40, 4, gold, background, borders, True))
	gui.add_control("elbo4", Elbo(pygame.Rect(orgx, orgy, width, height), Corner.TOP_LEFT,     20, 40, 4, red,  background, borders, True))
	return gui

if __name__=='__main__':
	pygame.init()
	width, height = (1024, 700)
	main(create_gui(width, height))
