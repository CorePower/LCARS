import pygame
from LCARSGui import *
from pygame.color import Color
from pygame.rect import Rect

pygame.init()

#f = pygame.font.Font("data/Swiss911ExtraCompressed.ttf", 12)

background = Color("grey10")
borders = Color("black")
buttontext = Color("black")
gold = Color("gold")
red = Color("orangered")

class GUI(object):
	VALID_EVENT_NAMES = ["onmouseup", "onmousedown", "onmouseover", "ondrag", "ondragout", "ondragin"]

	def __init__(self, width, height):
		self.controls_l = []
		self.controls_m = {}
		self.width  = width
		self.height = height
		self.screenrect = Rect(0, 0, width, height)
		self.running = True
		self.LAST_DRAG_CTRL = None

	def add_control(self, name, ctrl):
		if self.controls_m.has_key(name):
			raise KeyError("control \"%s\" already exists" % name)
		self.controls_m[name] = ctrl
		self.controls_l.append(ctrl)

	def install_handler(self, ctrlname, eventname, func):
		ctrl = self.controls_m[ctrlname]
		if eventname not in self.VALID_EVENT_NAMES:
			raise KeyError("no such event handler \"%s\"", eventname)
		setattr(ctrl, eventname, func)

	def repaint(self):
		window = pygame.display.get_surface()
		pygame.draw.rect(window, background, self.screenrect)
		for ctrl in self.controls_l:
			ctrl.draw(window)
		pygame.display.flip()

	def find_control_at_point(self, pos):
		for ctrl in self.controls_l:
			if ctrl.collidePoint(pos):
				return ctrl
		return None

	def shutdown(self):
		self.running = False

	def onquit(self, event):
		self.shutdown()

	def onkeypress(self, event):
		if event.key == pygame.K_ESCAPE:
			self.shutdown()

	def onmousedown(self, event):
		ctrl = self.find_control_at_point(event.pos)
		if ctrl is None: return
		self.LAST_DRAG_CTRL = ctrl
		print "mousedown"
		ctrl.onmousedown(event)

	def onmouseup(self, event):
		self.LAST_DRAG_CTRL = None
		ctrl = self.find_control_at_point(event.pos)
		if ctrl is None: return
		print "mouseup"
		ctrl.onmouseup(event)

	def onmousemotion(self, event):
		print "mousemotion", event.pos
		ctrl = self.find_control_at_point(event.pos)
		if event.buttons == (0, 0, 0):
			if ctrl is None: return
			ctrl.onmouseover(event)
		else:
			print ctrl, self.LAST_DRAG_CTRL
			if ctrl is None:
				if self.LAST_DRAG_CTRL is None: return
				self.LAST_DRAG_CTRL = None
				print "dragout"
				self.LAST_DRAG_CTRL.ondragout(event)
			else:
				if ctrl == self.LAST_DRAG_CTRL:
					ctrl.ondragover(event)
				else:
					self.LAST_DRAG_CTRL = ctrl
					ctrl.ondragin(event)

	def onevent(self, event):
		if event.type == pygame.QUIT:
			self.onquit(event)
		elif event.type == pygame.KEYUP:
			self.onkeypress(event)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			self.onmousedown(event)
		elif event.type == pygame.MOUSEBUTTONUP:
			self.onmouseup(event)
		elif event.type == pygame.MOUSEMOTION:
			self.onmousemotion(event)

	def dispatch_events(self):
		for event in pygame.event.get():
			try:
				self.onevent(event)
			except KeyError:
				print event
				pass # ignore unregistered events
