import xbmcgui
import xbmc
import xbmcaddon
import os, sys

__title__ = "Pandora"
__script_id__ = "script.xbmc.pandorajson"
__settings__ = xbmcaddon.Addon(id=__script_id__)
__version__ = "1.2.11-git"

print "PANDORA: Initializing v%s" % __version__
print "PANDORA: sys.platform = %s" % sys.platform

dlg = xbmcgui.DialogProgress()
dlg.create("PANDORA", "Loading Script...")
dlg.update(0)

from libpandora.pandora import Pandora, PandoraError

from pandagui import PandaGUI
from pandaplayer import PandaPlayer

scriptPath = __settings__.getAddonInfo('path')

dataDir = os.path.join("special://profile/addon_data/%s/" % __script_id__)

#Workaround: open() doesn't translate path correctly on some versions
dataDir = xbmc.translatePath(dataDir)

if __settings__.getSetting("firstrun") == "true":
	print  "PANDORA: First run, showing settings dialog"
	__settings__.openSettings()
	__settings__.setSetting("firstrun", "false")

class PandaException(Exception):
	def __init__(self):
		xbmcgui.Dialog().ok("Pandora", \
			"An exception has occurred. Disable Pandora One and try again")
	pass

class Panda:

	def __init__(self):
		self.gui = None
		self.pandora = None
		self.playlist = []
		self.curStation = ""
		self.curSong = None
		self.playing = False
		self.skip = False
		self.die = False
		self.settings = __settings__
		self.player = None
		self.skinName = "Default"
		
		try:
			self.pandora = Pandora()
		except PandoraError, e:
			xbmcgui.Dialog().ok("Pandora", "Error: %s" % e)
			self.die = True
			return

		while not self.auth():
			resp = xbmcgui.Dialog().yesno("Pandora", \
					"Failed to authenticate listener.", \
					"Check username/password and try again.", \
					"Show Settings?")
			if resp:
				self.settings.openSettings()
			else:
				self.Quit()
				return

		# Get skin from settings.
		# Check if a value is set in the settings. If not then use Default.
		if self.settings.getSetting ("skin") != "":
			self.skinName = self.settings.getSetting("skin")
		
		self.player = PandaPlayer(panda=self)

		self.gui = PandaGUI("script-pandora.xml", scriptPath, self.skinName)
		
		self.gui.setPanda(self)

	def auth(self):
		dlg = xbmcgui.DialogProgress()
		dlg.create("PANDORA", "Logging In...")
		dlg.update(0)
		'''partnerResult = self.pandora.PartnerLogin()
		if not partnerResult:
			dlg.close()
			return partnerResult
		ret = self.pandora.UserLogin()'''
		ret = self.pandora.Login()
		dlg.close()
		return ret

	def playStation(self, stationId):
		self.curStation = stationId
		self.curSong = None
		self.playlist = []
		self.getMoreSongs()
		self.playing = True
		self.playNextSong()

	def getStations(self):
		return self.pandora.GetStationList()
	
	def getMoreSongs(self):
		if self.curStation == "":
			raise PandaException()
		items = []
		fragment = self.pandora.GetPlaylist(self.curStation)
		if len(fragment) < 1:
			raise PandaException()
		for s in fragment:

			thumbnail = s.coverArt
			
			item = xbmcgui.ListItem(s.title)
			item.setIconImage(thumbnail)
			item.setThumbnailImage(thumbnail)
			item.setProperty("Cover", thumbnail)
			item.setProperty("MusicId", s.trackToken)
			if s.rating:
				item.setProperty("Rating", str(s.rating.Rating))
			else:
				item.setProperty("Rating", "0")
			
			info = { "title"	:	s.title, \
					 "artist"	:	s.artist, \
					 "album"	:	s.album }
			print "PANDORA: item info = %s" % info
			item.setInfo("music", info)
			items.append((s.audioUrl, item))

		self.playlist.extend(items)

	def playNextSong(self):
		if not self.playing:
			raise PandaException()
		try:
			Next = self.playlist.pop(0)
			self.player.playSong(Next)
			art = Next[1].getProperty("Cover")
			self.gui.setProperty("AlbumArt", art)
			self.curSong = Next
			
			rating = int(Next[1].getProperty("Rating"))
			self.gui.setRating(rating)
			
		except IndexError:
			self.curSong = None
			self.getMoreSongs()

		if len(self.playlist) == 0:
			#Out of songs, grab some more while playing
			self.getMoreSongs()

	def skipSong(self):
		self.skip = True
		self.player.stop()

	def addFeedback(self, likeFlag):
		if not self.playing:
			raise PandaException()
		musicId = self.curSong[1].getProperty("MusicId")
		self.pandora.AddFeedback(musicId, likeFlag)

	def addTiredSong(self):
		if not self.playing:
			raise PandaException()
		musicId = self.curSong[1].getProperty("MusicId")
		self.pandora.SetTired(musicId)

	def main(self):
		if self.die:
			return
		self.gui.doModal()
		self.cleanup()
		xbmc.sleep(500) #Wait to make sure everything finishes

	def stop(self):
		self.playing = False
		if self.player and self.player.timer\
				and self.player.timer.isAlive():
			self.player.timer.stop()

	def cleanup(self):
		self.skip = False
		if self.playing:
			self.playing = False
			self.player.stop()
		del self.gui
		del self.player

	def Quit(self):
		if self.player and self.player.timer\
				and self.player.timer.isAlive():
			self.player.timer.stop()
		if self.gui != None:
			self.gui.close()
		self.die = True

if __name__ == '__main__':
	if __settings__.getSetting("username") == "" or \
		__settings__.getSetting("password") == "":
		xbmcgui.Dialog().ok("Pandora", \
			"Username and/or password not specified")
		__settings__.setSetting("firstrun", "true")
	else:
		panda = Panda()
		dlg.close()
		panda.main()
