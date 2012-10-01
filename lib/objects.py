import Queue

class Track(object):
	def __init__(self, file, title=None, artist=None, album=[], id=None):
		self.file=file
		self.title=title
		self.artist=artist
		self.album=album
		self.id=id
		
	def debug(self):
		print '%s - %s | %s | %s'%(self.title,self.artist.name,self.albumprint(),self.file)
	
	def albumprint(self):
		text = ''
		for album in self.album:
			text = text + album.title + ' '
		return text
		
class Directory(object):
	def __init__(self, path):
		self.path = path
		self.tracks = []
		self.albums = {}
		self.q = Queue.Queue(maxsize=0)
		
	def add(self, track):
		self.tracks.append(track)
		self.q.put(track)
		
	def update(self, track):
		#add new albums to list		  V -  find new albums - V
		new = list(set(track.album) - set(self.albums.keys()))
		for album in new:
			self.albums[album]=0
		#update album probability
		self.probupdate(track)
		
	def probupdate(self, track):
		for album in track.album:
			self.albums[album] += 1
		
	def get(self):
		try:
			track = self.q.get_nowait()
		except Queue.Empty:
			return None
		
		return track
		
		
class Album(object):
	def __init__(self, title, artist = None, tracks = []):
		self.title = title
		self.artist = artist
		self.tracks = tracks
		
		

class Artist(object):
	def __init__(self, name, artist = None, albums = []):
		self.name = name
		self.albums = albums
		self.artist = artist
		
	def getAlbum(self, title = None):
		#search albums using title - return album object or None if not found
		if title:
			for album in self.albums:
				if album.title == title:
					return album
		return None
		
	def addAlbum(self, title):
		album = self.getAlbum(title)
		if not album:
			album = Album(title, self)
			self.albums.append(album)
		return album
		
		
class Library(object):
	def __init__(self):
		self.artists = []
		
	def addArtist(self,name):
		artist = self.getArtist(name)
		if not artist:
			artist = Artist(name, self)
			self.artists.append(artist)
		return artist
		
	def getArtist(self, name):
		for artist in self.artists:
			if artist.name == name:
				return artist
		return None
		
	def getAlbum(self, artist, title):
		for artist in self.artist:
			if artist.name == artist:
				for album in artist.album:
					if album.title == title:
						return album
		return None
				