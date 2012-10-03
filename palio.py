import lib.objects as objs
import lib.id_api as id
import Queue

class Palio(object):
	def __init__(self):
		self.unprocessed = Queue.Queue(maxsize=0)
		