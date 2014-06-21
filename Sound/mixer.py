import pygame.mixer

class Mixer(object):
	def __init__(self):
		pass

	def is_active(self):
		return pygame.mixer.get_busy()

	def wait(self):
		while self.is_active():
			pass
