from invaders import *
from ui_elements import Text


waiting_for_button_text = Text(surface, text='PRESS "R" TO RESTART', font_size=16, color=(255, 255, 255))
waiting_for_button_text.center(int(width/2), int(heigth/2))

game_won_text = Text(surface, text='GAME WON! PRESS "R" TO RESTART', font_size=36, color=(255, 255, 255))
game_won_text.center(int(width/2), int(heigth/2))


def initiate_game():
	global main, game_over, waiting_for_restart, game_won, protector, enemyFleet

	main = True
	game_over = False
	waiting_for_restart = False
	game_won = False

	#to prevent shooting after pressing space or mousebutton1 to restart the game
	
	for bullet in bullets:
		del bullet
	bullets.clear()

	for barrier in barriers:
		del barrier
		barriers.clear()

	protector = Player()
	protector.Place(width/2, heigth-30)

	enemyFleet = EnemyFleet(48, row = 6)
	enemyFleet.CreateTheFleet() 
	enemyFleet.PlaceTheFleet()

	Barrier(30, heigth - 90, 6, 3).Place()
	Barrier(110, heigth - 90, 6, 3).Place()

	Barrier(width-150, heigth - 90, 6, 3).Place()
	Barrier(width-70, heigth - 90, 6, 3).Place()

initiate_game()

while(main):
	clock.tick(120)
	surface.fill((0,0,0))

	if waiting_for_restart:
		waiting_for_button_text.update()

	if game_won:
		game_won_text.update()

	events = pygame.event.get()
	for event in events:
		if(event.type == pygame.QUIT):
			main = False
		elif (event.type == pygame.KEYDOWN):
			if waiting_for_restart or game_won:
				if event.key == pygame.K_r:
					initiate_game()


	keys = pygame.key.get_pressed()
	if(pygame.mouse.get_pressed()[0] or keys[pygame.K_SPACE]):
		if not game_over and not game_won:
			protector.Shoot()


	for bullet in bullets:
		if(not game_over):
			bullet.Move()
		bullet.Show()

		if(bullet.y < 0 or bullet.y > heigth):
			bullets.remove(bullet)

		for ship in enemyFleet.ships:
			if(ship != None):
				if(Collide(ship, bullet)):
					ship.Explode()
					bullet.Explode()
					if enemyFleet.shipAmount == 0:
						game_won = True

		for barrier in barriers:
			for block in barrier.blocks:
				if(Collide(block, bullet)):
					block.Explode()
					bullet.Explode()
					break

		if(Collide(protector, bullet)):
			bullet.Explode()
			game_over = True
			waiting_for_restart = True

	for ship in enemyFleet.readyToFire:
		if(ship.x < protector.x+protector.w/2 < ship.x+ship.w):
			ship.Shoot()

	for barrier in barriers:
		barrier.Show()

	protector.Show()
	if(not game_over):
		enemyFleet.Move()
		enemyFleet.Shoot()

		if(keys[pygame.K_RIGHT] or keys[pygame.K_d]):
			protector.Move(1)
		if(keys[pygame.K_LEFT] or keys[pygame.K_a]):
			protector.Move(-1)
			
	enemyFleet.Show()

	pygame.display.update()

pygame.quit()