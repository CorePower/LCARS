import pygame

from LCARS.Controls import Drawable

class Control(Drawable):
	def __init__(self, enclosingrect, fg, bg):
		Drawable.__init__(self, enclosingrect, fg, bg)

	def _onmousemotion(self, event):
		self.onmousemotion(event)

	def _ondragover(self, event):
		self._onmousemotion(event)
		self.ondragover(event)

	def _ondragout(self, event):
		self._onmousemotion(event)
		self.ondragout(event)

	def _ondragin(self, event):
		self._onmousemotion(event)
		self.ondragin(event)

	def _onmouseover(self, event):
		self._onmousemotion(event)
		self.onmouseover(event)

	def _onmousedown(self, event):
		self.onmousedown(event)

	def _onmouseup(self, event):
		self.onmouseup(event)

	def onmousemotion(self, event):
		pass

	def ondragover(self, event):
		pass

	def ondragout(self, event):
		pass

	def ondragin(self, event):
		pass

	def onmouseover(self, event):
		pass

	def onmousedown(self, event):
		pass

	def onmouseup(self, event):
		pass
