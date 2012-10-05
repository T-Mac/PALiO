import lib.objects as objs
import lib.id_api as id
import Queue
import lib.workers as workers
import os
import os.path

class Palio(object):
	def __init__(self):
		self.unprocessed = Queue.Queue(maxsize=0)
		self.unscanned = Queue.Queue(maxsize=0)
		self.dirscanner = workers.DirScanner(self.unprocessed, self.unscanned)
		self.buildlist('/home/tmac/media/music')


	def buildlist(self, folder):
		for dir in os.listdir(folder):
			if os.path.isdir(dir):
				self.unscanned.put(os.path.join(folder,dir))
