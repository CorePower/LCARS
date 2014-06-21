import pygame.mixer
from pkg_resources import resource_filename

class Clip(object):
	def __init__(self, clipname):
		self.filename = resource_filename(__name__, "../data/sfx/%s.wav" % clipname)
		self.sound = pygame.mixer.Sound(self.filename)

	def play(self):
		self.sound.play()

class Cache(object):
	def __init__(self):
		self.loaded = {}

	def preload(self, clipname):
		if not self.loaded.has_key(clipname):
			self.loaded[clipname] = Clip(clipname)

	def play(self, clipname):
		self.preload(clipname)
		self.loaded[clipname].play()
