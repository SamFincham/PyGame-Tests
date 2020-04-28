#TEST GAME

import pygame as pg

""" GAME CONSTANTS """
s = {'screen': {
	'dim': [400, 400],
	'title': 'Test Game'		
	}
}

""" LEVEL SETTINGS """
l = {'platforms': [[],[],[],[]],
	'colors': [[0,0,0],[80,80,80],[160,160,160],[240,240,240]]
}

""" PLAYER SETTINGS """
p = {'size': [16,16]}

""" IMPORTANT VARIABLES """
v = {'clk': pg.time.Clock(),
	'done': False,
	'fps': 30
}

""" PLAYER CLASS """
class Player(pg.sprite.Sprite):

	def __init__(self):

		super(Player, self).__init__()
		self.image = pg.Surface(p['size'])
		self.image.fill(l['colors'][0])
		self.rect = self.image.get_rect()

""" LEVEL CLASS """
class Level(object):
	#Generic super class for levels
	def __init__(self, player):
		self.platform_list = pg.sprite.Group()
		self.player = player

	def update(self):
		self.platform_list.update()

	def draw(self, screen):
		screen.fill(l['colors'][2])
		self.platform_list.draw(screen)

""" PLATFORM CLASS """
class Platform(pg.sprite.Sprite):
	
	def __init__(self):
		super(Platform, self).__init__()
		
		self.image = pg.Surface()

""" MAIN LOOP """
def main():
	""" Main Program """
	pg.init()
	screen = pg.display.set_mode(s['screen']['dim'])
	pg.display.set_caption(s['screen']['title'])

	""" Load Levels """
	l1 = Level(l)

	""" Main Loop """
	while not v['done']:
		
		#Event Checker
		get_input(v)

		l1.update()
		l1.draw(screen)
		
		#End of Loop
		v['clk'].tick(v['fps'])
		pg.display.flip()

	pg.quit()

""" KEY INPUT """
def get_input(v):
	for event in pg.event.get():
		if event.type == pg.QUIT:
			v['done'] = True

		if event.type == pg.KEYDOWN:
			if event.key == pg.K_LEFT:
				pass
			if event.key == pg.K_RIGHT:
				pass
			if event.key == pg.K_UP:
				pass

		if event.type == pg.KEYUP:
			if event.key == pg.K_LEFT:
				pass
			if event.key == pg.K_RIGHT:
				pass
			if event.key == pg.K_UP:
				pass			 

if __name__ == "__main__":
	main()
