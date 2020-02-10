from invaders import *

protector = Player()
protector.Place(width/2, heigth-30)

enemyFleet = EnemyFleet(48, row = 6)
enemyFleet.CreateTheFleet() 
enemyFleet.PlaceTheFleet()

Barrier(30, heigth - 90, 6, 3).Place()
Barrier(110, heigth - 90, 6, 3).Place()

Barrier(width-150, heigth - 90, 6, 3).Place()
Barrier(width-70, heigth - 90, 6, 3).Place()

main = True
gameOver = False
while(main):
	clock.tick(120)
	surface.fill((0,0,0))
	events = pygame.event.get()
	for event in events:
		if(event.type == pygame.QUIT):
			main = False
	keys = pygame.key.get_pressed()
	if(pygame.mouse.get_pressed()[0] or keys[pygame.K_SPACE] and not gameOver):
		protector.Shoot()

	for bullet in bullets:
		if(not gameOver):
			bullet.Move()
		bullet.Show()
		if(bullet.y < 0 or bullet.y > heigth):
			bullets.remove(bullet)
		for ship in enemyFleet.ships:
			if(ship != None):
				if(Collide(ship, bullet)):
					ship.Explode()
					bullet.Explode()
		for barrier in barriers:
			for block in barrier.blocks:
				if(Collide(block, bullet)):
					block.Explode()
					bullet.Explode()
					break
		if(Collide(protector, bullet)):
			bullet.Explode()
			gameOver = True

	for ship in enemyFleet.readyToFire:
		if(ship.x < protector.x+protector.w/2 < ship.x+ship.w):
			ship.Shoot()

	for barrier in barriers:
		barrier.Show()

	protector.Show()
	if(not gameOver):
		enemyFleet.Move()
		enemyFleet.Shoot()

		if(keys[pygame.K_RIGHT] or keys[pygame.K_d]):
			protector.Move(1)
		if(keys[pygame.K_LEFT] or keys[pygame.K_a]):
			protector.Move(-1)
			
	enemyFleet.Show()
	pygame.display.update()

pygame.quit()