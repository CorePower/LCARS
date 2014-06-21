import pygame
from pygame.color import Color
from pygame.rect import Rect
import LCARS
from LCARS.Controls import *

background = Color("grey10")
gold = Color("gold")
red = Color("orangered")

#=======================================

class ElbosTest(LCARS.Main):
	def __init__(self, width, height, surface=None, fullscreen=False):
		LCARS.Main.__init__(self, width, height, "LCARS Demonstration: elbos", surface, fullscreen)
		self.create()

	def create(self):
		midx, midy = (self.width/2-5, self.height/2-5)
		orgx, orgy = (midx+10, midy+10)
		xthick, ythick = (80, 10)
		self.add_control("elbo1", Elbo(pygame.Rect(0,    0,    midx,  midy),   Corner.BOTTOM_RIGHT, xthick, ythick, red, background))
		self.add_control("elbo2", Elbo(pygame.Rect(orgx, 0,    self.width, midy),   Corner.BOTTOM_LEFT,  xthick, ythick, gold,  background))
		self.add_control("elbo3", Elbo(pygame.Rect(0,    orgy, midx,  self.height), Corner.TOP_RIGHT,    xthick, ythick, gold, background))
		self.add_control("elbo4", Elbo(pygame.Rect(orgx, orgy, self.width, self.height), Corner.TOP_LEFT,     xthick, ythick, red,  background))

if __name__=='__main__':
	ElbosTest(700, 700).mainloop()
