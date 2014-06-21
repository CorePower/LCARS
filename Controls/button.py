##
## LCARS GUI Objects Library : Rectangular bar capped with semicircle(s)
##

from __future__ import division

import pygame

from LCARS.Controls import CappedBar, Text, TextAlign

def glow_colour(clr):
	glow = pygame.Color(clr.r, clr.g, clr.b, clr.a)
	hsla = glow.hsla
	glow.hsla = (hsla[0], hsla[1], hsla[2]*1.5, hsla[3])
	return glow

class Button(CappedBar):
	def __init__(self, rect, caplocation, text, fg, bg, textclr):
		CappedBar.__init__(self, rect, caplocation, text, fg, bg, textclr)
		self.glow = glow_colour(fg)
		self.is_glowing = False

		self.glowtext = None
		if self.text:
			self.glowtext = Text(self.text.alignpoint, text, self.text.fontsize, self.text.xalign, self.textclr, self.glow)

	def setText(self, text):
		if len(text) > 0:
			if self.rect.h > self.rect.w:
				#Portrait format
				texty = self.rect.bottom - self.rect.h
				textx = self.rect.right - (self.rect.w / 10)
				textw = self.PointSizeFromBarWidth()
			elif self.rect.h < self.rect.w:
				#Landscape
				texty = self.rect.centery
				textx = self.rect.right - (self.rect.w/2)
				textw = self.PointSizeFromBarHeight()
			else:
				#Square
				texty = self.rect.centery
				textx = self.rect.right - (self.rect.w/2)
				textw = self.PointSizeFromBarHeight()

			self.text = Text((textx, texty), text, textw, TextAlign.XALIGN_CENTRE, self.textclr, self.fg)
			self.glowtext = Text((textx, texty), text, textw, TextAlign.XALIGN_CENTRE, self.textclr, self.glow)
		else:
			self.text = None
			self.glowtext = None

		self.textString = text

	def _onmousedown(self, event):
		self.is_glowing = True
		self.onmousedown(event)

	def _onmouseup(self, event):
		self.is_glowing = False
		self.onmouseup(event)

	def _ondragout(self, event):
		self.is_glowing = False
		self.ondragout(event)

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
