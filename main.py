#TEST GAME

import pygame as pg

""" GAME SETTINGS """
#Master Settings Variable
s = {}

#Display Settings
s['d'] = {}
s['d']['scr'] = {'dim': [400, 400], 'title': 'Test Game'} #Screen
s['d']['fps'] = 60 #Frames Per Second

#Player Settings
s['p'] = {}
s['p']['d']  = {'size': [16,16]} #Display
s['p']['hm'] = {'accel': 1, 'max': 8} #Horizontal Movement
s['p']['vm'] = {'gravity': 0.35, 'max': 10} #Vertical Movement
s['p']['j']  = {'launch': 0, 'boost': 1, 'boost_count': 10} #Jumping Mechanics

#Game Variables
s['g'] = {}
s['g']['clk'] = pg.time.Clock()
s['g']['level_complete'] = False
s['g']['done'] = False
s['g']['screen'] = pg.display.set_mode(s['d']['scr']['dim'])

#Level Settings
s['l'] = list()
s['l'].append({'platforms': [[200,10,100,100],[200,10,100,200],[200,10,100,300]],
	'colors': [[0,0,0],[80,80,80],[160,160,160],[240,240,240]],
	'start': [200,384]
})
s['l'].append({'platforms': [[200,10,100,100],[200,10,100,200],[200,10,100,300]],
	'colors': [[0,255,0],[80,80,80],[160,160,160],[240,0,240]],
	'start': [200,384]
})
s['l'].append({'platforms': [[200,10,100,100],[200,10,100,200],[200,10,100,300]],
	'colors': [[0,0,255],[80,80,80],[160,160,160],[0,240,240]],
	'start': [200,384]
})

""" USER INPUT """
uip = dict() #"tap" means pressed this frame, "hold" means key is down
uip["any"] = {"tap": False, "hold": False, "key": 0} #For any key input. Tap only.
uip["up"] = {"tap": False, "hold": False, "key": pg.K_UP} #Jump
uip["left"] = {"tap": False, "hold": False, "key": pg.K_LEFT} #Move left
uip["right"] = {"tap": False, "hold": False, "key": pg.K_RIGHT} #Move right
uip["reset"] = {"tap": False, "hold": False, "key": pg.K_r} #Reset level 
uip["next"] = {"tap": False, "hold": False, "key": pg.K_n} #Skip level
uip["q"] = {"tap": False, "hold": False, "key": pg.K_q} #Quit game

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
			block = Platform(p, l)
			self.platform_list.add(block)

	def update(self):
		self.platform_list.update()

	def draw(self):
		s['g']['screen'].fill(self.s['colors'][2]) #Add background colour first
		self.platform_list.draw(s['g']['screen']) #Populate with platforms

""" PLATFORM CLASS """
class Platform(pg.sprite.Sprite):
	
	def __init__(self, p, l):
		super(Platform, self).__init__()
		#Basic Platform Setup
		self.image = pg.Surface([p[0],p[1]]) #Dimensions of Platform
		self.rect = self.image.get_rect()
		self.rect.x = p[2]; self.rect.y = p[3] #Position
		self.image.fill(l['colors'][0]) #Colour from level colour scheme
		

""" MAIN LOOP """
def main():
	#Setup
	pg.init()
	screen = pg.display.set_mode(s['d']['scr']['dim'])
	pg.display.set_caption(s['d']['scr']['title'])

	#Go through levels
	for l in s['l']:
		#If game done, exit loop and end game
		if s['g']['done']: break		
	
		#Set up the next level
		s['g']['level_complete'] = False
		player = Player(l)
		level = Level(l)
		player.level = level
		active_sprite_list = pg.sprite.Group()
		active_sprite_list.add(player)
	
		#Main Game Loop
		while not s['g']['level_complete']:	
			#Event Checker
			get_input()
			if uip['q']['tap']: s['g']['done'] = True; break

			level.update()
			player.update()

			#Draw to Screen
			level.draw()
			active_sprite_list.draw(s['g']['screen'])
		
			#End of Loop
			s['g']['clk'].tick(s['d']['fps'])
			pg.display.flip()

			if uip['next']['tap']: s['g']['level_complete'] = True

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
