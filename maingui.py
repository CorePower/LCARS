import pygame
from LCARS.Controls import *
from LCARS.Sound import Mixer
from pygame.color import Color

background = Color("grey10")
borders = Color("black")
buttontext = Color("black")
gold = Color("gold")
red = Color("orangered")

class Main(object):
	VALID_EVENT_NAMES = ["onmouseup", "onmousedown", "onmouseover", "ondrag", "ondragout", "ondragin"]

	def __init__(self, width, height, caption=None, surface=None, fullscreen=False):
		self.controls_l = []
		self.controls_m = {}
		self.width  = width
		self.height = height
		self.screenrect = pygame.Rect(0, 0, width, height)
		if surface is None:
			pygame.init()
			pygame.mixer.init()
			mode_flags = pygame.DOUBLEBUF|pygame.NOFRAME
			if fullscreen:
				mode_flags = mode_flags|pygame.FULLSCREEN
			pygame.display.set_mode((width, height), mode_flags)
			surface = pygame.display.get_surface()
		self.surface = surface
		self.set_caption(caption)
		self.running = True
		self.LAST_DRAG_CTRL = None

	def mainloop(self):
		clock = pygame.time.Clock()
		while self.running:
			clock.tick(60)
			self.repaint()
			self.dispatch_events()
		Mixer().wait()

	def set_caption(self, text):
		if text is None: text = ""
		pygame.display.set_caption(text)

	def add_control(self, name, ctrl):
		if self.controls_m.has_key(name):
			raise KeyError("control \"%s\" already exists" % name)
		self.controls_m[name] = ctrl
		self.controls_l.append(ctrl)
		return ctrl

	def install_handler(self, ctrlname, eventname, func):
		ctrl = self.controls_m[ctrlname]
		if eventname not in self.VALID_EVENT_NAMES:
			raise KeyError("no such event handler \"%s\"", eventname)
		setattr(ctrl, eventname, func)
		return ctrl

	def repaint(self, window=None):
		if window is None:
			window = self.surface
		pygame.draw.rect(window, background, self.screenrect)
		for ctrl in self.controls_l:
			ctrl.draw(window)
		pygame.display.flip()

	def find_control_at_point(self, pos, hookname):
		for ctrl in reversed(self.controls_l):
			if ctrl.collidePoint(pos):
				if ctrl.has_hook(hookname):
					return ctrl
		return None

	def shutdown(self):
		self.running = False

	def _onquit(self, event):
		self.onquit(event)

	def _onkeypress(self, event):
		self.onkeypress(event)

	def _onmousedown(self, event):
		ctrl = self.find_control_at_point(event.pos, "onmousedown")
		if ctrl is None: return
		self.LAST_DRAG_CTRL = ctrl
		ctrl._onmousedown(event)
		self.onmousedown(event)

	def _onmouseup(self, event):
		self.LAST_DRAG_CTRL = None
		ctrl = self.find_control_at_point(event.pos, "onmouseup")
		if ctrl is None: return
		ctrl._onmouseup(event)
		self.onmouseup(event)

	def _onmousemotion(self, event):
		ctrl = self.find_control_at_point(event.pos, "onmousemotion")
		if event.buttons == (0, 0, 0):
			if ctrl is None: return
			ctrl._onmouseover(event)
			self.onmouseover(event)
		else:
			if ctrl is None:
				if self.LAST_DRAG_CTRL is None: return
				self.LAST_DRAG_CTRL._ondragout(event)
				self.LAST_DRAG_CTRL = None
				self.ondrag(event)
			else:
				if ctrl == self.LAST_DRAG_CTRL:
					ctrl._ondragover(event)
					self.ondrag(event)
				else:
					if self.LAST_DRAG_CTRL is not None:
						self.LAST_DRAG_CTRL._ondragout(event)
						self.LAST_DRAG_CTRL = ctrl
					ctrl._ondragin(event)
					self.ondrag(event)

	def onquit(self, event):
		self.shutdown()

	def onkeypress(self, event):
		if event.key == pygame.K_ESCAPE:
			self.shutdown()

	def onmousedown(self, event):
		pass

	def onmouseup(self, event):
		pass

	def onmouseover(self, event):
		pass

	def ondrag(self, event):
		pass

	def onevent(self, event):
		if event.type == pygame.QUIT:
			self._onquit(event)
		elif event.type == pygame.KEYUP:
			self._onkeypress(event)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			self._onmousedown(event)
		elif event.type == pygame.MOUSEBUTTONUP:
			self._onmouseup(event)
		elif event.type == pygame.MOUSEMOTION:
			self._onmousemotion(event)

	def dispatch_events(self):
		for event in pygame.event.get():
			try:
				self.onevent(event)
			except KeyError:
				pass # ignore unregistered events
