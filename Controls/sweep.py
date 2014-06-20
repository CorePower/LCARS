##
## LCARS GUI Objects Library : "Sweep" with corner at top-left
##

from __future__ import division

import pygame

from LCARS.Controls import Control
import math

class SweepCornerExternal(Control):
	def __init__(self, rect, bordersize, fg, bg, border, show):
		Control.__init__(self, rect, fg, bg, show)
		self.border = border
		x0, y0 = rect.topleft
		minthick = min(rect.width, rect.height)
		maxthick = max(rect.width, rect.height)
		diameter = 2*minthick
		radius = diameter / 2
		dw, dh = (rect.width - radius, rect.height - radius)
		xe, ye = (x0+radius, y0+radius)

		if dh > 0:
			self.rect = pygame.Rect(x0, ye, rect.width, dh)
			self.bpatch = pygame.Rect(x0-bordersize, ye, bordersize, dh)
		elif dw > 0:
			self.rect = pygame.Rect(xe, y0, dw, rect.height)
			self.bpatch = pygame.Rect(xe, y0-bordersize, dw, bordersize)
		else:
			self.rect = False

		self.curvebound = pygame.Rect(x0, y0, diameter, diameter)
		self.borderbound = pygame.Rect(self.curvebound)
		self.borderbound.left   -= bordersize
		self.borderbound.top    -= bordersize
		self.borderbound.width  += 2*bordersize
		self.borderbound.height += 2*bordersize
		self.clip = pygame.Rect(self.borderbound.left, self.borderbound.top, radius+bordersize, radius+bordersize)

	def draw(self, window):
		if not self.visible: return

		if self.rect:
			pygame.draw.rect(window, self.fg, self.rect)
			pygame.draw.rect(window, self.border, self.bpatch)
		oldclip = window.get_clip()
		window.set_clip(self.clip)
		pygame.draw.ellipse(window, self.border, self.borderbound)
		pygame.draw.ellipse(window, self.fg, self.curvebound)
		window.set_clip(oldclip)


class SweepCornerInternal(Control):
	def __init__(self, rect, bordersize, fg, bg, border, show):
		minthick = min(rect.width, rect.height)
		rect = pygame.Rect(rect.right, rect.bottom, minthick, minthick)
		Control.__init__(self, rect, fg, bg, show)
		self.rect = rect
		self.clip = rect
		self.borderbound = pygame.Rect(rect)
		self.borderbound.width  *= 2
		self.borderbound.height *= 2

		self.border = border
		self.maskbound = pygame.Rect(self.borderbound)
		self.maskbound.left   += bordersize
		self.maskbound.top    += bordersize
		self.maskbound.width  -= 2*bordersize
		self.maskbound.height -= 2*bordersize

	def draw(self, window):
		if not self.visible: return

		pygame.draw.rect(window, self.fg, self.rect)
		oldclip = window.get_clip()
		window.set_clip(self.clip)
		pygame.draw.ellipse(window, self.border, self.borderbound)
		pygame.draw.ellipse(window, self.bg, self.maskbound)
		window.set_clip(oldclip)


class Sweep(Control):
	def __init__(self, rect, corner, xthick, ythick, bordersize, fg, bg, border, show):
		rect = pygame.Rect(rect)
		rect.top += bordersize
		rect.left += bordersize
		rect.width -= bordersize
		rect.height -= bordersize
		Control.__init__(self, rect, fg, bg, show)
		self.bordersize = bordersize
		self.border = border

		armpos_x = self.rect.left+xthick
		armpos_y = self.rect.top+ythick
		armlen_w = self.rect.w-xthick
		armlen_h = self.rect.h-ythick

		self.byrectA = pygame.Rect(self.rect.left-bordersize, armpos_y, bordersize, armlen_h)
		self.byrectB = pygame.Rect(armpos_x, armpos_y, bordersize, armlen_h)
		self.yrect   = pygame.Rect(self.rect.left, armpos_y, xthick, armlen_h)

		self.bxrectA = pygame.Rect(armpos_x, self.rect.top-bordersize, armlen_w, bordersize)
		self.bxrectB = pygame.Rect(armpos_x, armpos_y, armlen_w, bordersize)
		self.xrect   = pygame.Rect(armpos_x, self.rect.top, armlen_w, ythick)

		self.exterior = SweepCornerExternal(pygame.Rect(self.rect.left, self.rect.top, xthick, ythick), bordersize, fg, bg, border, show)
		self.interior = SweepCornerInternal(pygame.Rect(self.rect.left, self.rect.top, xthick, ythick), bordersize, fg, bg, border, show)

	def collidepoint(self, pos):
		collide = self.yrect.collidepoint(pos)
		collide = collide or self.xrect.collidepoint(pos)
		collide = collide or self.exterior.collidepoint(pos)
		return collide

	def l(self):
		return self.xrect.left

	def draw(self, window):
		if not self.visible: return

		pygame.draw.rect(window, self.border, self.byrectA, 0)
		pygame.draw.rect(window, self.border, self.byrectB, 0)
		pygame.draw.rect(window, self.border, self.bxrectA, 0)
		pygame.draw.rect(window, self.border, self.bxrectB, 0)

		pygame.draw.rect(window, self.fg, self.yrect, 0)
		pygame.draw.rect(window, self.fg, self.xrect, 0)

		self.exterior.draw(window)
		self.interior.draw(window)
