'''
Created on May 24, 2012

@author: newatv2user
'''

PIANO_RPC_HOST = "tuner.pandora.com"
PIANO_ONE_HOST = "internal-tuner.pandora.com"
PIANO_RPC_PATH = "/services/json/?"

class PianoUserInfo:
    def __init__(self):
        self.listenerId = ''
        self.authToken = ''
        
class PianoStation:
    def __init__(self):
        self.isCreator = ''
        self.isQuickMix = ''
        self.useQuickMix = ''
        self.name = ''
        self.id = ''
        self.seedId = ''
        
        
# Piano Song Rating Enum
PIANO_RATE_NONE = 0
PIANO_RATE_LOVE = 1
PIANO_RATE_BAN = 2
class PianoSongRating:
    def __init__(self):
        self.Rating = PIANO_RATE_NONE

# Piano Audio Format Enum
PIANO_AF_UNKNOWN = 0
PIANO_AF_AACPLUS = 1
PIANO_AF_MP3 = 2
PIANO_AF_MP3_HI = 3
PIANO_AF_AACPLUS_LO = 4
class PianoAudioFormat:
    def __init__(self):
        self.Format = PIANO_AF_UNKNOWN

class PianoSong:
    def __init__(self):
        self.artist = ''
        self.stationId = ''
        self.album = ''
        self.audioUrl = ''
        self.coverArt = ''
        self.musicId = ''
        self.title = ''
        self.seedId = ''
        self.feedbackId = ''
        self.detailUrl = ''
        self.trackToken = ''
        self.fileGain = 0 
        self.rating = PianoSongRating()
        self.audioFormat = PianoAudioFormat()
        

class PianoArtist:
    def __init__(self):
        self.name = ''
        self.musicId = ''
        self.seedId = ''
        self.score = 0
        self.next = PianoArtist()

class PianoGenre:
    def __init__(self):
        self.name = ''
        self.musicId = ''
        

class PianoGenreCategory:
    def __init__(self):
        self.name = ''
        self.genres = PianoGenre()
        

class PianoPartner:
    def __init__(self):
        self.In = ''
        self.out = ''
        self.authToken = ''
        self.device = ''
        self.user = ''
        self.password = ''
        self.id = 0

class PianoSearchResult:
    def __init__(self):
        self.songs = PianoSong()
        self.artists = PianoArtist()

class PianoStationInfo:
    def __init__(self):
        self.songSeeds = PianoSong()
        self.artistSeeds = PianoArtist()
        self.stationSeeds = PianoStation()
        self.feedback = PianoSong()

# Piano Request Type Enum
#/* 0 is reserved: memset (x, 0, sizeof (x)) */ 
PIANO_REQUEST_LOGIN = 1
PIANO_REQUEST_GET_STATIONS = 2
PIANO_REQUEST_GET_PLAYLIST = 3
PIANO_REQUEST_RATE_SONG = 4
PIANO_REQUEST_ADD_FEEDBACK = 5
PIANO_REQUEST_MOVE_SONG = 6
PIANO_REQUEST_RENAME_STATION = 7
PIANO_REQUEST_DELETE_STATION = 8
PIANO_REQUEST_SEARCH = 9
PIANO_REQUEST_CREATE_STATION = 10
PIANO_REQUEST_ADD_SEED = 11
PIANO_REQUEST_ADD_TIRED_SONG = 12
PIANO_REQUEST_SET_QUICKMIX = 13
PIANO_REQUEST_GET_GENRE_STATIONS = 14
PIANO_REQUEST_TRANSFORM_STATION = 15
PIANO_REQUEST_EXPLAIN = 16
PIANO_REQUEST_BOOKMARK_SONG = 18
PIANO_REQUEST_BOOKMARK_ARTIST = 19
PIANO_REQUEST_GET_STATION_INFO = 20
PIANO_REQUEST_DELETE_FEEDBACK = 21
PIANO_REQUEST_DELETE_SEED = 22
class PianoRequestType:
    def __init__(self):
        self.RequestType = PIANO_REQUEST_LOGIN

class PianoRequest:
    def __init__(self):
        self.type = PianoRequestType()
        self.secure = False
        self.data = ''
        self.urlPath = [1024]
        self.postData = ''
        self.responseData = ''

#/* request data structures */ 
class PianoRequestDataLogin:
    def __init__(self):
        self.user = ''
        self.password = ''
        self.step = ''

class PianoRequestDataGetPlaylist:
    def __init__(self):
        self.station = PianoStation()
        self.format = PianoAudioFormat()
        self.retPlaylist = PianoSong()

class PianoRequestDataRateSong:
    def __init__(self):
        self.song = PianoSong()
        self.rating = PianoSongRating()

class PianoRequestDataAddFeedback:
    def __init__(self):
        self.stationId = ''
        self.trackToken = ''
        self.rating = PianoSongRating()

class PianoRequestDataMoveSong:
    def __init__(self):
        self.song = PianoSong()
        self.From = PianoStation()
        self.to = PianoStation()
        self.step = 0

class PianoRequestDataRenameStation:
    def __init__(self):
        self.station = PianoStation()
        self.newName = ''

class PianoRequestDataSearch:
    def __init__(self):
        self.searchStr = ''
        self.searchResult = PianoSearchResult()

class PianoRequestDataCreateStation:
    def __init__(self):
        self.type = ''
        self.id = ''

class PianoRequestDataAddSeed:
    def __init__(self):
        self.station = PianoStation()
        self.musicId = ''

class PianoRequestDataExplain:
    def __init__(self):
        self.song = PianoSong()
        self.retExplain = ''

class PianoRequestDataGetStationInfo:
    def __init__(self):
        self.station = PianoStation()
        self.info = PianoStationInfo()

class PianoRequestDataDeleteSeed:
    def __init__(self):
        self.song = PianoSong()
        self.artist = PianoArtist()
        self.station = PianoStation()

#/* pandora error code offset */ 
PIANO_RET_OFFSET = 1024
# Piano Return Enum
PIANO_RET_ERR = 0
PIANO_RET_OK = 1
PIANO_RET_INVALID_RESPONSE = 2
PIANO_RET_CONTINUE_REQUEST = 3
PIANO_RET_OUT_OF_MEMORY = 4
PIANO_RET_INVALID_LOGIN = 5
PIANO_RET_QUALITY_UNAVAILABLE = 6
PIANO_RET_P_INTERNAL = PIANO_RET_OFFSET + 0
PIANO_RET_P_API_VERSION_NOT_SUPPORTED = PIANO_RET_OFFSET + 11
PIANO_RET_P_BIRTH_YEAR_INVALID = PIANO_RET_OFFSET + 1025
PIANO_RET_P_BIRTH_YEAR_TOO_YOUNG = PIANO_RET_OFFSET + 1026
PIANO_RET_P_CALL_NOT_ALLOWED = PIANO_RET_OFFSET + 1008
PIANO_RET_P_CERTIFICATE_REQUIRED = PIANO_RET_OFFSET + 7
PIANO_RET_P_COMPLIMENTARY_PERIOD_ALREADY_IN_USE = PIANO_RET_OFFSET + 1007
PIANO_RET_P_DAILY_TRIAL_LIMIT_REACHED = PIANO_RET_OFFSET + 1035
PIANO_RET_P_DEVICE_ALREADY_ASSOCIATED_TO_ACCOUNT = PIANO_RET_OFFSET + 1014
PIANO_RET_P_DEVICE_DISABLED = PIANO_RET_OFFSET + 1034
PIANO_RET_P_DEVICE_MODEL_INVALID = PIANO_RET_OFFSET + 1023
PIANO_RET_P_DEVICE_NOT_FOUND = PIANO_RET_OFFSET + 1009
PIANO_RET_P_EXPLICIT_PIN_INCORRECT = PIANO_RET_OFFSET + 1018
PIANO_RET_P_EXPLICIT_PIN_MALFORMED = PIANO_RET_OFFSET + 1020
PIANO_RET_P_INSUFFICIENT_CONNECTIVITY = PIANO_RET_OFFSET + 13
PIANO_RET_P_INVALID_AUTH_TOKEN = PIANO_RET_OFFSET + 1001
PIANO_RET_P_INVALID_COUNTRY_CODE = PIANO_RET_OFFSET + 1027
PIANO_RET_P_INVALID_GENDER = PIANO_RET_OFFSET + 1027
PIANO_RET_P_INVALID_PARTNER_LOGIN = PIANO_RET_OFFSET + 1002
PIANO_RET_P_INVALID_PASSWORD = PIANO_RET_OFFSET + 1012
PIANO_RET_P_INVALID_SPONSOR = PIANO_RET_OFFSET + 1036
PIANO_RET_P_INVALID_USERNAME = PIANO_RET_OFFSET + 1011
PIANO_RET_P_LICENSING_RESTRICTIONS = PIANO_RET_OFFSET + 12
PIANO_RET_P_MAINTENANCE_MODE = PIANO_RET_OFFSET + 1
PIANO_RET_P_MAX_STATIONS_REACHED = PIANO_RET_OFFSET + 1005
PIANO_RET_P_PARAMETER_MISSING = PIANO_RET_OFFSET + 9
PIANO_RET_P_PARAMETER_TYPE_MISMATCH = PIANO_RET_OFFSET + 8
PIANO_RET_P_PARAMETER_VALUE_INVALID = PIANO_RET_OFFSET + 10
PIANO_RET_P_PARTNER_NOT_AUTHORIZED = PIANO_RET_OFFSET + 1010
PIANO_RET_P_READ_ONLY_MODE = PIANO_RET_OFFSET + 1000
PIANO_RET_P_SECURE_PROTOCOL_REQUIRED = PIANO_RET_OFFSET + 6
PIANO_RET_P_STATION_DOES_NOT_EXIST = PIANO_RET_OFFSET + 1006
PIANO_RET_P_UPGRADE_DEVICE_MODEL_INVALID = PIANO_RET_OFFSET + 1015
PIANO_RET_P_URL_PARAM_MISSING_AUTH_TOKEN = PIANO_RET_OFFSET + 3
PIANO_RET_P_URL_PARAM_MISSING_METHOD = PIANO_RET_OFFSET + 2
PIANO_RET_P_URL_PARAM_MISSING_PARTNER_ID = PIANO_RET_OFFSET + 4
PIANO_RET_P_URL_PARAM_MISSING_USER_ID = PIANO_RET_OFFSET + 5
PIANO_RET_P_USERNAME_ALREADY_EXISTS = PIANO_RET_OFFSET + 1013
PIANO_RET_P_USER_ALREADY_USED_TRIAL = PIANO_RET_OFFSET + 1037
PIANO_RET_P_LISTENER_NOT_AUTHORIZED = PIANO_RET_OFFSET + 1003
PIANO_RET_P_USER_NOT_AUTHORIZED = PIANO_RET_OFFSET + 1004
PIANO_RET_P_ZIP_CODE_INVALID = PIANO_RET_OFFSET + 1024
class PianoReturn:
    def __init__(self):
        self.Return = PIANO_RET_ERR

def PianoFindStationById (stations, searchStation):
    #/*    get station from list by id
    #*    @param search here
    #*    @param search for this
    #*    @return the first station structure matching the given id
    #*/
    for station in stations:
        if station.id == searchStation:
            return station        
    return None

def PianoErrorToStr (ret):
    #/*    convert return value to human-readable string
    #*    @param enum
    #*    @return error string
    #*/
    return {
             PIANO_RET_OK: "Everything is fine :)",
             PIANO_RET_ERR: "Unknown.",
             PIANO_RET_INVALID_RESPONSE: "Invalid response.",
             PIANO_RET_CONTINUE_REQUEST: "Fix your program.",
             PIANO_RET_OUT_OF_MEMORY: "Out of memory.",
             PIANO_RET_INVALID_LOGIN: "Wrong email address or password.",
             PIANO_RET_QUALITY_UNAVAILABLE: "Selected audio quality is not available.",
             PIANO_RET_P_INTERNAL: "Internal error.",
             PIANO_RET_P_CALL_NOT_ALLOWED: "Call not allowed.",
             PIANO_RET_P_INVALID_AUTH_TOKEN: "Invalid auth token.",
             PIANO_RET_P_MAINTENANCE_MODE: "Maintenance mode.",
             PIANO_RET_P_MAX_STATIONS_REACHED: "Max number of stations reached.",
             PIANO_RET_P_READ_ONLY_MODE: "Read only mode. Try again later.",
             PIANO_RET_P_STATION_DOES_NOT_EXIST: "Station does not exist.",
             PIANO_RET_P_INVALID_PARTNER_LOGIN: "Invalid partner login.",
             PIANO_RET_P_LICENSING_RESTRICTIONS: "Pandora is not available in your country. "\
             "Set up a control proxy (see manpage).",
             PIANO_RET_P_PARTNER_NOT_AUTHORIZED: "Invalid partner credentials.",
             PIANO_RET_P_LISTENER_NOT_AUTHORIZED: "Listener not authorized."
             }.get(ret, "No error message available.")
