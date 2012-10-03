import Queue
import threading
import objects

class DirProcessor(threading.Thread):
	def __init__(self, workq, MusicId):
		self.workq = workq
		self.trackq = Queue.Queue(maxsize=0)
		self.MusicId = MusicId
		self.workers = []
		for x in range(0,4):
			worker = IdWorker(self.trackq, self.MusicId)
			worker.daemon = True
			self.workers.append(worker)
		self.alive=threading.Event()
		self.alive.set()
		threading.Thread.__init__(self)
	def run(self):
		while self.alive.isSet():
			try:
				dir = self.workq.get_nowait()
			except Queue.Empty:
				self.alive.clear()
			else:
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
		
	def run(self):
		while self.alive.isSet():
			self.process.wait()
				while self.process.isSet():
					try:
						track = self.parent.trackq.get_nowait()
					except Queue.Empty:
						self.process.clear()
					else:
						self.MusicId.id(track)
						self.parent.trackq.task_done()
			
	def join(self):
		self.alive.clear()
		self.process.set()	
		threading.Thread.join(1)
			
			
class DirScanner(threading.Thread):
	def __init__(self, workq):
		self.alive = threading.Event()
		self.alive.set()
		
		