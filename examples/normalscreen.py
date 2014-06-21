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

class NormalScreen(LCARS.Main):
	def __init__(self, width, height, surface=None, fullscreen=False):
		LCARS.Main.__init__(self, width, height, "LCARS Terminal", surface, fullscreen)
		self.sounds = LCARS.Sound.Cache()
		self.create()

	def create(self):
		spacing = 5

		rail_top = self.add_control("rail_top", CappedBar(Rect(150+spacing, 190, self.width-150-spacing, 10), Cap.NONE, None, clr_elbos, None, None))
		rail_bottom = self.add_control("rail_bottom", CappedBar(Rect(150+spacing, rail_top.b()+spacing, self.width-150-spacing, 10), Cap.NONE, None, clr_elbos, None, None))
		elbo_top = self.add_control("elbo_top", Elbo(Rect(0, 0, 150, 200), Corner.BOTTOM_LEFT, 100, 10, clr_elbos, self.background))
		elbo_bottom = self.add_control("elbo_bottom", Elbo(Rect(0, elbo_top.b()+spacing, 150, 200), Corner.TOP_LEFT, 100, 10, clr_elbos, self.background))

		btn_foo = self.add_control("btn_foo", Button(Rect(0, elbo_bottom.b()+spacing, 100, 40), Cap.NONE, "FOO", clr_primary, self.background, buttontext))
		btn_bar = self.add_control("btn_bar", Button(Rect(0, btn_foo.b()+spacing, 100, 40), Cap.NONE, "BAR", clr_primary, self.background, buttontext))
		btn_foo.set_enabled(False)
		col_stub = self.add_control("stub", CappedBar(Rect(0, self.height-40, 100, 40), Cap.NONE, None, clr_elbos, None, None))
		btn_exit = self.add_control("btn_exit", Button(Rect(0, col_stub.t()-40-spacing, 100, 40), Cap.NONE, "EXIT", clr_cancel, self.background, buttontext))
		spacer = self.add_control("spacer", CappedBar(Rect(0, btn_bar.b()+spacing, 100, btn_exit.t()-btn_bar.b()-2*spacing), Cap.NONE, None, clr_elbos, None, None))

		btn_top1 = self.add_control("btn_top1", Button(Rect(self.width-320,  50, 150, 40), Cap.HORZ, "TOP1", clr_primary, None, buttontext))
		btn_top2 = self.add_control("btn_top2", Button(Rect(self.width-160,  50, 150, 40), Cap.HORZ, "TOP2", clr_primary, None, buttontext))
		btn_top3 = self.add_control("btn_top3", Button(Rect(self.width-320, 100, 150, 40), Cap.HORZ, "TOP3", clr_primary, None, buttontext))
		btn_top4 = self.add_control("btn_top4", Button(Rect(self.width-160, 100, 150, 40), Cap.HORZ, "TOP4", clr_primary, None, buttontext))

		def on_btn_exit(event):
			self.shutdown()
		self.install_handler("btn_exit", "onclick", on_btn_exit)
		btn_exit.beep = None

	def onquit(self, event):
		self.sounds.play("whirr")

	def while_control_disabled(self, ctrl, event, hookname):
		self.sounds.play("deny-chirp")

if __name__=='__main__':
	NormalScreen(1366, 768, fullscreen=True).mainloop()
