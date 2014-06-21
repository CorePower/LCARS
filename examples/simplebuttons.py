import pygame
from pygame.color import Color
from pygame.rect import Rect
import LCARS
from LCARS.Controls import *
from LCARS.Sound import *

white = Color("white")
black = Color("black")
clr_elbos   = Color("#f1df6f")
clr_unavail = Color("#999999")
clr_primary = Color("#99ccff")
clr_secondary1 = Color("#ffff33")
clr_secondary2 = Color("#ffffcc")
clr_offline = Color("#ff0000")
clr_cancel = Color("orangered")

buttontext = black

#=======================================

class SimpleTest(LCARS.Main):
	def __init__(self, width, height, surface=None, fullscreen=False):
		LCARS.Main.__init__(self, width, height, "LCARS Terminal", surface, fullscreen)
		self.sounds = LCARS.Sound.Cache()
		self.create()

	def create(self):
		spacing = 5
		elbo_stub = self.add_control("elbo_stub", CappedBar(pygame.Rect(self.width-50, 10, 50, 40), Cap.RIGHT, None, clr_elbos, self.background, None))
		elbo_caption = self.add_control("elbo_caption", Text((elbo_stub.l()-20, 30), "LCARS Terminal", 40, TextAlign.XALIGN_RIGHT, white, None))
		elbo = self.add_control("elbo", Elbo(pygame.Rect(10, 10, elbo_caption.l()-20-spacing, 140), Corner.TOP_LEFT, 100, 40, clr_elbos, self.background))
		btn_foo = self.add_control("btn_foo", Button(Rect(10, elbo.b()+spacing, 100, 40), Cap.NONE, "FOO", clr_primary, self.background, buttontext))
		btn_bar = self.add_control("btn_bar", Button(Rect(10, btn_foo.b()+spacing, 100, 40), Cap.NONE, "BAR", clr_secondary1, self.background, buttontext))
		btn_baz = self.add_control("btn_baz", Button(Rect(10, btn_bar.b()+spacing, 100, 40), Cap.NONE, "BAZ", clr_secondary2, self.background, buttontext))
		col_stub = self.add_control("stub", CappedBar(Rect(10, self.height-40, 100, 40), Cap.NONE, None, clr_elbos, None, None))
		btn_exit = self.add_control("btn_exit", Button(Rect(10, col_stub.t()-40-spacing, 100, 40), Cap.NONE, "EXIT", clr_cancel, self.background, buttontext))
		spacer = self.add_control("spacer", CappedBar(pygame.Rect(10, btn_baz.b()+spacing, 100, btn_exit.t()-btn_baz.b()-2*spacing), Cap.NONE, None, clr_elbos, None, None))
		def on_btn_exit(event):
			self.shutdown()
		self.install_handler("btn_exit", "onclick", on_btn_exit)
		btn_exit.beep = None

	def onquit(self, event):
		self.sounds.play("slide-into-place")

	def while_control_disabled(self, ctrl, event, hookname):
		self.sounds.play("deny-chirp")

if __name__=='__main__':
	SimpleTest(1024, 700).mainloop()
