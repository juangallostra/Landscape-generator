# Imports
import collections
import json
from urllib.request import Request, urlopen, URLError
from colourlovers_data_containers import *


# TODO
#       - proper error raising
# 	   	- implement switches (Lover -> ?comments=1)
# DONE 	- implement searches for new, top and random parameters.
# DONE	- check than when random is used no more parameters are used.
# DONE	- valid parameter types when doing unique searches
# 		- unicode to string conversion ? 
# DONE	- stats search


# API Wrapper
class ColourLovers(object):
    """
    ColourLovers API python wrapper
    """
    def __init__(self):

        self.__API_URL = "http://www.colourlovers.com/api/"

        # When searching for new, top or random use the request keyword in the called search method
        self.__API_REQUEST_KEYWORD = "request"
        self.__API_EXCLUSIVE_REQUEST = "random"
        self.__API_REQUEST_TYPE = {"colors": set({"new", "top", "random"}),
                                   "palettes": set({"new", "top", "random"}),
                                   "patterns": set({"new", "top", "random"}),
                                   "lovers": set({"new", "top"}),
                                   "stats": set({"colors", "palettes", "patterns", "lovers"}),
                                   "color": set(),
                                   "palette": set(),
                                   "pattern": set(),
                                   "lover": set()}

        self.__API_PARAMETERS = {"colors": set(
            {"lover", "hueRange", "briRange", "keywords", "keywordExact", "orderCol", "sortBy", "numResults",
             "resultOffset", "format", "jsonCallback"}),
            "palettes": set(
                {"lover", "hueOption", "hex", "hex_logic", "keywords", "keywordExact", "orderCol",
                 "sortBy", "numResults", "resultOffset", "format", "jsonCallback",
                 "showPaletteWidths"}),
            "patterns": set(
                {"lover", "hueOption", "hex", "hex_logic", "keywords", "keywordExact", "orderCol",
                 "sortBy", "numResults", "resultOffset", "format", "jsonCallback"}),
            "lovers": set(
                {"orderCol", "sortBy", "numResults", "resultOffset", "format", "jsonCallback"}),
            "stats": set({"format", "jsonCallback"}),
            "color": set({"format", "jsonCallback"}),
            "palette": set({"id", "format", "jsonCallback"}),
            "pattern": set({"format", "jsonCallback"}),
            "lover": set({"comments", "format", "jsonCallback"})}

        self.__API_SWITCHES = {"palette": set({"showPaletteWidths"}),
                               "lover": set({"comments"})}

        self.__API_ADD_PARAM = ["&", "=", "?", "/"]

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
        self.search_colors = self.__public_api_method(self.__API_COLORS, Color)
        self.search_color = self.__public_api_method(self.__API_COLOR, Color)
        self.search_palettes = self.__public_api_method(self.__API_PALETTES, Palette)
        self.search_palette = self.__public_api_method(self.__API_PALETTE, Palette)
        self.search_patterns = self.__public_api_method(self.__API_PATTERNS, Pattern)
        self.search_pattern = self.__public_api_method(self.__API_PATTERN, Pattern)
        self.search_lovers = self.__public_api_method(self.__API_LOVERS, Lover)
        self.search_lover = self.__public_api_method(self.__API_LOVER, Lover)
        self.search_stats = self.__public_api_method(self.__API_STATS, Stats)

    # Private methods

    def __public_api_method(self, search_type, data_container):
        def _api_search(raw_data=False, **kwargs):
            processed_request = self.__process_optional_requests(search_type, **kwargs)

            if not raw_data:  # if user hasn't asked for the raw data of the API response build container objects
                processed_request.kwargs["format"] = "json"

            api_response = self.__search(search_type, processed_request.optional_request, **processed_request.kwargs).decode()
            containers = self.__process_response(raw_data, api_response, data_container)
            if containers is not None:
                return containers
            else:
                print("The data you asked for could not be retrieved")
        return _api_search

    def __search(self, search_term, optional_request_term, **kwargs):
        try:
            self.__check_args(search_term, **kwargs)
        except ValueError as e:
            print(e)

        return self.__request(search_term, optional_request_term, **kwargs)

    def __check_args(self, search_term, **kwargs):
        if search_term not in self.__API_REQUEST_TYPE.keys():
            raise ValueError("Unsupported search: " + search_term)

        elif kwargs is not None:
            # Look for invalid arguments
            invalid_parameters = set(kwargs.keys()) - self.__API_PARAMETERS[search_term]
            if invalid_parameters:
                raise ValueError("Unsupported search argument/s: " + ', '.join(invalid_parameters))

            # Look for invalid argument value types
            types = [(i, type(value)) for (i, value) in enumerate(kwargs.values())]
            for parameter_type in types:
                if parameter_type[1] not in [list, str, int]:
                    raise ValueError("Unsupported argument value type " + str(parameter_type))
                # If the argument value is a list, the type of all the elements in the list should be
                # a valid type and the same type for all the values
                elif parameter_type[1] == list:
                    parameter_values_types = [type(parameter_value) for parameter_value in
                                              kwargs.values()[parameter_type[0]]]
                    type_selector = parameter_values_types[
                        0]  # Select the type of the first value in list as the parameter type
                    # and look for inconsistencies or invalid types
                    if type_selector not in [str, int]:
                        raise ValueError("Unsupported value type in argument " + str(kwargs.keys()[parameter_type[0]]))
                    for parameter_value_type in parameter_values_types:
                        if parameter_value_type != type_selector:
                            raise ValueError(
                                "Inconsistent value types in argument " + str(kwargs.keys()[parameter_type[0]]))
        else:
            return True

    def __request(self, search_term, optional_request_term, **kwargs):
        # build API request
        try:
            api_request_url = self.__API_URL + search_term + optional_request_term
        except:
            api_request_url = self.__API_URL + search_term

        for argument in kwargs.keys():
            # build API parameter specification string
            if type(kwargs[argument]) == list:
                values = ','.join([str(value) for value in kwargs[argument]])
            else:
                values = str(kwargs[argument])
            additional_parameter = self.__API_ADD_PARAM[0] + argument + self.__API_ADD_PARAM[1] + values
            # add parameter to API request
            api_request_url += additional_parameter
        # HTTP API request
        req = Request(api_request_url, headers={'User-Agent': "Magic Browser"})
        # Make request and read response
        try:
            response = urlopen(req)
            data = response.read()
            return data
        except URLError as e:
            print(e)

    def __process_response(self, raw_data, api_response, request_type_class):
        if api_response is not None:
            if raw_data:
                return api_response
            else:
                parsed_json = json.loads(api_response)
                if type(parsed_json) == dict:
                    response_containers = request_type_class(parsed_json)
                else:
                    response_containers = []
                    for element in parsed_json:
                        response_containers += [request_type_class(element)]
                return response_containers
        else:
            return None

    def __process_optional_requests(self, search_type, **kwargs):
        processed_request = collections.namedtuple('Processed_request', ['kwargs', 'optional_request'])

        optional_request_term = None

        if self.__API_REQUEST_KEYWORD in kwargs.keys():
            if type(kwargs[self.__API_REQUEST_KEYWORD]) == str:
                request = set({kwargs[self.__API_REQUEST_KEYWORD]})
                valid_request = bool(request.intersection(self.__API_REQUEST_TYPE[search_type]))
                if valid_request:
                    optional_request_term = self.__API_ADD_PARAM[3] + kwargs[self.__API_REQUEST_KEYWORD]
                    del kwargs[self.__API_REQUEST_KEYWORD]
                    # if the optional request is random/the search is for stats
                    # then ignore the rest of arguments since they are not allowed
                    if self.__API_EXCLUSIVE_REQUEST in request or search_type == self.__API_STATS:
                        kwargs = {}
                else:
                    raise ValueError("Unsupported request argument/s: " + kwargs[self.__API_REQUEST_KEYWORD])
            else:
                raise ValueError("Unsupported request argument type: " + str(type(kwargs[self.__API_REQUEST_KEYWORD])))

        return processed_request(kwargs=kwargs, optional_request=optional_request_term)
