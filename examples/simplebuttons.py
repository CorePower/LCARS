import pygame
from pygame.color import Color
from pygame.rect import Rect
import LCARS
from LCARS.Controls import *
from LCARS.Sound import *

white = Color("white")
black = Color("black")
gold = Color("gold")
red = Color("orangered")
darkgrey = Color("grey10")
background = darkgrey
buttontext = black

#=======================================

class SimpleTest(LCARS.Main):
	def __init__(self, width, height, surface=None, fullscreen=False):
		LCARS.Main.__init__(self, width, height, "LCARS Terminal", surface, fullscreen)
		self.sounds = LCARS.Sound.Cache()
		self.create()

	def create(self):
		spacing = 5
		elbo_stub = self.add_control("elbo_stub", CappedBar(pygame.Rect(self.width-50, 10, 50, 40), Cap.RIGHT, None, gold, background, None))
		elbo_caption = self.add_control("elbo_caption", Text((elbo_stub.l()-20, 30), "LCARS Terminal", 40, TextAlign.XALIGN_RIGHT, white, None))
		elbo = self.add_control("elbo", Elbo(pygame.Rect(10, 10, elbo_caption.l()-20-spacing, 140), Corner.TOP_LEFT, 100, 40, gold, background))
		btn_foo = self.add_control("btn_foo", Button(Rect(10, elbo.b()+spacing, 100, 40), Cap.NONE, "FOO", gold, background, buttontext))
		btn_bar = self.add_control("btn_bar", Button(Rect(10, btn_foo.b()+spacing, 100, 40), Cap.NONE, "BAR", gold, background, buttontext))
		col_stub = self.add_control("stub", CappedBar(Rect(10, self.height-40, 100, 40), Cap.NONE, None, gold, None, None))
		btn_exit = self.add_control("btn_exit", Button(Rect(10, col_stub.t()-40-spacing, 100, 40), Cap.NONE, "EXIT", red, background, buttontext))
		spacer = self.add_control("spacer", CappedBar(pygame.Rect(10, btn_bar.b()+spacing, 100, btn_exit.t()-btn_bar.b()-2*spacing), Cap.NONE, None, gold, None, None))
		self.install_handler("btn_foo", "onmouseup", lambda e: self.sounds.play("deny-chirp"))
		self.install_handler("btn_bar", "onmouseup", lambda e: self.sounds.play("deny-chirp"))
		def on_btn_exit(event):
			self.sounds.play("slide-into-place")
			self.shutdown()
		self.install_handler("btn_exit", "onmouseup", on_btn_exit)

if __name__=='__main__':
	pygame.init()
	pygame.mixer.init()
	SimpleTest(1024, 700).mainloop()
