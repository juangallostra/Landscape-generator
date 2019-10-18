# Landscape-generator

Python landscape generator using midpoint displacement.

To read an in depth explanation visit this [blog entry](https://bitesofcode.wordpress.com/2016/12/23/landscape-generation-using-midpoint-displacement/).

## Usage

1. Clone this repository: `$ git clone https://github.com/juangallostra/Landscape-generator.git`
2. Install dependencies (it is recommended to do so in a virtual environment): `$ pip install -r requirements.txt`
3. Execute the script: `$ python landscape_generator.py` or, alternatively and to change the color palette, `$ python landscape_generator -t [THEME]` where `[THEME]` is a word indicating the desired color theme (`river`, `mountain`, `sun`, `moon`, etc.)

## TO DO

- Let the user play with the parametres of the landscape
- Command line arguments / GUI
- ~~Documentation~~ See the blog post linked above and comments in the code.
- It would be nice to have a tool to preview and organize the selected colors (The obtained classes from the search now implement a method, ```draw()```, which draws the Pattern, Color or Palette it is called on)
