#TEST GAME

import pygame as pg

""" GAME CONSTANTS """
s = {'screen': {
	'dim': [400, 400],
	'title': 'Test Game'		
	}
}

""" IMPORTANT VARIABLES """
v = {'clk': pg.time.Clock(),
	'done': False
}

""" LEVEL CLASS """
class Level(object):
	#Generic super class for levels
	def __init__(self):
		self.background = None


""" MAIN LOOP """
def main():
	""" Main Program """
	pg.init()
	screen = pg.display.set_mode(s['screen']['dim'])
	pg.display.set_caption(s['screen']['title'])

	""" Main Loop """
	while not v['done']:
		
		#Event Checker
		get_input(v)
		
		#End of Loop
		v['clk'].tick(60)
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
