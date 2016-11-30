## Initial skecthes on building an API wrapper to get color palettes (Colourlovers API)

# Imports
from urllib2 import Request, urlopen, URLError

# buld API call url
request = "http://www.colourlovers.com/api/palettes" # Accessing palette catalog
topic = "mountain"                                   # Topic to search for
url = request+"&keywords="+topic                     # Request url

# HTTP request
req = Request(url, headers={'User-Agent' : "Magic Browser"})

# Ask for palettes and read response
try:
	response = urlopen(req)
	kittens = response.read()
	print kittens
except URLError, e:
    print 'Error', e
