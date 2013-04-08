'''
Created on May 29, 2012

@author: newatv2user
'''
import xbmcaddon
import piano

__script_id__ = "script.xbmc.pandorajson"
__settings__ = xbmcaddon.Addon(id=__script_id__)
class Settings:
    def __init__(self):
        self.autoselect = True
        self.history = 5
        self.volume = 0
        self.username = ''
        self.password = ''
        self.autostartStation = ''
        self.settings = __settings__
        # Check if Pandora One
        if self.settings.getSetting("pandoraone") == 'true':
            self.rpcHost = piano.PIANO_ONE_HOST
            self.partnerUser = "pandora one"
            self.partnerPassword = 'TVCKIBGS9AO9TSYLNNFUML0743LH82D'
            self.device = 'D01'
            self.inkey = 'U#IO$RZPAB%VX2'
            self.outkey = '2%3WCL*JU$MP]4'
            self.tlsFingerprint = 'B0A1EB460B1B6F33A1B6CB500C6523CB2E6EC946'
        else:
            self.rpcHost = piano.PIANO_RPC_HOST
            self.partnerUser = 'android'
            self.partnerPassword = 'AC7IBG09A3DTSYM4R41UJWL07VLN8JI7'
            self.device = 'android-generic'
            self.inkey = 'R=U!LH$O2B#'
            self.outkey = '6#26FRL$ZWD'
            self.tlsFingerprint = '\xA2\xA0\xBE\x8A\x37\x92\x39\xAE\x2B\x2E\x71\x4C\x56\xB3\x8B\xC1\x2A\x9B\x4B\x77'
        self.Base_Url = self.rpcHost + piano.PIANO_RPC_PATH
        self.username = self.settings.getSetting("username")
        self.password = self.settings.getSetting("password")
        fmt = int(self.settings.getSetting("quality"))
        self.audioFormat = ("lowQuality", "mediumQuality", "highQuality")[fmt]
        print 'Audio Format: ' + self.audioFormat
        #Proxy settings
        #print self.settings.getSetting("proxy_enable")
        self.proxy = False
        if self.settings.getSetting("proxy_enable") == 'true':
            print "PANDORA: Proxy Enabled"
            self.proxy = True
            self.proxy_info = {
                "host" : self.settings.getSetting("proxy_server"),
                "port" : self.settings.getSetting("proxy_port"),
                "user" : self.settings.getSetting("proxy_user"),
                "pass" : self.settings.getSetting("proxy_pass")
            }
