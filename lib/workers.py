import Queue
import threading
import objects
import logging
import os
import os.path

LOGLVL = logging.DEBUG 
logging.basicConfig(level=LOGLVL, filename='debug.log', format='%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
class DirProcessor(threading.Thread):
	def __init__(self, workq, MusicId):
		self.workq = workq
		self.MusicId = MusicId
		self.workers = []
		self.trackq = Queue.Queue(maxsize=0)
		for x in range(0,4):
			worker = IdWorker(self, self.MusicId)
			worker.daemon = True
			worker.start()
			self.workers.append(worker)
		self.alive=threading.Event()
		self.alive.set()
		self.log = logging.getLogger('DirProcessor')
		threading.Thread.__init__(self)
	def run(self):
		while self.alive.isSet():
			try:
				dir = self.workq.get_nowait()
			except Queue.Empty:
				pass
			else:
				self.log.debug('Got New Dir Obj: %s'%dir.path)
				self.trackq = dir.q
				for worker in self.workers:
					worker.process.set()
				self.trackq.join()
				
	def join(self):
		self.alive.clear()
		for worker in self.workers:
			worker.join()
		threading.Thread.join(self)
		
class IdWorker(threading.Thread):
	def __init__(self, parent, MusicId):
		self.parent = parent
		self.MusicId = MusicId
		self.alive = threading.Event()
		self.alive.set()
		self.process = threading.Event()
		threading.Thread.__init__(self)
		self.log = logging.getLogger('ID Worker')
		
	def run(self):
		while self.alive.isSet():
			self.log.debug('Waiting For Job')
			self.process.wait()
			while self.process.isSet():
				try:
					track = self.parent.trackq.get_nowait()
				except Queue.Empty:
					self.process.clear()
				else:
					#self.log.debug('Got Track: %s'%track.file)
					self.MusicId.id(track)
					self.parent.trackq.task_done()
					self.log.error('Track IDed: %s'%track.title)
			
	def join(self):
		self.alive.clear()
		self.process.set()	
		threading.Thread.join(1)
			
			
class DirScanner(threading.Thread):
	def __init__(self, workq, unscanned):
		self.alive = threading.Event()
		self.alive.set()
		self.workq = workq
		self.unscanned = unscanned
		threading.Thread.__init__(self)
		self.log = logging.getLogger('DirScanner')
		
	def run(self):
			self.log.debug('Worker Started')
			while self.alive.isSet():
				try:
					path = self.unscanned.get_nowait()
					self.log.debug('Got job: %s'%path)
				except Queue.Empty:
					pass
				else:
					dirs = self.build(path)
					for dir in dirs:
						self.log.debug('new obj - %s'%dir.path)	
						self.workq.put(dir)

	def join(self):
		self.alive.clear()
		threading.Thread.join(self)
	
	def build(self, dir):
		objs = []
		for path, dirs, files in  os.walk(dir, topdown = True):
			if any('.mp3' in file for file in files):
				dirobj = objects.Directory(path)
				for file  in files:
					if '.mp3' in file:
						dirobj.addnew(os.path.join(path,file))
				objs.append(dirobj)
		return objs

