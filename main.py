#TEST GAME

import pygame as pg

""" GAME CONSTANTS """
s = {'screen': {
	'dim': [400, 400],
	'title': 'Test Game'		
	}
}

""" IMPORTANT VARIABLES """
clk = pg.time.Clock()

""" MAIN LOOP """
def main():
	""" Main Program """
	pg.init()
	screen = pg.display.set_mode(s['screen']['dim'])
	pg.display.set_caption(s['screen']['title'])

	""" Main Loop """
	done = False
	while not done:
		
		#Event Checker
		for event in pg.event.get():
			#Check if quit has been pressed
			if pg.QUIT == event.type:
				done = True
		
		#End of Loop
		clk.tick(60)
		pg.display.flip()

	pg.quit()

if __name__ == "__main__":
	main()
