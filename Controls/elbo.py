##
## LCARS GUI Objects Library : "Elbo" with corner at top-left
##

from __future__ import division

import pygame

from LCARS.Controls import Drawable
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

class ElboCornerExternal(Drawable):
	def __init__(self, rect, corner, fg, bg, show):
		Drawable.__init__(self, rect, fg, bg, show)
		x0, y0 = rect.topleft
		minthick = min(rect.width, rect.height)
		maxthick = max(rect.width, rect.height)
		diameter = 2*minthick
		radius = diameter / 2
		dw, dh = (rect.width - radius, rect.height - radius)
		xe, ye = (x0+radius, y0+radius)

		if dh > 0:
			self.brect = pygame.Rect(x0, ye, rect.width, dh)
		elif dw > 0:
			self.brect = pygame.Rect(xe, y0, dw, rect.height)
		else:
			self.brect = False

		self.curvebound = pygame.Rect(x0, y0, diameter, diameter)
		self.reflect_curve(self.curvebound, corner)

		self.clip = pygame.Rect(x0, y0, radius, radius)

		self.reflect(corner)

	def reflect(self, corner):
		reflect_x, reflect_y = corner_to_reflections(corner)
		frame = self.rect
		if self.brect:
			reflect_rect(self.brect,  frame, reflect_x, reflect_y);
		reflect_rect(self.clip,   frame, reflect_x, reflect_y);

	def reflect_curve(self, subject, corner):
		if not (corner & Corner.LEFT):
			subject.left -= subject.width/2

	def draw(self, window):
		if not self.visible: return

		if self.brect:
			pygame.draw.rect(window, self.fg, self.brect)
		oldclip = window.get_clip()
		window.set_clip(self.clip)
		pygame.draw.ellipse(window, self.fg, self.curvebound)
		window.set_clip(oldclip)


class ElboCornerInternal(Drawable):
	def __init__(self, rect, corner, fg, bg, show):
		minthick = min(rect.width, rect.height)
		orect = pygame.Rect(rect.left, rect.top, minthick, minthick)
		Drawable.__init__(self, rect, fg, bg, show)
		self.orect = orect
		self.clip = orect

		self.maskbound = pygame.Rect(orect)
		self.maskbound.width  *= 2
		self.maskbound.height *= 2

		self.reflect_curve(self.maskbound, corner)

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
		pygame.draw.ellipse(window, self.bg, self.maskbound)
		window.set_clip(oldclip)


class Elbo(Drawable):
	def __init__(self, rect, corner, xthick, ythick, fg, bg, show):
		Drawable.__init__(self, rect, fg, bg, show)
		armpos_x = self.rect.left+xthick
		armpos_y = self.rect.top+ythick
		armlen_w = self.rect.w-xthick
		armlen_h = self.rect.h-ythick

		self.yrect   = pygame.Rect(self.rect.left, armpos_y, xthick, armlen_h)
		self.xrect   = pygame.Rect(armpos_x, self.rect.top, armlen_w, ythick)

		self.cornerextrect = pygame.Rect(self.rect.left, self.rect.top, xthick, ythick)
		min_int_corner = min(xthick, ythick)
		self.cornerintrect = pygame.Rect(self.rect.left+xthick-1, self.rect.top+ythick-1, min_int_corner, min_int_corner)

		self.reflect(corner)

		self.exterior = ElboCornerExternal(self.cornerextrect, corner, fg, bg, show)
		self.interior = ElboCornerInternal(self.cornerintrect, corner, fg, bg, show)

	def reflect(self, corner):
		reflect_x, reflect_y = corner_to_reflections(corner)

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

		pygame.draw.rect(window, self.fg, self.yrect, 0)
		pygame.draw.rect(window, self.fg, self.xrect, 0)

		self.exterior.draw(window)
		self.interior.draw(window)
