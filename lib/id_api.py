import acoustid
import musicbrainz2.webservice as ws
import threading
import time
from objects import Track
import logging

#Acoustid API Key
API_KEY = 't4dNyiO4'
#test id 041d9dea-38e2-4322-a70b-0ae4aafb9f1f
LOGLVL = logging.ERROR
logging.basicConfig(level=LOGLVL, filename='debug.log', format='%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
class MusicId(object):
	def __init__(self, library):
		self.MusicB = MusicB()
		self.library = library
		
	def id(self, track):
		try:
			dur, fp = acoustid.fingerprint_file(track.file)
			response = acoustid.parse_lookup_result(acoustid.lookup(API_KEY,fp,dur,'recordings'))
			response = response.next()
			releases = self.search((response[2],response[3],dur*1000))
			track.title = response[2]
			artist = self.library.addArtist(response[3])
			track.artist = artist
			albums = []
			for album in releases:
				x = artist.addAlbum(album)
				albums.append(x)
			track.album = albums
		except EOFError:
			track.title = 'ERROR'

		except StopIteration:
			track.title = 'ERROR'

	
	def search(self, data):
		releases = self.MusicB.lookup(data)
		return releases
	
		
class MusicB(object):
	def __init__(self):
		#create Query object and include
		self.mbQuery = ws.Query()
		#create thread sync stuff
		self.resource = threading.Semaphore(2)
		self.lastcall = time.time()
		self.log = logging.getLogger('MusicB')
	def lookup(self, data):
		x = True
		while x:
			if time.time() > self.lastcall+1:	
				self.resource.acquire()
				filter =  ws.TrackFilter(title=data[0], artistName=data[1], duration=data[2])
				tracks = self.mbQuery.getTracks(filter=filter)
				self.resource.release()
				self.lastcall = time.time()
				try:
					releaseobj = tracks[0].getTrack().getReleases()
					releases = []
					for re in releaseobj:
						releases.append(re.getTitle())
					releases = list(set(releases))
				except IndexError:
					self.log.error('INDEX ERROR: %s'%tracks)
					releases = []
				x = False
				return releases
			else:
				time.sleep(1)
