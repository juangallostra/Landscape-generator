## 

# Imports
from urllib2 import Request, urlopen, URLError
import json
from colourlovers_data_containers import *
import collections

# TODOs
# 	   	- implement switches (Lover -> ?comments=1)
# DONE 	- implement searches for new, top and random parametres.
#		- check than when random is used no more parametres are used.
# 		- valid parameter types when doing unique searches
# 		- unicode to string conversion ? 
# 		- stats search


# API Wrapper
class ColourLovers(object):
	'''
	ColourLovers API python wrapper
	'''
	def __init__(self):

		self.__API_URL = "http://www.colourlovers.com/api/"

		# when searching for new, top or random use the request keyword in the called search method
		self.__API_REQUEST_KWRD = "request"
		self.__API_EXCLUSIVE_REQUEST = "random"
		self.__API_REQUEST_TYPE = {"colors":set({"new","top","random"}),
									"palettes":set({"new","top","random"}),
									"patterns":set({"new","top","random"}),
									"lovers":set({"new","top"}),
									"stats":set({"colors", "palettes", "patterns", "lovers"}),
									"color":set(),
									"palette":set(),
									"pattern":set(),
									"lover":set()}

		self.__API_PARAMETRES = {"colors":set({"lover","hueRange","briRange","keywords","keywordExact","orderCol","sortBy","numResults","resultOffset","format","jsonCallback"}),
								 "palettes":set({"lover","hueOption","hex","hex_logic","keywords","keywordExact","orderCol","sortBy","numResults","resultOffset","format","jsonCallback","showPaletteWidths"}),
								 "patterns":set({"lover","hueOption","hex","hex_logic","keywords","keywordExact","orderCol","sortBy","numResults","resultOffset","format","jsonCallback"}),
								 "lovers":set({"orderCol","sortBy","numResults","resultOffset","format","jsonCallback"}),
								 "stats":set({"format","jsonCallback"}),
								 "color":set({"format","jsonCallback"}),
								 "palette":set({"id","format","jsonCallback"}),
								 "pattern":set({"format","jsonCallback"}),
								 "lover":set({"comments","format","jsonCallback"})}

		self.__API_SWITCHES = {"palette":set({"showPaletteWidths"}),
								"lover":set({"comments"})}

		self.__API_ADD_PARAM = ["&","=","?","/"]

		self.__API_COLORS = "colors"
		self.__API_PALETTES = "palettes" 
		self.__API_PATTERNS = "patterns"
		self.__API_LOVERS = "lovers"
		self.__API_STATS = "stats"
		self.__API_COLOR = "color"
		self.__API_PALETTE = "palette" 
		self.__API_PATTERN = "pattern"
		self.__API_LOVER = "lover"


	# Public methods
	def search_colors(self, raw_data=False, **kwargs):
		processed_request =  self.__process_optional_requests(self.__API_COLORS, **kwargs)	

		if raw_data == False:		# if user hasn't asked for the raw data of the API response build container objects 
			processed_request.kwargs["format"] = "json"

		api_response = self.__search(self.__API_COLORS, processed_request.optional_request, **processed_request.kwargs)

		containers = self.__process_response(raw_data, api_response, Color) 

		if containers is not None:
			return containers
		else:
			print "The data you asked for could not be retrieved"


	def search_color(self, raw_data=False, **kwargs):
		if raw_data == False:		# if user hasn't asked for the raw data of the API response build container objects 
			kwargs["format"] = "json"

		api_response = self.__search(self.__API_COLOR, None, **kwargs)

		containers = self.__process_response(raw_data, api_response, Color) 

		if containers is not None:
			return containers
		else:
			print "The data you asked for could not be retrieved"


	def search_palettes(self, raw_data=False, **kwargs):
		processed_request =  self.__process_optional_requests(self.__API_PALETTES, **kwargs)

		if raw_data == False:		# if user hasn't asked for the raw data of the API response build container objects 
			processed_request.kwargs["format"] = "json"

		api_response = self.__search(self.__API_PALETTES, processed_request.optional_request, **processed_request.kwargs)

		containers = self.__process_response(raw_data, api_response, Palette) 

		if containers is not None:
			return containers
		else:
			print "The data you asked for could not be retrieved"


	def search_palette(self, raw_data=False, **kwargs):
		if raw_data == False:		# if user hasn't asked for the raw data of the API response build container objects 
			kwargs["format"] = "json"

		# implement switch

		api_response = self.__search(self.__API_PALETTE, None, **kwargs)

		containers = self.__process_response(raw_data, api_response, Palette) 

		if containers is not None:
			return containers
		else:
			print "The data you asked for could not be retrieved"


	def search_patterns(self, raw_data=False, **kwargs):
		processed_request =  self.__process_optional_requests(self.__API_PATTERNS, **kwargs)

		if raw_data == False:		# if user hasn't asked for the raw data of the API response build container objects 
			processed_request.kwargs["format"] = "json"

		api_response = self.__search(self.__API_PATTERNS, processed_request.optional_request, **processed_request.kwargs)

		containers = self.__process_response(raw_data, api_response, Pattern) 

		if containers is not None:
			return containers
		else:
			print "The data you asked for could not be retrieved"


	def search_pattern(self, raw_data=False, **kwargs):
		if raw_data == False:		# if user hasn't asked for the raw data of the API response build container objects 
			kwargs["format"] = "json"

		api_response = self.__search(self.__API_PATTERN, None, **kwargs)

		containers = self.__process_response(raw_data, api_response, Pattern) 

		if containers is not None:
			return containers
		else:
			print "The data you asked for could not be retrieved"


	def search_lovers(self, raw_data=False, **kwargs):
		processed_request =  self.__process_optional_requests(self.__API_LOVERS, **kwargs)

		if raw_data == False:		# if user hasn't asked for the raw data of the API response build container objects 
			processed_request.kwargs["format"] = "json"

		api_response = self.__search(self.__API_LOVERS, processed_request.optional_request, **processed_request.kwargs)

		containers = self.__process_response(raw_data, api_response, Lover) 

		if containers is not None:
			return containers
		else:
			print "The data you asked for could not be retrieved"


	def search_lover(self, raw_data=False, **kwargs):
		if raw_data == False:		# if user hasn't asked for the raw data of the API response build container objects 
			kwargs["format"] = "json"

		# implement comments switch

		api_response = self.__search(self.__API_LOVER, None, **kwargs)

		containers = self.__process_response(raw_data, api_response, Lover) 

		if containers is not None:
			return containers
		else:
			print "The data you asked for could not be retrieved"


	def search_stats(self, raw_data=False, **kwargs):
		processed_request =  self.__process_optional_requests(self.__API_STATS, **kwargs)

		if raw_data == False:		# if user hasn't asked for the raw data of the API response build container objects 
			processed_request.kwargs["format"] = "json"

		api_response = self.__search(self.__API_STATS, processed_request.optional_request, **processed_request.kwargs)

		containers = self.__process_response(raw_data, api_response, Stats) 

		if containers is not None:
			return containers
		else:
			print "The data you asked for could not be retrieved"




	# Private methods
	def __search(self, searchterm, optional_request_term, **kwargs):
		try: 
			self.__check_args(searchterm, **kwargs)
		except ValueError as e:
			print(e)

		return self.__request(searchterm, optional_request_term, **kwargs)
			

	def __check_args(self, searchterm, **kwargs):
		if searchterm not in self.__API_REQUEST_TYPE.keys():
			raise ValueError("Unsupported search: "+searchterm)

		elif kwargs is not None:
			# Look for invalid arguments
			invalid_parameters = set(kwargs.keys())-self.__API_PARAMETRES[searchterm]
			if invalid_parameters:
				raise ValueError("Unsupported search argument/s: "+', '.join(invalid_parameters))

			# Look for invalid argument value types
			types = [(i,type(value)) for (i,value) in enumerate(kwargs.values())]
			for parameter_type in types:
				if parameter_type[1] not in [list,str,int]:
					raise ValueError("Unsupported argument value type "+str(parameter_type))
				# If the argument value is a list, the type of all the elements in the list should be
				# a valid type and the same type for all the values
				elif parameter_type[1]==list:
					parameter_values_types = [type(parameter_value) for parameter_value in kwargs.values()[parameter_type[0]]]
					type_selector = parameter_values_types[0] # Select the type of the first value in list as the parameter type
															  # and look for inconsistencies or invalid types
					if type_selector not in [str,int]:
						raise ValueError("Unsupported value type in argument "+str(kwargs.keys()[parameter_type[0]]))
					for parameter_value_type in parameter_values_types:
						if parameter_value_type != type_selector:
							raise ValueError("Inconsistent value types in argument "+str(kwargs.keys()[parameter_type[0]]))
		else:
			return True



	def __request(self,searchterm, optional_request_term, **kwargs):
		# build API request
		try:
			api_request_url = self.__API_URL+searchterm+optional_request_term
		except:
			api_request_url = self.__API_URL+searchterm

		for argument in kwargs.keys():
			# build API parameter specification string
			if type(kwargs[argument])==list:
				values = ','.join([str(value) for value in kwargs[argument]])
			else:
				values = str(kwargs[argument])
			additional_parameter = self.__API_ADD_PARAM[0]+argument+self.__API_ADD_PARAM[1]+values
			# add parameter to API request
			api_request_url+=additional_parameter

		# HTTP API request
		req = Request(api_request_url, headers={'User-Agent' : "Magic Browser"})

		# Make request and read response
		try:
			response = urlopen(req)
			data = response.read()
			return data
		except URLError, e:
			print 'Error', e


	def __process_response(self, raw_data, api_response, request_type_class):
		if api_response is not None:
			if raw_data == True:
				return api_response
			else:
				parsed_json = json.loads(api_response)
				if type(parsed_json)==dict:
					response_containers = request_type_class(parsed_json)
				else:
					response_containers = []
					for element in parsed_json:
						response_containers+=[request_type_class(element)]
				return response_containers
		else:
			return None


	def __process_optional_requests(self, search_type, **kwargs):
		processed_request = collections.namedtuple('Processed_request',['kwargs','optional_request'])

		optional_request_term = None

		if self.__API_REQUEST_KWRD in kwargs.keys():
			if type(kwargs[self.__API_REQUEST_KWRD]) == str:
				request = set({kwargs[self.__API_REQUEST_KWRD]})
				valid_request =  bool(request.intersection(self.__API_REQUEST_TYPE[search_type]))
				if valid_request:
					optional_request_term = self.__API_ADD_PARAM[3]+kwargs[self.__API_REQUEST_KWRD]
					del kwargs[self.__API_REQUEST_KWRD]
					if self.__API_EXCLUSIVE_REQUEST in request or search_type == self.__API_STATS: # if the optional request is random/the search is for stats
																								   # then ignore the rest of arguments since they are not allowed
						kwargs = {}
				else:
					raise ValueError("Unsupported request argument/s: "+ kwargs[self.__API_REQUEST_KWRD])
			else:
				raise ValueError("Unsupported request argument type: "+str(type(kwargs[self.__API_REQUEST_KWRD])))

		return processed_request(kwargs=kwargs, optional_request=optional_request_term)
