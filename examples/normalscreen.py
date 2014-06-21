import pygame
from pygame.color import Color
from pygame.rect import Rect
import LCARS
from LCARS.Controls import *
from LCARS.Sound import *

background = Color("grey10")
borders = Color("black")
buttontext = Color("black")
gold = Color("gold")
red = Color("orangered")

#=======================================

SOUNDS = LCARS.Sound.Cache()

def main(gui):
	clock = pygame.time.Clock()
	while gui.running:
		clock.tick(60)
		gui.repaint()
		gui.dispatch_events()
	Mixer().wait()

def create_gui(width, height):
	pygame.display.set_mode((width, height))
	pygame.display.set_caption("LCARS Terminal")
	elborect = Rect(10, 10, width-10, height-10)
	gui = LCARS.Main(width, height)
	gui.add_control("elbo", Elbo(elborect, Corner.TOP_LEFT, 60, 10, gold, background, True))
	gui.add_control("btn_foo", Button(pygame.Rect(10, 150, 60, 40), Cap.NONE, "FOO", red, gold, buttontext, True))
	gui.add_control("btn_exit", Button(pygame.Rect(10, 500, 60, 40), Cap.NONE, "EXIT", red, gold, buttontext, True))
	def on_btn_exit(event):
		SOUNDS.play("slide-into-place")
		gui.shutdown()
	gui.install_handler("btn_exit", "onmouseup", on_btn_exit)
	gui.install_handler("btn_foo", "onmouseup", lambda e: SOUNDS.play("deny-chirp"))
	return gui

if __name__=='__main__':
	pygame.init()
	width, height = (1024, 700)
	main(create_gui(width, height))
