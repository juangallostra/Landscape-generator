# Landscape_generator
Python landscape generator using midpoint displacement.

To read an in depth explanation visit this [blog entry](https://bitesofcode.wordpress.com/2016/12/23/landscape-generation-using-midpoint-displacement/).

I am finally using the API provided by ColourLovers at http://www.colourlovers.com/api

## TODO
- Make a python wrapper for the colourlovers API (or similar) to get color palettes
 * It consists of two modules (**_Currently working on this_**):
    - ```colourlovers_wrapper.py``` is in charge of making requests to the the API and retrieving its responses. **It still doesn't handle all the possible request that are accepted by the API**. Lack of support for ~~searching with parametres _new_, _top_ and _random_ as well as~~ the _switches_ in Color and Lover searches.)
    - ```colourlovers_data_containers.py``` Implements ~~xml~~ json deserializing for the API responses. (~~if finally using colourlovers API~~) It presents the data returned by the API request as class instances of the specified search type (Colors, Palettes, Patterns, Lovers or Stats). The attributes that this classes have are the data fields returned by the API for that concrete search type (**Work in progress**).

 
- ~~Organise and comment the code in ```landscape_generator.py``` file so it is more clear~~
- Let the user play with the parametres of the landscape
- Command line arguments / GUI
- Documentation
- It would be nice to have a tool to preview and organize the selected colors (The obtained classes from the search now implement a method, ```draw()```, which draws the Pattern, Color or Palette it is called on)


## Possible sources for color palettes
1. http://www.colr.org/api.html - (http://www.colr.org/)
2. http://www.colourlovers.com/api - (http://www.colourlovers.com/)
3. http://www.pictaculous.com/api/ - (http://www.pictaculous.com/)
4. It is also worth mentioning https://github.com/elbaschid/python-colourlovers
5. Another approach would be to __locally generate__ the color palettes (Read some theory). 


