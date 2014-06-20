##
## LCARS GUI Objects Library : Simple Rectangle Object with text
##

import pygame

from LCARS.Controls import Text

class TextRect(Text):
	def __init__(self, rect, text, size, xalign, fg, bg):
		self.Text.__init__(self, rect, text, size, xalign, fg, bg, True)

	def draw(self, window):
		pygame.draw.rect(window, SS_FG, self.rect, 0)
