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

class NormalScreen(LCARS.Main):
	def __init__(self, width, height, surface=None, fullscreen=False):
		LCARS.Main.__init__(self, width, height, "LCARS Terminal", surface, fullscreen)
		self.sounds = LCARS.Sound.Cache()
		self.create()

	def create(self):
		spacing = 5

		rail_top = self.add_control("rail_top", CappedBar(Rect(150, 190, self.width-150, 10), Cap.NONE, None, gold, None, None))
		rail_bottom = self.add_control("rail_bottom", CappedBar(Rect(150, rail_top.b()+spacing, self.width-150, 10), Cap.NONE, None, gold, None, None))
		elbo_top = self.add_control("elbo_top", Elbo(Rect(0, 0, 150, 200), Corner.BOTTOM_LEFT, 100, 10, gold, background))
		elbo_bottom = self.add_control("elbo_bottom", Elbo(Rect(0, elbo_top.b()+spacing, 150, 200), Corner.TOP_LEFT, 100, 10, gold, background))

		btn_foo = self.add_control("btn_foo", Button(Rect(0, elbo_bottom.b()+spacing, 100, 40), Cap.NONE, "FOO", gold, background, buttontext))
		btn_bar = self.add_control("btn_bar", Button(Rect(0, btn_foo.b()+spacing, 100, 40), Cap.NONE, "BAR", gold, background, buttontext))
		col_stub = self.add_control("stub", CappedBar(Rect(0, self.height-40, 100, 40), Cap.NONE, None, gold, None, None))
		btn_exit = self.add_control("btn_exit", Button(Rect(0, col_stub.t()-40-spacing, 100, 40), Cap.NONE, "EXIT", red, background, buttontext))
		spacer = self.add_control("spacer", CappedBar(Rect(0, btn_bar.b()+spacing, 100, btn_exit.t()-btn_bar.b()-2*spacing), Cap.NONE, None, gold, None, None))

		self.install_handler("btn_foo", "onclick", lambda e: self.sounds.play("deny-chirp"))
		self.install_handler("btn_bar", "onclick", lambda e: self.sounds.play("deny-chirp"))

		def on_btn_exit(event):
			self.shutdown()
		self.install_handler("btn_exit", "onclick", on_btn_exit)

	def onquit(self, event):
		self.sounds.play("whirr")

if __name__=='__main__':
	NormalScreen(1366, 768, fullscreen=True).mainloop()
