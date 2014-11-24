import libtcodpy as libtcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 45

LIMIT_FPS = 20

color_dark_wall = libtcod.Color(0,0,100)
color_dark_ground = libtcod.Color(50,50,150)
color_light_ground= libtcod.Color(150,50,50)
color_light_wall= libtcod.Color(50,50,50)

		

class Tile:
	def __init__(self, blocked, block_sight = None):
		self.blocked = blocked
		
		if block_sight is None: block_sight = blocked
		self.block_sight = block_sight
		
class Rect:
	def __init__(self, x, y, w, h,):
		self.x1 = x
		self.y1 = y
		self.x2 = x + w
		self.y2 = y + h
		
class Object:

	def __init__(self, x, y, char, color):
		self.x = x
		self.y = y
		self.char = char
		self.color = color
		
	def move(self, dx, dy):
		"""move a given ammount"""
		if not map[self.x + dx][self.y + dy].blocked:
			self.x += dx
			self.y += dy
		
	def draw(self):
		libtcod.console_set_default_foreground(con, self.color)
		libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)
		
	def clear (self):
		libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

def create_room(room):
	global map
	for x in range(room.x1 + 1, room.x2):
		for y in range (room.y1 + 1, room.y2):
			map[x][y].blocked = False
			map[x][y].blocked_sight = False 

def create_h_tunnel(x1, x2, y):
	global map
	for x in range(min(x1, x2), max (x1, x2)+1):
		map[x][y].blocked = False
		map[x][y].blocked_sight = False

def create_v_tunnel(y1, y2, x):
	global map
	for x in range(min(y1, y2), max (y1, y2)+1):
		map [x][y].blocked = False
		map [x][y].blocked_sight = False
		
def make_map():
	global map
	
	map = [[ Tile(True)
		for y in range(MAP_HEIGHT)]
			for x in range (MAP_WIDTH)]
		
	room1= Rect(20,15,10,15)
	room2= Rect(50,15,10,15)
	create_room(room1)
	create_room(room2)
	create_h_tunnel(25,55,23)
	player.x = 25
	player.y = 23
		
def render_all():
	global color_dark_wall, color_light_wall
	global color_dark_ground, color_light_ground
	
	for y in range(MAP_HEIGHT):
		for x in range (MAP_WIDTH):
			wall = map[x][y].block_sight
			if wall:
				libtcod.console_set_char_background(con, x, y, color_dark_wall, libtcod.BKGND_SET )
			else:
				libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET )
	
	for object in objects:
		object.draw()
		
	libtcod.console_blit(con, 0,0, SCREEN_WIDTH, SCREEN_HEIGHT, 0,0,0)
	
def handle_keys():
	
	key = libtcod.console_wait_for_keypress(True)
	
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		"""alt+ent toggle fullscreen"""
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
		
	elif key.vk == libtcod.KEY_ESCAPE:
		return True

	if libtcod.console_is_key_pressed(libtcod.KEY_UP):
		player.move(0,-1)
			
	elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
		player.move(0,1)
			
	elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
		player.move(-1,0)
			
	elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
		player.move(1,0)


	

""" use custom font """
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

"""initialize window"""
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
"""limit fps"""
libtcod.sys_set_fps(LIMIT_FPS)
"""Off Screen console"""
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

"""player and npc position"""
player = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@',libtcod.white)
npc = Object(SCREEN_WIDTH/2-5,SCREEN_HEIGHT/2, '@',libtcod.yellow)
objects = [npc, player]
make_map()
"""main loop """		
while not libtcod.console_is_window_closed():

	render_all()

	"""flush"""
	libtcod.console_flush()
	"""no trails"""
	for Object in objects:
		Object.clear()
	

	
	""" handle exit if needed"""
	exit = handle_keys()
	if exit:
		break
	




