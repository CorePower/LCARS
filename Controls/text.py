# #
# # LCARS GUI Objects Library : Text Object in "Star Trek" font
# #

import pygame

from LCARS.Controls import Control
from pkg_resources import resource_filename

font_search = "swiss911"


def getHeight(text, size):
	(w, h) = pygame.font.SysFont(font, size).size(text)
	return w

class TextAlign:
	XALIGN_CENTRE = 0
	XALIGN_LEFT = 1
	XALIGN_RIGHT = 2

class Text(Control):
	def __init__(self, alignpoint, text, size, xalign, fg, bg, show):
		(x, y) = alignpoint
		self.alignpoint = alignpoint
		self.text_string = text
		self.fontsize = size
		self.xalign = xalign

		font_list = pygame.font.get_fonts()
		font_list = [font for font in font_list if (font.find(font_search) > -1)]
		font_file = resource_filename(__name__, "../data/fonts/Swiss911ExtraCompressed.ttf")

		if len(font_list)>0:
			font_file = font_list[0]

		self.font = pygame.font.Font(font_file, size)
		self.text = self.font.render(text, 1, fg, bg)

		# Define enclosing rectangle based on alignment point and align choice
		top = y - (self.text.get_height() / 2)
		if (xalign == TextAlign.XALIGN_CENTRE):
			left = x - (self.text.get_width() / 2)
		elif (xalign == TextAlign.XALIGN_RIGHT):
			left = x - self.text.get_width()
		elif (xalign == TextAlign.XALIGN_LEFT):
			left = x

		rect = pygame.Rect(left, top, self.text.get_width(), self.text.get_height())

		Control.__init__(self, rect, fg, bg, show)

	def draw(self, window):
		window.blit(self.text, self.rect)
