class GeometryException(Exception):
	pass

class StopEventBubbling(Exception):
	def __init__(self, hookname):
		Exception.__init__(self, "event bubbling stopped")
		self.hookname = hookname

class ControlIsDisabled(StopEventBubbling):
	def __init__(self, ctrl, hookname):
		StopEventBubbling.__init__(self, hookname)
		self.ctrl = ctrl
