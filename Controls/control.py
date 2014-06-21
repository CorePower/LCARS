import pygame

from LCARS.Controls import Drawable
from LCARS.Exceptions import StopEventBubbling, ControlIsDisabled

class Control(Drawable):
	def __init__(self, enclosingrect, fg, bg, disabled_fg=pygame.Color("#999999")):
		Drawable.__init__(self, enclosingrect, fg, bg)
		self._enabled = True
		self.real_fg = self.fg
		self.disabled_fg = disabled_fg

	def set_enabled(self, setting):
		self._enabled = setting
		if self._enabled:
			self.fg = self.real_fg
		else:
			self.fg = self.disabled_fg

	def ensure_enabled(self, hookname):
		if not self._enabled:
			if hookname == "click":
				raise ControlIsDisabled(self, hookname)
			else:
				raise StopEventBubbling(hookname)

	def _onmousemotion(self, event):
		self.ensure_enabled("mousemotion")
		self.onmousemotion(event)

	def _ondragover(self, event, target):
		self.ensure_enabled("dragover")
		self._onmousemotion(event)
		self.ondragover(event, target)

	def _ondragout(self, event, target):
		self.ensure_enabled("dragout")
		self._onmousemotion(event)
		self.ondragout(event, target)

	def _ondragin(self, event, target):
		self.ensure_enabled("dragin")
		self._onmousemotion(event)
		self.ondragin(event, target)

	def _onmouseover(self, event):
		self.ensure_enabled("mouseover")
		self._onmousemotion(event)
		self.onmouseover(event)

	def _onmousedown(self, event):
		self.ensure_enabled("mousedown")
		self.onmousedown(event)

	def _onclick(self, event):
		self.ensure_enabled("click")
		self.onclick(event)

	def _onmouseup(self, event):
		self.ensure_enabled("mouseup")
		self.onmouseup(event)

	def onmousemotion(self, event):
		pass

	def ondragover(self, event, target):
		pass

	def ondragout(self, event, target):
		pass

	def ondragin(self, event, target):
		pass

	def onmouseover(self, event):
		pass

	def onmousedown(self, event):
		pass

	def onmouseup(self, event):
		pass

	def onclick(self, event):
		pass
