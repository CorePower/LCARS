##
## LCARS GUI Objects Library : "Elbo" with corner at top-left
##

from __future__ import division

import pygame

from LCARS.Controls import Control
import math

class Corner:
	TOP_LEFT     = 0b111
	TOP_RIGHT    = 0b011
	BOTTOM_LEFT  = 0b101
	BOTTOM_RIGHT = 0b001
	TOP          = 0b010
	LEFT         = 0b100

def corner_to_reflections(corner):
	if corner == Corner.TOP_LEFT:
		return (False, False)
	if corner == Corner.TOP_RIGHT:
		return (True, False)
	elif corner == Corner.BOTTOM_LEFT:
		return (False, True)
	elif corner == Corner.BOTTOM_RIGHT:
		return (True, True)
	return None

def reflect_coord(x, base, width):
	return 2*base + width - x

def reflect_rect(subject, frame, reflect_x, reflect_y):
	x0, y0, x1, y1 = (subject.left, subject.top, subject.right, subject.bottom)
	if reflect_x:
		x0 = reflect_coord(x0, frame.left, frame.width)
		x1 = reflect_coord(x1, frame.left, frame.width)
	if reflect_y:
		y0 = reflect_coord(y0, frame.top, frame.height)
		y1 = reflect_coord(y1, frame.top, frame.height)
	subject.left = min(x0, x1)
	subject.top  = min(y0, y1)

class ElboCornerExternal(Control):
	def __init__(self, rect, corner, bordersize, fg, bg, border, show):
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
			self.brect = pygame.Rect(x0, ye, rect.width, dh)
			self.bpatch = pygame.Rect(x0-bordersize, ye, bordersize, dh)
		elif dw > 0:
			self.brect = pygame.Rect(xe, y0, dw, rect.height)
			self.bpatch = pygame.Rect(xe, y0-bordersize, dw, bordersize)
		else:
			self.brect = False

		self.curvebound = pygame.Rect(x0, y0, diameter, diameter)
		self.reflect_curve(self.curvebound, corner)

		self.borderbound = pygame.Rect(self.curvebound)
		self.borderbound.left   -= bordersize
		self.borderbound.top    -= bordersize
		self.borderbound.width  += 2*bordersize
		self.borderbound.height += 2*bordersize
		self.clip = pygame.Rect(x0-bordersize, y0-bordersize, radius+bordersize, radius+bordersize)

		self.reflect(corner)

	def reflect(self, corner):
		reflect_x, reflect_y = corner_to_reflections(corner)
		frame = self.rect
		reflect_rect(self.brect,  frame, reflect_x, reflect_y);
		reflect_rect(self.bpatch, frame, reflect_x, reflect_y);
		reflect_rect(self.clip,   frame, reflect_x, reflect_y);

	def reflect_curve(self, subject, corner):
		if not (corner & Corner.LEFT):
			subject.left -= subject.width/2

	def draw(self, window):
		if not self.visible: return

		if self.brect:
			pygame.draw.rect(window, self.fg, self.brect)
			pygame.draw.rect(window, self.border, self.bpatch)
		oldclip = window.get_clip()
		window.set_clip(self.clip)
		pygame.draw.ellipse(window, self.border, self.borderbound)
		pygame.draw.ellipse(window, self.fg, self.curvebound)
		window.set_clip(oldclip)


class ElboCornerInternal(Control):
	def __init__(self, rect, corner, bordersize, fg, bg, border, show):
		minthick = min(rect.width, rect.height)
		orect = pygame.Rect(rect.left, rect.top, minthick, minthick)
		Control.__init__(self, rect, fg, bg, show)
		self.orect = orect
		self.clip = orect
		self.borderbound = pygame.Rect(orect)
		self.borderbound.width  *= 2
		self.borderbound.height *= 2

		self.reflect_curve(self.borderbound, corner)

		self.border = border
		self.maskbound = pygame.Rect(self.borderbound)
		self.maskbound.left   += bordersize
		self.maskbound.top    += bordersize
		self.maskbound.width  -= 2*bordersize
		self.maskbound.height -= 2*bordersize

	def reflect_curve(self, subject, corner):
		if not (corner & Corner.TOP):
			subject.top  -= 1 + subject.height/2
		else:
			subject.top  += 1
		if not (corner & Corner.LEFT):
			subject.left -= 1 + subject.width/2
		else:
			subject.left += 1

	def draw(self, window):
		if not self.visible: return
		pygame.draw.rect(window, self.fg, self.orect)
		oldclip = window.get_clip()
		window.set_clip(self.clip)
		pygame.draw.ellipse(window, self.border, self.borderbound)
		pygame.draw.ellipse(window, self.bg, self.maskbound)
		window.set_clip(oldclip)


class Elbo(Control):
	def __init__(self, rect, corner, xthick, ythick, bordersize, fg, bg, border, show):
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

		self.cornerextrect = pygame.Rect(self.rect.left, self.rect.top, xthick, ythick)
		min_int_corner = min(xthick-bordersize, ythick-bordersize)
		self.cornerintrect = pygame.Rect(self.rect.left+xthick-1, self.rect.top+ythick-1, min_int_corner, min_int_corner)

		self.reflect(corner)

		self.exterior = ElboCornerExternal(self.cornerextrect, corner, bordersize, fg, bg, border, show)
		self.interior = ElboCornerInternal(self.cornerintrect, corner, bordersize, fg, bg, border, show)

	def reflect(self, corner):
		reflect_x, reflect_y = corner_to_reflections(corner)

		reflect_rect(self.byrectA, self.rect, reflect_x, reflect_y)
		reflect_rect(self.byrectB, self.rect, reflect_x, reflect_y)
		reflect_rect(self.bxrectA, self.rect, reflect_x, reflect_y)
		reflect_rect(self.bxrectB, self.rect, reflect_x, reflect_y)
		reflect_rect(self.yrect, self.rect, reflect_x, reflect_y)
		reflect_rect(self.xrect, self.rect, reflect_x, reflect_y)
		reflect_rect(self.cornerextrect, self.rect, reflect_x, reflect_y)
		reflect_rect(self.cornerintrect, self.rect, reflect_x, reflect_y)

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
