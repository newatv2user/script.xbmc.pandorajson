# pandora client using json rpc
from settings import Settings
from crypt import Crypto
from piano import PianoPartner, PianoUserInfo, PianoStation, PianoSong, PianoFindStationById
import piano
import json
from utils import JsonGetURL
import time
import urllib, urllib2

#BASE_URL = piano.PIANO_RPC_HOST + piano.PIANO_RPC_PATH

class PandoraError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
    
class Pandora:
    def __init__(self):
        self.Settings = Settings()
        # Opener
        self.opener = urllib2.build_opener()
        # Proxy
        self.setProxy()
        # Partner Init
        self.partner = PianoPartner()
        self.partner.user = self.Settings.partnerUser
        self.partner.password = self.Settings.partnerPassword
        self.partner.device = self.Settings.device
        self.partner.In = Crypto(self.Settings.inkey)
        self.partner.out = Crypto(self.Settings.outkey)
        self.timeOffset = 0
        # User
        self.user = PianoUserInfo()
        # Station list
        self.stations = []        
        self.currentStation = None
        # Reauthentication
        self.Reauthenticate = False
        
    def PartnerLogin(self):
        # Try to login with partner info. Return false if unsuccessful.
        postData = json.dumps({"username": self.partner.user,
                                "password": self.partner.password,
                                "deviceModel": self.partner.device,
                                "version": "5",
                                "includeUrls": True})
        # Use secure connection for login
        Url = 'https://' + self.Settings.Base_Url + 'method=auth.partnerLogin'
        responseData = JsonGetURL(Url, postData, self.opener)
        if not self.ValidateResponse(responseData):
            return False
        responseJson = json.loads(responseData)
        result = responseJson["result"]
        cryptedTimestamp = result["syncTime"]
        decryptedTimestamp = self.partner.In.decrypt(cryptedTimestamp)
        if decryptedTimestamp and len(decryptedTimestamp) > 4:
            timestamp = long(decryptedTimestamp[4:-2])
            self.timeOffset = time.time() - timestamp
            
        self.partner.authToken = result["partnerAuthToken"]
        self.partner.id = int(result["partnerId"])
        return True
    
    def UserLogin(self):
        # Partner Login must be successful before calling UserLogin
        timestamp = time.time() - self.timeOffset
        postData = json.dumps({"loginType": "user",
                               "username": self.Settings.username,
                               "password": self.Settings.password,
                               "partnerAuthToken": self.partner.authToken,
                               "syncTime": timestamp})
        #print postData
        #return False
        encPostData = self.partner.out.encrypt(postData)
        urlencAuthToken = urllib.quote_plus(self.partner.authToken)
        # Use secure connection for login
        Url = 'https://' + self.Settings.Base_Url + "method=auth.userLogin&auth_token=%s&partner_id=%i" % (urlencAuthToken, self.partner.id)
        responseData = JsonGetURL(Url, encPostData, self.opener)
        #print "Response in UserLogin: " + responseData        
        if not self.ValidateResponse(responseData):
            return False
        responseJson = json.loads(responseData)
        result = responseJson["result"]
        self.user.listenerId = int(result["userId"])
        self.user.authToken = result["userAuthToken"]
        return True

    def GetStationList(self):
        # After successful login, try to get the station list for the user
        method = "user.getStationList"
        Url = self.ConstructURL(method)
        postDict = {}
        self.AppendPostData(postDict)        
        postData = json.dumps(postDict)
        encPostData = self.partner.out.encrypt(postData)        
        responseData = JsonGetURL(Url, encPostData, self.opener)
        if not self.ValidateResponse(responseData):
            return []
        responseJson = json.loads(responseData)
        result = responseJson["result"]
        stations = result["stations"]
        for station in stations:
            tmpStation = PianoStation()
            tmpStation.name = station["stationName"]
            tmpStation.id = station["stationToken"]
            tmpStation.isCreator = not bool(station["isShared"])
            tmpStation.isQuickMix = bool(station["isQuickMix"])
            self.stations.append(tmpStation)
        return self.stations
    
    def GetPlaylist(self, stationId):        
        # Set current station
        self.currentStation = PianoFindStationById(self.stations, stationId)
        postDict = {"stationToken": stationId}
        self.AppendPostData(postDict)
        postData = json.dumps(postDict)
        encPostData = self.partner.out.encrypt(postData)
        method = "station.getPlaylist"
        Url = self.ConstructURL(method, secure=True)
        responseData = JsonGetURL(Url, encPostData, self.opener)
        if not self.ValidateResponse(responseData):
            # Check if Re-authentication is required
            if self.Reauthenticate:
                self.ReAuthenticate()
                return self.GetPlaylist(stationId)
            else:
                return []
        responseJson = json.loads(responseData)
        result = responseJson["result"]
        items = result["items"]
        playlist = []
        for item in items:
            song = PianoSong()
            if not 'artistName' in item:
                continue
            artistName = item["artistName"]
            audioUrlMap = item["audioUrlMap"]
            if not audioUrlMap:
                continue
            song.audioUrl = audioUrlMap[self.Settings.audioFormat]["audioUrl"]
            song.artist = artistName
            song.album = item["albumName"]
            song.title = item["songName"]
            song.trackToken = item["trackToken"]
            song.stationId = item["stationId"]
            song.coverArt = item["albumArtUrl"]
            song.detailUrl = item["songDetailUrl"]
            song.fileGain = float(item["trackGain"])
            song.audioFormat = self.Settings.audioFormat
            songRating = int(item["songRating"])
            if songRating == 1:
                song.rating.Rating = piano.PIANO_RATE_LOVE            
            playlist.append(song)
        return playlist

    def AddFeedback(self, trackToken, isPositive):
        assert (self.currentStation != None)
        print 'Adding Feedback: ' + str(isPositive)
        postDict = {"stationToken": self.currentStation.id,
                    "trackToken": trackToken,
                    "isPositive": isPositive}
        self.AppendPostData(postDict)
        postData = json.dumps(postDict)
        encPostData = self.partner.out.encrypt(postData)
        method = "station.addFeedback"
        Url = self.ConstructURL(method)
        responseData = JsonGetURL(Url, encPostData, self.opener)
        if not self.ValidateResponse(responseData):
            # Check if Re-authentication is required
            if self.Reauthenticate:
                self.ReAuthenticate()
                self.AddFeedback(trackToken, isPositive)            
        
    def SetTired(self, trackToken):
        print 'Setting Tired'
        postDict = {"trackToken": trackToken}
        self.AppendPostData(postDict)
        postData = json.dumps(postDict)
        encPostData = self.partner.out.encrypt(postData)
        method = "user.sleepSong"
        Url = self.ConstructURL(method)
        responseData = JsonGetURL(Url, encPostData, self.opener)
        if not responseData:
            # Check if Re-authentication is required
            if self.Reauthenticate:
                self.ReAuthenticate()
                self.SetTired(trackToken)
        
    def ConstructURL(self, method, secure=False):
        urlencAuthToken = urllib.quote_plus(self.user.authToken)
        if secure:
            prefix = 'https://'
        else:
            prefix = 'http://'
        Url = prefix + self.Settings.Base_Url + "method=%s&auth_token=%s&partner_id=%i&user_id=%s" % (method,
                                                                                           urlencAuthToken,
                                                                                           self.partner.id,
                                                                                           self.user.listenerId)
        return Url

    def AppendPostData(self, postDict):
        postDict["userAuthToken"] = self.user.authToken
        postDict["syncTime"] = self.GetCorrectedTimestamp()
        
    def GetCorrectedTimestamp(self):
        return time.time() - self.timeOffset

    def setProxy(self):
        if not self.Settings.proxy:
            return
        if self.Settings.proxy_info["user"] == "" and self.Settings.proxy_info["pass"] == "":
            proxy_h = urllib2.ProxyHandler({ "http" : \
                "http://%(host)s:%(port)s" % self.Settings.proxy_info })
        else:
            proxy_h = urllib2.ProxyHandler({ "http" : \
                "http://%(user)s:%(pass)s@%(host)s:%(port)s" % self.Settings.proxy_info })

        proxy_o = urllib2.build_opener(proxy_h, urllib2.HTTPHandler)

        self.opener = proxy_o
        
    def ValidateResponse(self, response):
        if not response:
            return False
        responseJson = json.loads(response)
        stat = responseJson["stat"]
        if stat == "ok":
            return True
        if stat == "fail":
            if responseJson["code"] == 1001:    #INVALID_AUTH_TOKEN
                self.Reauthenticate = True
            return False 

    def ReAuthenticate(self):
        '''if self.PartnerLogin():
            if self.UserLogin():
                self.Reauthenticate = False'''
        if self.Login():
            self.Reauthenticate = False

    def Login(self):
        if self.PartnerLogin() == True:
            #print 'Partner Logged In'
            ret = self.UserLogin()
            return ret
        return False
