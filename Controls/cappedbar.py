##
## LCARS GUI Objects Library : Rectangular bar capped with semicircle(s)
##

from __future__ import division

import pygame

from LCARS.Controls import Control, Text, TextAlign
from LCARS.Exceptions import GeometryException

class Cap(object):
	NONE = 0
	TOP = 1
	LEFT = 2
	RIGHT = 4
	BOTTOM = 8
	HORZ = 6
	VERT = 9
	def __init__(self, bound, clip):
		self.bound = bound
		self.clip = clip

	def draw(self, window, colour):
		oldclip = window.get_clip()
		window.set_clip(self.clip)
		pygame.draw.ellipse(window, colour, self.bound)
		window.set_clip(oldclip)

	def __repr__(self):
		return "<Cap: bound=%s, clip=%s>" % (str(self.bound), str(self.clip))

class CappedBar(Control):
	def __init__(self, rect, caplocation, text, fg, bg, textclr):
		Control.__init__(self, rect, fg, bg)
		self.textclr = textclr
		self.setText(text)

		self.innerrect = pygame.Rect(self.rect)
		self.caps = []
		if (caplocation & Cap.TOP):
			self.add_top_cap()
		if (caplocation & Cap.LEFT):
			self.add_left_cap()
		if (caplocation & Cap.RIGHT):
			self.add_right_cap()
		if (caplocation & Cap.BOTTOM):
			self.add_bottom_cap()


	def add_left_cap(self):
		if self.rect.height > self.rect.width: raise GeometryException("cannot add a horizontal cap on a portrait-shaped bar")
		radius = self.rect.height/2
		bound = pygame.Rect(self.rect.left, self.rect.top, 2*radius, 2*radius)
		clip  = pygame.Rect(self.rect.left, self.rect.top, radius, 2*radius)
		self.caps.append(Cap(bound, clip))
		self.innerrect.left += radius
		self.innerrect.width -= radius

	def add_right_cap(self):
		if self.rect.height > self.rect.width: raise GeometryException("cannot add a horizontal cap on a portrait-shaped bar")
		radius = self.rect.height/2
		bound = pygame.Rect(self.rect.right-2*radius, self.rect.top, 2*radius, 2*radius)
		clip  = pygame.Rect(self.rect.right-radius, self.rect.top, radius, 2*radius)
		self.caps.append(Cap(bound, clip))
		self.innerrect.width -= radius

	def add_top_cap(self):
		if self.rect.height < self.rect.width: raise GeometryException("cannot add a vertical cap on a landscape-shaped bar")
		radius = self.rect.width/2
		bound = pygame.Rect(self.rect.left, self.rect.top, 2*radius, 2*radius)
		clip  = pygame.Rect(self.rect.left, self.rect.top, 2*radius, radius)
		self.caps.append(Cap(bound, clip))
		self.innerrect.top += radius
		self.innerrect.height -= radius

	def add_bottom_cap(self):
		if self.rect.height < self.rect.width: raise GeometryException("cannot add a vertical cap on a landscape-shaped bar")
		radius = self.rect.width/2
		bound = pygame.Rect(self.rect.left, self.rect.bottom-2*radius, 2*radius, 2*radius)
		clip  = pygame.Rect(self.rect.left, self.rect.bottom-radius, 2*radius, radius)
		self.caps.append(Cap(bound, clip))
		self.innerrect.height -= radius

	def PointSizeFromBarHeight(self):
		pointSizeAt50px = 24
		return int((self.rect.h / 50) * pointSizeAt50px)

	def PointSizeFromBarWidth(self):
		pointSizeAt50px = 24
		return int((self.rect.w / 50) * pointSizeAt50px)

	def setText(self, text):
		if (text is None) or len(text) == 0:
			self.text = None
			self.textString = ""
			return

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

		self.text = Text((textx, texty), text, textw, TextAlign.XALIGN_CENTRE, self.textclr, None)
		self.textString = text

	def getText(self):
		return self.textString

	def setWidth(self, newWidth):
		self.rect.width = newWidth
		# Make sure that text is correctly located
		self.setText(self.textString)

	def draw(self, window):
		if not self.visible: return
		# Draw each endcap
		for cap in self.caps:
			cap.draw(window, self.fg)

		if self.innerrect.width > 0 and self.innerrect.height > 0:
			pygame.draw.rect(window, self.fg, self.innerrect)

		# Draw text (if any)
		if self.text is not None:
			self.text.draw(window)
