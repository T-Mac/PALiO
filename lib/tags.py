import mutagen

def tagupdate(self, track):
	audio = mutagen.File(track.file, easy=True)
	audio.delete()
	audio['title'] = track.title
	audio['album'] = track.album.title
	audio['artist'] = track.artist.name
	audio.save()