##
## LCARS GUI Objects Library : "Sweep" with corner at top-left
##

from __future__ import division

import pygame

from LCARSGui import LCARSObject
import math

def add_outer_border(rect, vertbordersize, horzbordersize):
	top, height = (rect.top-vertbordersize, rect.height+2*vertbordersize)
	left, width = (rect.left-horzbordersize, rect.width+2*horzbordersize)
	return pygame.Rect(left, top, width, height)

class LCARSSweep(LCARSObject):

	def __init__(self, rect, corner, xthick, ythick, bordersize, fg, bg, border, show):
		rect = pygame.Rect(rect)
		rect.top += bordersize
		rect.left += bordersize
		rect.width -= bordersize
		rect.height -= bordersize
		LCARSObject.__init__(self, rect, fg, bg, show)
		self.bordersize = bordersize
		self.border = border
		
		minl = min(xthick, ythick)
		ycorrection = ythick - (minl * 2/3)
		xcorrection = xthick + (minl * 2/3)
		
		self.yrect = pygame.Rect(self.rect.left, self.rect.top + ycorrection, xthick, self.rect.h - ycorrection)
		self.xrect = pygame.Rect(self.rect.left + xcorrection, self.rect.top, self.rect.w - xcorrection, ythick)

		self.byrectA = pygame.Rect(self.rect.left-bordersize, self.rect.top + ycorrection, bordersize, self.rect.h - ycorrection)
		self.byrectB = pygame.Rect(self.rect.left+xthick, self.rect.top + ythick, bordersize, self.rect.h - ythick)
		self.bxrectA = pygame.Rect(self.rect.left + xcorrection, self.rect.top-bordersize, self.rect.w - xcorrection, bordersize)
		self.bxrectB = pygame.Rect(self.rect.left + xcorrection, self.rect.top+ythick, self.rect.w - xcorrection, bordersize)
		
		self.outersweepdraw = pygame.Rect(self.rect.left, self.rect.top, minl * 3, minl * 3)
		self.outersweepmask = pygame.Rect(self.rect.left + xthick, self.rect.top + ythick, minl * 3, minl * 3)
		self.innersweepdraw = pygame.Rect(self.rect.left + xthick, self.rect.top + ythick, minl, minl)
		self.innersweepmask = pygame.Rect(self.rect.left + xthick, self.rect.top + ythick, minl * 2, minl * 2)
		
		self.boutersweepdraw = add_outer_border(self.outersweepdraw, bordersize, bordersize)
		self.boutersweepmask = add_outer_border(self.outersweepmask, bordersize, bordersize)
		self.binnersweepdraw = add_outer_border(self.innersweepdraw, -bordersize, -bordersize)
		self.binnersweepmask = add_outer_border(self.innersweepmask, -bordersize, -bordersize)

		self.innersweepmaskA = pygame.Rect(self.rect.left + xthick + minl, self.rect.top + ythick+bordersize, minl, minl*2-bordersize)
		self.innersweepmaskB = pygame.Rect(self.rect.left + xthick+bordersize, self.rect.top + ythick + minl, minl*2-bordersize, minl)
		
	def collidepoint(self, pos):
		collide = self.yrect.collidepoint(pos)
		collide = collide or self.xrect.collidepoint(pos) 
		collide = collide or (self.pointInsideEllipse(self.outersweepdraw, pos) and (not self.outersweepmask.collidepoint(pos)))
		collide = collide or ((not self.pointInsideEllipse(self.innersweepmask, pos)) and (self.innersweepdraw.collidepoint(pos)))
		return collide
	
	def pointInsideEllipse(self, rect, pos):
		## No point testing for inside circle
		## if outside enclosing rect
		collide = False
		if rect.collidepoint(pos):
			x, y = pos
			x = x - rect.centerx
			y = y - rect.centery
			
			rx = rect.w / 2
			ry = rect.h / 2
			
			rxx = rx*rx
			ryy = ry * ry
			xx = x*x
			yy = y*y
			
			res = (xx/rxx) + (yy/ryy)
			
			collide = res <	 1
		
		return collide
		
	def l(self):
		return self.xrect.left
		
	def draw(self, window):
		pygame.draw.ellipse(window, self.border, self.boutersweepdraw, 0)

		#Sweep - big ellipse (foreground) and rectangle (background)
		pygame.draw.ellipse(window, self.fg, self.outersweepdraw, 0)
		pygame.draw.rect(window, self.bg, self.outersweepmask, 0)

		pygame.draw.rect(window, self.border, self.byrectA, 0)
		pygame.draw.rect(window, self.border, self.byrectB, 0)
		pygame.draw.rect(window, self.border, self.bxrectA, 0)
		pygame.draw.rect(window, self.border, self.bxrectB, 0)

		# Vertical and horizontal bars
		pygame.draw.rect(window, self.fg, self.yrect, 0)
		pygame.draw.rect(window, self.fg, self.xrect, 0)
	
		#Sweep - small ellipse (background) and rectangle (foreground)
		#pygame.draw.rect(window, self.fg, self.innersweepdraw, 0)
		#pygame.draw.ellipse(window, self.bg, self.innersweepmask, 0)
		pygame.draw.rect(window, self.fg, self.innersweepdraw, 0)
		pygame.draw.ellipse(window, self.border, self.innersweepmask, 0)
		pygame.draw.ellipse(window, self.bg, self.binnersweepmask, 0)
		pygame.draw.rect(window, self.bg, self.innersweepmaskA, 0)
		pygame.draw.rect(window, self.bg, self.innersweepmaskB, 0)
