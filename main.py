#TEST GAME

import pygame as pg

""" GAME CONSTANTS """
s = {'screen': {
	'dim': [400, 400],
	'title': 'Test Game',	
	},
	'fps': 60
}

""" LEVEL SETTINGS """
l = {'platforms': [[200,10,100,100],[200,10,100,300]],
	'colors': [[0,0,0],[80,80,80],[160,160,160],[240,240,240]],
	'start': [s['screen']['dim'][0]/2, s['screen']['dim'][1]]
}

""" PLAYER SETTINGS """
p = {'size': [16,16],
	'hv_accel': 1,
	'hv_max': 8,
	'j_launch': 0,
	'j_boost': 1,
	'j_count': 10 
}

""" IMPORTANT VARIABLES """
v = {'clk': pg.time.Clock(),
	'done': False,
	'j_count': p['j_count']
}

""" USER INPUT """
uip = dict() #"tap" means pressed this frame, "hold" means key is down
uip["any"] = {"tap": False, "hold": False, "key": 0} #For any key input. Tap only.
uip["up"] = {"tap": False, "hold": False, "key": pg.K_UP}
uip["down"] = {"tap": False, "hold": False, "key": pg.K_DOWN}
uip["left"] = {"tap": False, "hold": False, "key": pg.K_LEFT}
uip["right"] = {"tap": False, "hold": False, "key": pg.K_RIGHT}
uip["a"] = {"tap": False, "hold": False, "key": pg.K_a}
uip["return"] = {"tap": False, "hold": False, "key": pg.K_RETURN}
uip["p"] = {"tap": False, "hold": False, "key": pg.K_p}

""" PLAYER CLASS """
class Player(pg.sprite.Sprite):

	def __init__(self):

		super(Player, self).__init__()
		self.image = pg.Surface(p['size'])
		self.image.fill(l['colors'][0])
		self.rect = self.image.get_rect()

		#Define Player Settings
		self.v = [0,0] #Velocity

	def update(self):

		#Gravity
		if self.v[1] == 0: self.v[1] = 1
		else: self.v[1] += 0.35

		#Apply Inputs - Jumping
		if uip['up']['tap']: self.v[1] = -p['j_launch']
		if uip['up']['hold'] and v['j_count'] > 0:
			self.v[1] -= p['j_boost']
			v['j_count'] -= 1
		elif not uip['up']['hold']: v['j_count'] = p['j_count']

		#Apply Inputs - Horizontal Movement
		if uip['left']['hold'] and self.v[0] > -p['hv_max']: self.v[0] -= p['hv_accel']
		if uip['right']['hold'] and self.v[0] < p['hv_max']: self.v[0] += p['hv_accel']
		if not (uip['left']['hold'] or uip['right']['hold']): self.v[0] = 0

		#Horizontal Movement and Collision Detection
		self.rect.x += self.v[0]
		hit_list = pg.sprite.spritecollide(self, self.level.platform_list, False)
		for block in hit_list:
			if self.v[0] > 0: self.rect.right = block.rect.left
			elif self.v[0] < 0: self.rect.left = block.rect.right

		#Horizontal Border Correction
		if self.rect.x < 0:
			self.rect.x = 0
		elif self.rect.x > s['screen']['dim'][0] - p['size'][1]:
			self.rect.x = s['screen']['dim'][0] - p['size'][1]

		#Vertical Movement and Collision Detection
		self.rect.y += self.v[1]
		hit_list = pg.sprite.spritecollide(self, self.level.platform_list, False)
		for block in hit_list:
			if self.v[1] > 0: self.rect.bottom = block.rect.top
			elif self.v[1] < 0: self.rect.top = block.rect.bottom
			self.v[1] = 0 #Stop vertical movement

		#Vertical Level Border Correction
		if self.rect.y >= s['screen']['dim'][1] - p['size'][0]:
			self.v[1]
			self.rect.y = s['screen']['dim'][1] - p['size'][0]

""" LEVEL CLASS """
class Level(object):
	#Generic super class for levels
	def __init__(self, player):
		self.platform_list = pg.sprite.Group()
		self.player = player

		for platform in l['platforms']:
			block = Platform([platform[0], platform[1]])
			block.rect.x = platform[2]
			block.rect.y = platform[3]
			block.player = self.player
			self.platform_list.add(block)

	def update(self):
		self.platform_list.update()

	def draw(self, screen):
		screen.fill(l['colors'][2])
		self.platform_list.draw(screen)

""" PLATFORM CLASS """
class Platform(pg.sprite.Sprite):
	
	def __init__(self, dim):
		super(Platform, self).__init__()
		
		self.image = pg.Surface(dim)
		self.image.fill(l['colors'][0])
		self.rect = self.image.get_rect()
		

""" MAIN LOOP """
def main():
	""" Main Program """
	pg.init()
	screen = pg.display.set_mode(s['screen']['dim'])
	pg.display.set_caption(s['screen']['title'])

	""" Load Levels & Player"""
	player = Player()
	level = Level(player)
	player.level = level
	active_sprite_list = pg.sprite.Group()
	active_sprite_list.add(player)
	
	player.rect.x = l['start'][0]
	player.rect.y = l['start'][1]

	""" Main Loop """
	while not v['done']:
		
		#Event Checker
		get_input()

		level.update()
		player.update()

		#Draw to Screen
		level.draw(screen)
		active_sprite_list.draw(screen)
		
		#End of Loop
		v['clk'].tick(s['fps'])
		pg.display.flip()

	pg.quit()

""" KEY INPUT """
def get_input():
	#Reset taps
	for button in uip:
		uip[button]['tap'] = False

	#Get all current inputs
	for event in pg.event.get():
		#If user quits
		if event.type == pg.QUIT:
			v['done'] = True

		#If keydown event
		if event.type == pg.KEYDOWN:
			uip['any']['tap'] = True
			for button in uip:
				if event.key == uip[button]['key']:
					uip[button]['tap'] = True
					uip[button]['hold'] = True
					break

		#If key release event
		if event.type == pg.KEYUP:
			for button in uip:
				if event.key == uip[button]['key']:
					uip[button]['hold'] = False
					break

if __name__ == "__main__":
	main()
