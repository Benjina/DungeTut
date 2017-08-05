#BenjLel
#dungeycrawly.py
#
#Following the tutorials at 
#	http://www.roguebasin.com/index.php?title=Roguelike_Tutorial,_using_python3%2Btdl
#

import tdl
import random

SCREEN_HEIGHT = 80
SCREEN_WIDTH = 50
MAX_MAP_HEIGHT = 60
MAX_MAP_WIDTH = 50
LIMIT_FPS = 20
playerx = random.randint(5, MAX_MAP_WIDTH - 5)		#Initialize player to random loc
playery = random.randint(5, MAX_MAP_HEIGHT - 5)		#	with a slight buffer.
color_dark_ground = (162, 82, 45)
color_dark_wall = (169, 169, 169)

class GameObject:
	#General game object to be inherited by more specific obj classes
	#	Always represented by a character on screen
	def __init__(self, xloc, yloc, char, color):
		self.x = xloc
		self.y = yloc
		self.char = char
		self.color = color

	def move(self, dx, dy):
		#Move by given amount
		if not cur_map[self.x + dx][self.y + dy].blocked:
			self.x += dx
			self.y += dy

	def setColor(self, newcolor):
		#Set color
		self.color = newcolor

	def draw(self):
		#Draw character reoresenting given object at given pos
		con.draw_char(self.x, self.y, self.char, self.color)

	def clear(self):
		#Clear character representing given object
		con.draw_char(self.x, self.y, ' ', bg=None)


class Tile:
	#Sets up the tiles we'll use to build the map
	#
	def __init__(self, blocked, blocked_sight=None, color=color_dark_wall):
		self.blocked = blocked
		#Generally if a tile is blocked it also blocks sight
		if blocked_sight is None: blocked_sight = blocked
		self.blocked_sight = blocked_sight
		self.color = color

	def setColor(self, color):
		#Sets color to input color value
		self.color = color

def make_map():
	#Makes a 2-D Array of Tiles for displaying the Map
	#
	global cur_map
	cur_map = [[Tile(False) for y in range(MAX_MAP_HEIGHT)] 
			for x in range(MAX_MAP_WIDTH)]

	#Map test
	cur_map[30][20].blocked = True
	cur_map[30][20].blocked_sight = True
	cur_map[31][20].blocked = True
	cur_map[31][20].blocked_sight = True
	cur_map[32][20].blocked = True
	cur_map[32][20].blocked_sight = True
	cur_map[33][20].blocked = True
	cur_map[33][20].blocked_sight = True
	cur_map[34][20].blocked = True
	cur_map[34][20].blocked_sight = True

	#Outline Map
	for y in range(MAX_MAP_HEIGHT):
		for x in range(MAX_MAP_WIDTH):
			if 0 in (x, y) or x == MAX_MAP_WIDTH - 1 or y == MAX_MAP_HEIGHT - 1:
				cur_map[x][y].blocked = True
				cur_map[x][y].blocked_sight = True

def roomGenerator():
	pass

def renderAll():
	#Draws all objects in list
	#
	for obj in objects:
		obj.draw()

	#Draw tiles
	for tilecol in range(MAX_MAP_HEIGHT):
		for tilerow in range(MAX_MAP_WIDTH):
			curtile = cur_map[tilerow][tilecol]
			if not curtile.blocked_sight:
				curtile.setColor(color_dark_ground)

			con.draw_char(tilerow, tilecol, None, fg=None, bg=curtile.color)

	root.blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)

def handle_keys():
	#Handles user keyboard input
	#
	global playerx, playery
	dx = 0
	dy = 0
	#user_input = tdl.event.key_wait()			Turn-based setting
	
	keypress = False							#Realtime settings
	for event in tdl.event.get():
		if event.type == 'KEYDOWN':
			user_input = event
			keypress = True
	if not keypress:
		return

	#Movement keys
	if user_input.key == 'UP':
		player.move(0, -1)
	elif user_input.key == 'DOWN':
		player.move(0, 1)
	elif user_input.key == 'LEFT':
		player.move(-1, 0)
	elif user_input.key == 'RIGHT':
		player.move(1, 0)
	elif user_input.key == 'ESCAPE':
		return True		#Exit game


######
# Main
######

tdl.set_font('celtic_garamond_10x10_gs_tc.png', greyscale=False, altLayout=True)
#Console variable
root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Dungey Crawley", fullscreen=False)
con = tdl.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
tdl.setFPS(LIMIT_FPS)							#Realtime (comment for turn-based)

player = GameObject(playerx, playery, '@', (255,255,255))
npc1 = GameObject(random.randint(5, MAX_MAP_WIDTH - 5),
	 			random.randint(5, MAX_MAP_HEIGHT - 5), 'X', (0,255,255))
objects = [player, npc1]

make_map()

# Loop action, fam
while not tdl.event.is_window_closed():
	#con.draw_char(playerx, playery, '@', bg=None, fg=(255,255,255))
	renderAll()
	tdl.flush()				#Presenting changes to screen (flushing the console)

	for obj in objects:			#Clears all existing objects
		obj.clear()

	exit_game = handle_keys()
	if exit_game:
		break
