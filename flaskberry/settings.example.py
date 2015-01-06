DEBUG = False
SECRET_KEY = "cH4ng3_M3"

# List of enabled modules
ENABLED_MODULES = [
    "system",
    "disks",
    "movies",
]

# List of links to add to main navigation bar
EXTERNAL_LINKS = [
    # tuple of URL and name, e.g.
    # ('http://192.168.1.1/admin', 'Router Admin'),
]

# Configuration for the 'movie player'
# Path to where video files are stored
MOVIES_DIR = "/mnt/media/videos"
# Show files with these extensions
MOVIES_EXT = (u".mp4", u".webm", u".ogg", u".ogv")
# URL to the directory specified as MOVIES_DIR
MOVIES_URL = "http://raspberry/videos/"

# Configuration for subtitle laoding via opensubtitles.org
# preferred languages
MOVIES_OS_LANG = "eng"
# your username/password, optional
MOVIES_OS_USER = ""
MOVIES_OS_PASSWORD = ""
# User Agent
MOVIES_OS_UA = "OSTestUserAgent"
# API
MOVIES_OS_API = "http://api.opensubtitles.org/xml-rpc"
