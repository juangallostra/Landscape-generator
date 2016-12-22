import colorsys
from PIL import Image, ImageDraw


# Data containers for API responses
class CommonData(object):
    def __init__(self, json_data):
        self.id = json_data["id"]
        self.title = json_data["title"]
        self.username = json_data["userName"]
        self.num_views = json_data["numViews"]
        self.num_votes = json_data["numVotes"]
        self.num_comments = json_data["numComments"]
        self.num_hearts = json_data["numHearts"]
        self.rank = json_data["rank"]
        self.date_created = json_data["dateCreated"]
        self.description = json_data["description"]
        self.url = json_data["url"]
        self.image_url = json_data["imageUrl"]
        self.badge_url = json_data["badgeUrl"]
        self.api_url = json_data["apiUrl"]


class Palette(CommonData):
    def __init__(self, json_data):
        CommonData.__init__(self, json_data)
        try:
            self.color_widths = json_data["colorWidths"]
        except:
            pass

        self.colors = json_data["colors"]
        self.num_colors = len(self.colors)

    def hex_to_rgb(self):
        # Converts color in hex to RGB. Returns list of tuples where the channel order is (R,G,B)
        return [tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) for hex_color in self.colors]

    def hex_to_hsv(self):
        # Converts color in hex to HSV. Returns list of tuples such that each tuple is (H,S,V)
        return [tuple(colorsys.rgb_to_hsv(rgb_color[0], rgb_color[1], rgb_color[2])) for rgb_color in self.hex_to_rgb()]

    def draw(self, tile_size=24, offset=8):
        # Allows the visualization of the palette
        im = Image.new("RGB", ((offset+tile_size+offset)*self.num_colors, tile_size), "black")
        draw = ImageDraw.Draw(im)
        rgb_colors = self.hex_to_rgb()
        for i in range(self.num_colors):
            draw.rectangle((((offset+tile_size)*i, 0), ((offset+tile_size)*(i+1)-offset, tile_size)), fill=rgb_colors[i])

        im.show()


class Color(CommonData):
    def __init__(self, json_data):
        CommonData.__init__(self, json_data)
        self.hex = json_data["hex"]
        self.RGB = RGB(json_data["rgb"])
        self.HSV = HSV(json_data["hsv"])

    def draw(self, tile_size=24, offset=8):
        # Allows visualization of the color
        im = Image.new("RGB", ((offset+tile_size+offset), tile_size), "black")
        draw = ImageDraw.Draw(im)
        draw.rectangle((((offset+tile_size), 0), (tile_size, tile_size)), fill=self.RGB.rgb)
        im.show()


class Pattern(CommonData):
    def __init__(self, json_data):
        CommonData.__init__(self, json_data)
        self.colors = json_data["colors"]
        self.num_colors = len(self.colors)

    def hex_to_rgb(self):
        # converts color in hex to RGB. Returns list of tuples where the channel order is (R,G,B)
        return [tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) for hex_color in self.colors]

    def hex_to_hsv(self):
        # converts color in hex to HSV. Returns list of tuples such that each tuple is (H,S,V)
        return [tuple(colorsys.rgb_to_hsv(rgb_color[0], rgb_color[1], rgb_color[2])) for rgb_color in self.hex_to_rgb()]

    def draw(self, tile_size=24, offset=8):
        # Allows the visualization of the palette
        im = Image.new("RGB", ((offset+tile_size+offset)*self.num_colors, tile_size), "black")
        draw = ImageDraw.Draw(im)
        rgb_colors = self.hex_to_rgb()
        for i in range(self.num_colors):
            draw.rectangle((((offset+tile_size)*i, 0), ((offset+tile_size)*(i+1)-offset, tile_size)), fill=rgb_colors[i])

        im.show()


class Lover(object):
    def __init__(self, json_data):
        self.id = json_data["id"]
        self.username = json_data["userName"]
        self.date_registered = json_data["dateRegistered"]
        self.date_last_active = json_data["dateLastActive"]
        self.rating = json_data["rating"]
        self.location = json_data["location"]
        self.num_colors = json_data["numColors"]
        self.num_palettes = json_data["numPalettes"]
        self.num_patterns = json_data["numPatterns"]
        self.num_comments_made = json_data["numCommentsMade"]
        self.num_lovers = json_data["numLovers"]
        self.num_comments_on_profile = json_data["numCommentsOnProfile"]
        try:
            pass
        # implement comments section -> switch
        except:
            pass


class Stats(object):
    def __init__(self, json_data):
        self.total = json_data["total"]


class RGB(object):
    def __init__(self, rgb):
        self.red = rgb["red"]
        self.green = rgb["green"]
        self.blue = rgb["blue"]
        self.rgb = (self.red, self.green, self.blue)


class HSV(object):
    def __init__(self, hsv):
        self.hue = hsv["hue"]
        self.saturation = hsv["saturation"]
        self.value = hsv["value"]
        self.hsv = (self.hue, self.saturation, self.value)
