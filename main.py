#TEST GAME

import pygame as pg
pg.font.init() #Initialise font module

""" GAME SETTINGS """
#Master Settings Variable
s = {}

#Display Settings
s['d'] = {}
s['d']['scr'] = {'dim': [400, 400], 'title': 'Test Game'} #Main Game Screen
s['d']['fps'] = 60 #Frames Per Second
s['d']['font'] = pg.font.SysFont('Comic Sans MS', 30)

#Player Settings
s['p'] = {}
s['p']['d']  = {'size': [16,16]} #Display
s['p']['hm'] = {'accel': 1, 'max': 8} #Horizontal Movement
s['p']['vm'] = {'gravity': 0.35, 'max': 8} #Vertical Movement
s['p']['j']  = {'launch': 0, 'boost': 1, 'boost_count': 10} #Jumping Mechanics
s['p']['death'] = {'flash': 3, 'lim': 30} #Flash every X for Y frames when dead

#Game Variables
s['g'] = {}
s['g']['clk'] = pg.time.Clock()
s['g']['frame_no'] = 0
s['g']['game_time'] = 60
s['g']['level_current'] = 0
s['g']['level_complete'] = False
s['g']['pause'] = False
s['g']['done'] = False
s['g']['screen'] = pg.display.set_mode(s['d']['scr']['dim'])
s['g']['alive'] = True
s['g']['death_frame'] = 0 #Blink on and off every X frames when dead
s['g']['draw_player'] = True

#Level Settings
s['l'] = list()
s['l'].append({'platforms': [[200,10,100,100],[200,10,100,200],[200,10,100,300]],
	'hazards': [[100,5,150,150],[100,5,150,250]],
	'exits': [[20,40,200,60]],
	'shift': {'vert': True, 'hor': True},
	'colors': [[0,0,0],[80,80,80],[160,160,160],[240,240,240]],
	'start': [200,384]
})
s['l'].append({'platforms': [[200,10,100,100],[200,10,100,200],[200,10,100,300]],
	'hazards': list(),
	'exits': [[20,40,200,60]],
	'shift': {'vert': True, 'hor': True},
	'colors': [[0,0,0],[80,80,80],[160,160,160],[240,240,240]],
	'start': [200,384]
})
s['l'].append({'platforms': [[200,10,100,100],[200,10,100,200],[200,10,100,300]],
	'hazards': list(),
	'exits': [[20,40,200,60]],
	'shift': {'vert': True, 'hor': True},
	'colors': [[0,0,0],[80,80,80],[160,160,160],[240,240,240]],
	'start': [200,384]
})

#User Input Keys
uip = dict() #"tap" means pressed this frame, "hold" means key is down
uip["any"] = {"tap": False, "hold": False, "key": 0} #For any key input. Tap only.
uip["up"] = {"tap": False, "hold": False, "key": pg.K_UP} #Jump
uip["left"] = {"tap": False, "hold": False, "key": pg.K_LEFT} #Move left
uip["right"] = {"tap": False, "hold": False, "key": pg.K_RIGHT} #Move right
uip["reset"] = {"tap": False, "hold": False, "key": pg.K_r} #Reset level 
uip["next"] = {"tap": False, "hold": False, "key": pg.K_n} #Skip level
uip["pause"] = {"tap": False, "hold": False, "key": pg.K_p} #Pause game
uip["quit"] = {"tap": False, "hold": False, "key": pg.K_q} #Quit game
uip["kill"] = {"tap": False, "hold": False, "key": pg.K_k} #Quit game

""" STATUS BAR """
class Status():

	def __init__(self, l):
		self.col = l['colors'][0]
		self.font = s['d']['font']
		#Time:
		self.time = self.font.render('TIME: %i' % s['g']['game_time'], False, self.col)

	def update(self):
		if s['g']['frame_no'] == 0: #If a new second has passed
			self.time = self.font.render('TIME: %i' % s['g']['game_time'], False, self.col)

	def draw(self):
		s['g']['screen'].blit(self.time, (0,0))

""" PLAYER CLASS """
class Player(pg.sprite.Sprite):

	def __init__(self, l):
		#Player Setup
		super(Player, self).__init__()
		self.image = pg.Surface(s['p']['d']['size'])
		self.rect = self.image.get_rect()

		#Define General Settings
		self.v = [0,0] #Velocity
		self.j = {'boost_count': 0, 'on_ground': True}

		#Define Level Specific Settings
		self.rect.x = l['start'][0]; self.rect.y = l['start'][1]
		self.image.fill(l['colors'][0])

	def update(self):
		#Gravity
		if self.v[1] == 0: self.v[1] = 1
		else: self.v[1] += s['p']['vm']['gravity']

		#Apply Inputs - Jumping
		if uip['up']['tap'] and self.j['on_ground']: #Launch player if tap and not already airborne
			self.v[1] = -s['p']['j']['launch']
			self.j['boost_count'] = s['p']['j']['boost_count']
			
		if uip['up']['hold'] and self.j['boost_count'] > 0: #Holding key gives additional boost
			self.v[1] -= s['p']['j']['boost']
			self.j['boost_count'] -= 1

		if not uip['up']['hold']: #Releasing jump button cancels any further boosts
			self.j['boost_count'] = 0

		#Apply Inputs - Horizontal Movement
		if uip['left']['hold'] and self.v[0] > -s['p']['hm']['max']: #Move left up to max speed
			self.v[0] -= s['p']['hm']['accel']
		if uip['right']['hold'] and self.v[0] < s['p']['hm']['max']: #Move right up to max speed
			self.v[0] += s['p']['hm']['accel']
		if not (uip['left']['hold'] or uip['right']['hold']): self.v[0] = 0 #Stop if not doing anything

		#Horizontal Movement and Collision Detection
		self.rect.x += self.v[0]
		hit_list = pg.sprite.spritecollide(self, self.level.platform_list, False)
		for block in hit_list: #Go through things which have been hit and readjust sprite position
			if self.v[0] > 0: self.rect.right = block.rect.left
			elif self.v[0] < 0: self.rect.left = block.rect.right
			self.v[0] = 0 #Stop moving upon collision

		#Horizontal Border Correction
		if self.rect.x < 0: self.rect.x = 0; self.v[0] = 0
		elif self.rect.x > s['d']['scr']['dim'][0] - s['p']['d']['size'][0]:
			self.v[0] = 0
			self.rect.x = s['d']['scr']['dim'][0] - s['p']['d']['size'][0]

		#Vertical Movement and Collision Detection
		self.rect.y += self.v[1]
		hit_list = pg.sprite.spritecollide(self, self.level.platform_list, False)
		for block in hit_list:
			if self.v[1] > 0: self.rect.bottom = block.rect.top
			elif self.v[1] < 0: self.rect.top = block.rect.bottom
			self.v[1] = 0 #Stop vertical movement

		#Vertical Level Border Correction
		if self.rect.y < 0: self.rect.y = 0; self.v[1] = 0
		elif self.rect.y >= s['d']['scr']['dim'][1] - s['p']['d']['size'][1]:
			self.v[1] = 0
			self.rect.y = s['d']['scr']['dim'][1] - s['p']['d']['size'][1]

		#Hazard Collision
		hit_list = pg.sprite.spritecollide(self, self.level.hazard_list, False)
		if hit_list: s['g']['alive'] = False

		#Exit Collision
		hit_list = pg.sprite.spritecollide(self, self.level.exit_list, False)
		if hit_list: s['g']['level_complete'] = True

		#Check If On Ground
		if self.rect.y == s['d']['scr']['dim'][1] - s['p']['d']['size'][1]: #If on bottom of screen
			self.j['on_ground'] = True
		else: #Check if any platforms. If not then not on ground
			self.rect.y += 2; hit_list = pg.sprite.spritecollide(self, self.level.platform_list, False); self.rect.y -= 2
			if len(hit_list) != 0: self.j['on_ground'] = True
			else: self.j['on_ground'] = False

""" LEVEL CLASS """
class Level(object):
	#Generic super class for levels
	def __init__(self, l):
		#Save configuration settings
		self.s = {}
		self.s['colors'] = l['colors']	

		#Add Platforms
		self.platform_list = pg.sprite.Group()
		for p in l['platforms']: #Create each platform and add to level
			platform = Block(p, l['colors'][0])
			self.platform_list.add(platform)

		#Add Hazards
		self.hazard_list = pg.sprite.Group()
		for h in l['hazards']: #Create each hazard and add to level
			hazard = Block(h, l['colors'][3])
			self.hazard_list.add(hazard)

		#Add Exit(s)
		self.exit_list = pg.sprite.Group()
		for e in l['exits']:
			exit = Block(e, l['colors'][0])
			self.exit_list.add(exit)

	def update(self):
		pass
		#self.platform_list.update()
		#self.hazard_list.update()

	def draw(self):
		s['g']['screen'].fill(self.s['colors'][2]) #Add background colour first
		self.platform_list.draw(s['g']['screen']) #Populate with platforms
		self.hazard_list.draw(s['g']['screen']) #Populate with platforms
		self.exit_list.draw(s['g']['screen'])

""" BLOCK CLASS """
class Block(pg.sprite.Sprite):	
	#Basic Platform Setup
	def __init__(self, p, c):
		super(Block, self).__init__()
		self.image = pg.Surface([p[0],p[1]]) #Dimensions of Platform
		self.rect = self.image.get_rect()
		self.rect.x = p[2]; self.rect.y = p[3] #Position
		self.image.fill(c) #Colour from level colour scheme		

""" MAIN LOOP """
def main():
	#Setup
	pg.init()
	screen = pg.display.set_mode(s['d']['scr']['dim'])
	pg.display.set_caption(s['d']['scr']['title'])

	#Go through levels
	while not s['g']['done']:	
		#Set up the next level
		s['g']['level_complete'] = False
		player = Player(s['l'][s['g']['level_current']])
		level = Level(s['l'][s['g']['level_current']])
		player.level = level

		#Reset some game variables
		s['g']['death_frame'] = 0
		s['g']['draw_player'] = True
		s['g']['alive'] = True

		status = Status(s['l'][s['g']['level_current']])
		active_sprite_list = pg.sprite.Group()
		active_sprite_list.add(player)
	
		#Main Game Loop
		while not s['g']['level_complete']:
			#Get and apply user input
			get_input()
			if uip['pause']['tap']: s['g']['pause'] = not s['g']['pause']

			if not s['g']['pause']:
				#Get non-pause inputs
				if uip['kill']['tap']: s['g']['alive'] = False
				if uip['reset']['tap']: break
				if s['g']['death_frame'] > s['p']['death']['lim']: break

				#Frame & Time Counter
				s['g']['frame_no'] = (s['g']['frame_no'] + 1) % s['d']['fps'] #Increase and reset at fps
				if s['g']['frame_no'] == 0: s['g']['game_time'] -= 1 #Increment time counter per second

				#Update all Sprites, Player, etc.
				level.update()
				if s['g']['alive']: player.update()
				status.update()

				#Check what to draw to screen
				if s['g']['alive']: s['g']['draw_player'] = True #If alive, draw.
				else: #If dead, flash every X frames.
					if s['g']['death_frame'] <= s['p']['death']['lim']: s['g']['death_frame'] += 1 
					s['g']['draw_player'] = (s['g']['death_frame'] / s['p']['death']['flash']) % 2 == 1

				#Draw to Screen
				level.draw() #First draw level items
				if s['g']['draw_player']: active_sprite_list.draw(s['g']['screen']) #Then draw players / entities
				status.draw()
		
			#Display Things
			s['g']['clk'].tick(s['d']['fps'])
			pg.display.flip()

			#Level Complete Check
			if uip['next']['tap']: 
				s['g']['level_complete'] = True

			if s['g']['level_complete']: s['g']['level_current'] += 1

			#Check if end of game reached
			if s['g']['done'] or s['g']['level_current'] >= len(s['l']) or uip['quit']['tap'] or s['g']['game_time'] == 0:
				s['g']['done'] = True
				break

	#End game here
	pg.quit()

""" GET KEY INPUT """
def get_input():
	#Reset taps
	for button in uip:
		uip[button]['tap'] = False

	#Get all current inputs
	for event in pg.event.get():
		#If user quits
		if event.type == pg.QUIT:
			s['g']['done'] = True

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
