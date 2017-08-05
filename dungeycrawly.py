#BenjLel
#dungeycrawly.py
#
#Following the tutorials at 
#	http://www.roguebasin.com/index.php?title=Roguelike_Tutorial,_using_python3%2Btdl
#
#
#		Current State:
#
#	Recursive rooms work, need to pad with some space, add corridors/doorways
#
#	As of now (still testing) X char should be only one with chance of spawning
#		in a wall space. Others should correct before placing.
#
#
#	Needs:
#	
#		Movement for NPCs
#		Health properties and visuals
#		Items, Weapons, Chests, Loot
#		Weapons and functionality
#		Char inventory/equip properties
#		Gui
#		
#
#	Ideas:
#
#		Add pickaxe and change some walls to breakable.
#

import tdl
import random

SCREEN_HEIGHT = 80
SCREEN_WIDTH = 80
MAX_MAP_HEIGHT = 60
MAX_MAP_WIDTH = 80
LIMIT_FPS = 20
#playerx = random.randint(5, MAX_MAP_WIDTH - 5)		#Initialize player to random loc
#playery = random.randint(5, MAX_MAP_HEIGHT - 5)		#	with a slight buffer.
playerx = 0
playery = 0
color_dark_ground = (162, 82, 45)
color_dark_wall = (169, 169, 169)


###############################################
#		Primary Components
###############################################

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


class CharObject(GameObject):
	#Slightly more specific object, inherits from GameObj and initializes
	#	values to anticipate movement (not randomly located on a wall etc.)
	def __init__(self, char, color):
		xloc = random.randint(5, MAX_MAP_WIDTH - 5)
		yloc = random.randint(5, MAX_MAP_HEIGHT - 5)
		while cur_map[xloc][yloc].blocked_sight:
			xloc = random.randint(5, MAX_MAP_WIDTH - 5)
			yloc = random.randint(5, MAX_MAP_HEIGHT - 5)
		super().__init__(xloc, yloc, char, color)

class Tile:
	#Sets up the tiles we'll use to build the map
	#
	def __init__(self, blocked, blocked_sight=None, color=color_dark_ground):
		self.blocked = blocked
		#Generally if a tile is blocked it also blocks sight
		if blocked_sight is None: blocked_sight = blocked
		self.blocked_sight = blocked_sight
		self.color = color

	def setColor(self, color):
		#Sets color to input color value
		self.color = color


###############################################
#		Primary Functionalities
###############################################

def make_map():
	#Makes a 2-D Array of Tiles for displaying the Map
	#
	global cur_map
	cur_map = [[Tile(False) for y in range(MAX_MAP_HEIGHT)] 
			for x in range(MAX_MAP_WIDTH)]

	#Outline Map
	for y in range(MAX_MAP_HEIGHT):
		for x in range(MAX_MAP_WIDTH):
			if 0 in (x, y) or x == MAX_MAP_WIDTH - 1 or y == MAX_MAP_HEIGHT - 1:
				cur_map[x][y].blocked = True
				cur_map[x][y].blocked_sight = True
			if cur_map[x][y].blocked_sight:
				cur_map[x][y].setColor(color_dark_wall)

intercol = (100, 100, 100)
#First take at recursive room generator.
def roomGenerator(inmap):

	print("len(inmap) - 10: {}  ------ len(inmap[0] - 10: {}".format(len(inmap)-10, len(inmap[0])-10))

	if len(inmap) * len(inmap[0]) < 30:						#Base case 1
		return
	if len(inmap) - 5 <= 20:
		return
	if len(inmap[0]) - 5 <= 20:
		return

	xinter = random.randint(5, len(inmap) - 5)
	yinter = random.randint(5, len(inmap[0]) - 5)
	newcol = [ x + 10 for x in intercol ]
	divcol = (255, 255, 0)
	for x in range(len(inmap)):
		for y in range(len(inmap[x])):
			tile = inmap[x][y]
			if x == xinter:
				tile.blocked = True
				tile.blocked_sight = True

			if y == yinter:
				tile.blocked = True
				tile.blocked_sight = True

	cellA = [[inmap[x][y] for x in range(xinter)]		#Attempt to fill cells
			for y in range(yinter)]						#Holy shit this worked
	cellB = [[inmap[x][y] for x in range(xinter + 1, len(inmap))]
			for y in range(yinter)]
	cellC = [[inmap[x][y] for x in range(xinter + 1, len(inmap))]
			for y in range(yinter + 1, len(inmap[0]))]
	cellD = [[inmap[x][y] for x in range(xinter)]
			for y in range(yinter + 1, len(inmap[0]))]

	cells = [cellA, cellB, cellC, cellD]

	# aColor = (15, 15, 15)
	# bColor = (65, 65, 65)
	# cColor = (115, 115, 115)
	# dColor = (165, 165, 165)

	# for x in range(len(cellA)):
	# 	for y in range(len(cellA[x])):
	# 		cellA[x][y].setColor(aColor)		Cell test code
	# for x in range(len(cellB)):
	# 	for y in range(len(cellB[x])):
	# 		cellB[x][y].setColor(bColor)
	# for x in range(len(cellC)):
	# 	for y in range(len(cellC[x])):
	# 		cellC[x][y].setColor(cColor)
	# for x in range(len(cellD)):
	# 	for y in range(len(cellD[x])):
	# 		cellD[x][y].setColor(dColor)

	for cell in cells: roomGenerator(cell)




def renderAll():
	#Draws all objects in list
	#
	for obj in objects:
		obj.draw()

	#Draw tiles
	for tilecol in range(MAX_MAP_HEIGHT):
		for tilerow in range(MAX_MAP_WIDTH):
			curtile = cur_map[tilerow][tilecol]
			if curtile.blocked_sight:
				curtile.setColor(color_dark_wall)
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
	elif user_input.key == 'ENTER':
		print(player.x, player.y)


###############################################
# Main
###############################################

tdl.set_font('celtic_garamond_10x10_gs_tc.png', greyscale=False, altLayout=True)
#Console variable
root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Dungey Crawley", fullscreen=False)
con = tdl.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
tdl.setFPS(LIMIT_FPS)							#Realtime (comment for turn-based)

make_map()


#Testing roomGen
roomGenerator(cur_map)

#Generate Objects
while cur_map[playerx][playery].blocked_sight:
	playerx = random.randint(5, MAX_MAP_WIDTH - 5)
	playery = random.randint(5, MAX_MAP_HEIGHT - 5)

#player = GameObject(playerx, playery, '@', (255,255,255))
npc1 = GameObject(random.randint(5, MAX_MAP_WIDTH - 5),
	 			random.randint(5, MAX_MAP_HEIGHT - 5), 'X', (0,255,255))
player = CharObject('@', (255,255,255))
npc2 = CharObject('O', (45, 200, 0))
objects = [player, npc1, npc2]

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
