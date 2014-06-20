##
## LCARS GUI Objects Library : Base LCARS Object
##

import pygame

class LCARSObject:
	def __init__(self, enclosingrect, fg, bg, visible):
		self.rect = enclosingrect.copy()
		self.fg = fg
		self.bg = bg
		self.visible = visible

	def r(self):
		return self.rect.left + self.rect.w

	def l(self):
		return self.rect.left

	def t(self):
		return self.rect.top

	def b(self):
		return self.rect.top + self.rect.h

	def collidePoint(self, pos):
		return self.rect.collidepoint(pos)

	def ondragover(self, event):
		pass

	def ondragout(self, event):
		pass

	def ondragin(self, event):
		pass

	def onmouseover(self, event):
		pass

	def onmousedown(self, event):
		pass

	def onmouseup(self, event):
		pass
