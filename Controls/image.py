##
## LCARS GUI Objects Library : Text Object in "Star Trek" font
##

import pygame

from LCARS.Controls import Control

class Image(Control):
	def __init__(self, enclosingrect, path):
		Control.__init__(self, enclosingrect, 0, 0) ## Colours do not matter
		self.image = pygame.image.load(path)
		imgrect = self.image.get_rect()

		self.rect.w = imgrect.w
		self.rect.h = imgrect.h

		self.rect.left = self.rect.left - (self.rect.w / 2)
		self.rect.bottom = self.rect.bottom - (self.rect.h / 2)

	def draw(self, window):
		window.blit(self.image, self.rect)
