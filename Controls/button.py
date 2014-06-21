from __future__ import division

import pygame

from LCARS.Controls import Control, CappedBar, Text, TextAlign
from LCARS.Sound import Cache, Clip

BUTTON_BEEP_CACHE = Cache()

def glow_colour(clr):
	glow = pygame.Color(clr.r, clr.g, clr.b, clr.a)
	hsla = glow.hsla
	oldlum = hsla[2]
	if oldlum >= 90:
		glow.hsla = (hsla[0], hsla[1]/2, 90, hsla[3])
	elif oldlum >= 80:
		glow.hsla = (hsla[0], hsla[1], 100, hsla[3])
	else:
		glow.hsla = (hsla[0], hsla[1], 90, hsla[3])
	return glow

class Button(CappedBar):
	def __init__(self, rect, caplocation, text, fg, bg, textclr):
		self.glow = glow_colour(fg)
		self.is_glowing = False
		self.beep = None
		CappedBar.__init__(self, rect, caplocation, text, fg, bg, textclr)

	def setGlowText(self, text):
		self.glowtext = None
		if self.text:
			self.glowtext = Text(self.text.alignpoint, text, self.text.fontsize, self.text.xalign, self.textclr, self.glow)

	def setText(self, text):
		CappedBar.setText(self, text)
		self.setGlowText(text)

	def _onmousedown(self, event):
		Control._onmousedown(self, event)
		self.is_glowing = True

	def _onmouseup(self, event):
		Control._onmouseup(self, event)
		self.is_glowing = False

	def _ondragout(self, event, target):
		Control._ondragout(self, event, target)
		self.is_glowing = False

	def _ondragin(self, event, target):
		Control._ondragin(self, event, target)
		self.is_glowing = (target==self)

	def _onclick(self, event):
		Control._onclick(self, event)
		if self.beep is not None:
			global BUTTON_BEEP_CACHE
			BUTTON_BEEP_CACHE.play(self.beep)

	def draw(self, window):
		if not self.visible: return
		oldclr = self.fg
		oldtext = self.text
		if self.is_glowing:
			self.fg = self.glow
			self.text = self.glowtext
		try:
			CappedBar.draw(self, window)
		except:
			pass
		self.fg = oldclr
		self.text = oldtext
