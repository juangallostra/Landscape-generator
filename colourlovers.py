import colourlovers_wrapper as cl

import json

class CommonData(object):
	def __init__ (self, json_data):
		self.id = json_data["id"]
		self.title = json_data["title"]
		self.username = json_data["userName"]
		self.numviews = json_data["numViews"]
		self.numvotes = json_data["numVotes"]
		self.numcomments = json_data["numComments"]
		self.numhearts = json_data["numHearts"]
		self.rank = json_data["rank"]
		self.date_created = json_data["dateCreated"]
		self.url = json_data["url"]
		self.image_url = json_data["imageUrl"]
		self.badge_url = json_data["badgeUrl"]
		self.api_url = json_data["apiUrl"]

#  id_num, title, username, numviews, numvotes, numcomments, numhearts, rank, date_created, url, image_url, badge_url, api_url, colors, color_widths, description

class Palette(CommonData):
	def __init__(self,json_data):
		ResponseData.__init__(self,json_data)
		self.color_widths = json_data["colorWidths"]
		self.description = json_data["description"]
		self.colors = json_data["colors"]
		self.num_colors = len(self.colors)

	def hex_to_rgb(self):	# TODO implement methods

	def hex_to_hsv(self):

class Color(CommonData):
	def __init__(self,json_data):
		data = json.loads(json_data)
		ResponseData.__init__(self,json_data)
		self.hex= json_data["hex"]
		self.RGB = RGB(json_data["rgb"]) # TODO implement attribute creation
		self.HSV = HSV(json_data["hsv"])
		self.description = json_data["description"]

class Pattern(CommonData):
	def __init__(self, json_data):
		pass

class Lover(object):
	def __init__(self, json_data):
		pass

class Stats(object):
	def __init__(self, json_data):
		pass

class RGB(object):
	def __init__(self,red,green,blue):
		self.red = red
		self.green = green
		self.blue = blue
		self.rgb = [red, green, blue]

class HSV(object):
	def __init__(self,hue,saturation,value):
		self.hue = hue
		self.saturation = saturation
		self.value = value
		self.hsv = [hue, saturation, value]
