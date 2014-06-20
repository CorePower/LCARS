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
	sweeprect = Rect(5, 5, width-5, height-5)
	gui = LCARS.Main(width, height)
	gui.add_control("btn_foo", CappedBar(Rect(0, 150, 100, 40), Cap.RIGHT, "foo", gold, background, buttontext, True))
	gui.add_control("btn_bar", CappedBar(Rect(0, 200, 100, 40), Cap.RIGHT, "bar", gold, background, buttontext, True))
	gui.add_control("btn_exit", CappedBar(Rect(0, height-50, 100, 40), Cap.RIGHT, "exit", red, background, buttontext, True))
	gui.install_handler("btn_exit", "onmouseup", lambda e: gui.shutdown())
	gui.add_control("sweep", Sweep(sweeprect, False, 20, 40, 4, gold, background, borders, True))
	gui.add_control("sweep_caption", Text((100, 30), "LCARS Terminal", 40, TextAlign.XALIGN_LEFT, buttontext, None, True))
	return gui

if __name__=='__main__':
	pygame.init()
	width, height = (1024, 700)
	main(create_gui(width, height))
