import acoustid
import musicbrainz2.webservice as ws
import threading
import time
from objects import Track
#Acoustid API Key
API_KEY = 't4dNyiO4'
#test id 041d9dea-38e2-4322-a70b-0ae4aafb9f1f

class MusicId(object):
	def __init__(self, library):
		self.MusicB = MusicB()
		self.library = library
		
	def id(self, track):
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
		
	def lookup(self, data):
		if time.time() > self.lastcall+1:	
			self.resource.acquire()
			filter =  ws.TrackFilter(title=data[0], artistName=data[1], duration=data[2])
			tracks = self.mbQuery.getTracks(filter=filter)
			self.resource.release()
			self.lastcall += 1
			releaseobj = tracks[0].getTrack().getReleases()
			releases = []
			for re in releaseobj:
				releases.append(re.getTitle())
			releases = list(set(releases))
			return releases