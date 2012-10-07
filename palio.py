import lib.objects as objs
import lib.id_api as id
import Queue
import lib.workers as workers
import os
import os.path
import logging
import threading
import lib.objects as objects

class Palio(object):
	def __init__(self):
		#create Q's
		self.unprocessed = Queue.Queue(maxsize=0)
		self.unscanned = Queue.Queue(maxsize=0)
		#create library
		self.library = objects.Library()
		#create MusicId
		self.musicid = id.MusicId(self.library)
		#create workers
		self.dirscanner = workers.DirScanner(self.unprocessed, self.unscanned)
		self.dirworkers = []
		for x in range(0,4):
		  worker = workers.DirProcessor(self.unprocessed, self.musicid)
		  worker.start()
		  self.dirworkers.append(worker)

		#setup logging
		self.loglvl = logging.DEBUG
		self.logfile = 'debug.log'
		logging.basicConfig(level=self.loglvl, filename=self.logfile, format='%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
		self.log = logging.getLogger('Palio')
		#create directory objects
		self.buildlist('/home/tmac/media/music/')
		self.alive = threading.Event()
		self.alive.set()

	def buildlist(self, folder):
		self.log.debug('Building Started')
		for dir in os.listdir(folder):
			self.log.debug('Testing: %s'%dir)
			if os.path.isdir(os.path.join(folder,dir)):
				self.unscanned.put(os.path.join(folder,dir))
				self.log.debug('added job: %s'%os.path.join(folder,dir))
