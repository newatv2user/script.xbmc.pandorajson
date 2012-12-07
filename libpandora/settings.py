'''
Created on May 29, 2012

@author: newatv2user
'''
import xbmcaddon
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
        self.rpcHost = ''
        self.partnerUser = 'android'
        self.partnerPassword = 'AC7IBG09A3DTSYM4R41UJWL07VLN8JI7'
        self.device = 'android-generic'
        self.inkey = 'R=U!LH$O2B#'
        self.outkey = '6#26FRL$ZWD'
        self.tlsFingerprint = '\xA2\xA0\xBE\x8A\x37\x92\x39\xAE\x2B\x2E\x71\x4C\x56\xB3\x8B\xC1\x2A\x9B\x4B\x77'
        self.settings = __settings__
        self.username = self.settings.getSetting("username")
        self.password = self.settings.getSetting("password")
        fmt = int(self.settings.getSetting("quality"))
        self.audioFormat = ("lowQuality", "mediumQuality", "highQuality")[fmt]
        print 'Audio Format: ' + self.audioFormat
        #Proxy settings
        if bool(self.settings.getSetting("proxy_enable")):
            #print "PANDORA: Proxy Enabled"
            self.proxy = True
            self.proxy_info = {
                "host" : self.settings.getSetting("proxy_server"),
                "port" : self.settings.getSetting("proxy_port"),
                "user" : self.settings.getSetting("proxy_user"),
                "pass" : self.settings.getSetting("proxy_pass")
            }
