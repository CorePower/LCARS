import pygame

class Drawable:
	def __init__(self, enclosingrect, fg, bg, visible=True):
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

	def has_hook(self, hookname):
		try:
			if getattr(self, hookname) is not None:
				return True
		except AttributeError:
			return False
		return False
