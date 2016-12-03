## Initial skecthes on building an API wrapper to get color palettes (Colourlovers API)

# Imports
from urllib2 import Request, urlopen, URLError

# buld API call url
request = "http://www.colourlovers.com/api/palettes" # Accessing palette catalog
topic = "mountain"                                   # Topic to search for
url = request+"&keywords="+topic                     # Request url

#HTTP request
req = Request(url, headers={'User-Agent' : "Magic Browser"})

#Ask for palettes and read response
try:
	response = urlopen(req)
	kittens = response.read()
	#print kittens
except URLError, e:
    #print 'Error', e
        pass


class ColourLovers(object):
	'''
		ColourLovers API python wrapper
	'''
	def __init__(self):
		self.__API_URL        = "http://www.colourlovers.com/api/"
		self.__API_REQUESTS   = {"colors":set({"new","top","random"}),
								 "palettes":set({"new","top","random"}),
								 "patterns":set({"new","top","random"}),
								 "lovers":set({"new","top"}),
								 "stats":set({"colors", "palettes", "patterns", "lovers"})}
		self.__API_PARAMETRES = {"colors":set({"lover","hueRange","briRange","keywords","keywordExact","orderCol","sortBy","numResults","resultOffset","format","jsonCallback"}),
								 "palettes":set({"lover","hueOption","hex","hex_logic","keywords","keywordExact","orderCol","sortBy","numResults","resultOffset","format","jsonCallback","showPaletteWidths"}),
								 "patterns":set({"lover","hueOption","hex","hex_logic","keywords","keywordExact","orderCol","sortBy","numResults","resultOffset","format","jsonCallback"}),
								 "lovers":set({"orderCol","sortBy","numResults","resultOffset","format","jsonCallback"}),
								 "stats":set({"format","jsonCallback"})}
		self.__API_ADD_PARAM  = ["&","="]

		self.__API_COLORS     = "colors"
		self.__API_PALETTES   = "palettes" 
		self.__API_PATTERNS   = "patterns"
		self.__API_LOVERS     = "lovers"
		self.__API_STATS      = "stats"

	# Public methods
	def search_colors(self, **kwargs):
		self.__search(self.__API_COLORS, **kwargs)
		pass

	def search_palettes(self, **kwargs):
		self.__search(self.__API_PALETTES, **kwargs)
		pass

	def search_patterns(self, **kwargs):
		self.__search(self.__API_PATTERNS, **kwargs)
		pass

	def search_lovers(self, **kwargs):
		self.__search(self.__API_LOVERS, **kwargs)
		pass

	def search_stats(self, **kwargs):
		self.__search(self.__API_STATS, **kwargs)
		pass



	# Private methods

	def __search(self, searchterm, **kwargs):
		try: 
			self.__check_args(searchterm, **kwargs)
		except ValueError as e:
			print(e)
			
	def __check_args(self, searchterm, **kwargs):
                
		if searchterm not in self.__API_REQUESTS.keys():
			raise ValueError("Unsupported search: "+searchterm)

		elif kwargs is not None:
				invalid_parameters = set(kwargs.keys())-self.__API_PARAMETRES[searchterm]
				if invalid_parameters:
					raise ValueError("Unsupported search parameter/s: "+', '.join(invalid_parameters))

		else:
			return True

