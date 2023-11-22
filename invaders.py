import pygame, time, random
from PIL import Image
from glob import glob
from sys import platform

if platform == "linux" or platform == "linux2":
    PATH_SEPERATOR = "/"
elif platform == "win32":
    PATH_SEPERATOR = "//"
else: # not supported
    raise Exception("FATAL: operating System is not supported!")


pygame.init()
width = 350
heigth = 340
surface = pygame.display.set_mode((width, heigth))
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()

bullets = []
barriers = []

pilImage = Image.open('Assets/Ship.png')
pilImage = pilImage.resize( ( int(pilImage.size[0]/2.7)  ,  int(pilImage.size[1]/2.7) ) )
shipSize = pilImage.size
shipImage = pygame.image.fromstring(pilImage.tobytes(), pilImage.size, pilImage.mode)

invaderImages = {}

for filename in glob('./Assets/Invaders/*.png'):
	pilImage = Image.open(filename)
	pilImage = pilImage.resize( ( int(pilImage.size[0]/2.7)  ,  int(pilImage.size[1]/2.7) ) )
	pyImage = pygame.image.fromstring(pilImage.tobytes(), pilImage.size, pilImage.mode)
	invaderImages[pyImage] = pilImage.size

sounds = {}

for filename in glob('./Assets/Sounds/*.wav'):
	sound = pygame.mixer.Sound(filename)
	sound.set_volume(0.2)
	print(filename)
	sounds[filename.split(PATH_SEPERATOR)[-1].split('.')[0]] = sound


def Collide(object1, bullet):
	return (object1.x <= bullet.x <= object1.x + object1.w and object1.y <= bullet.y <= object1.y + object1.h)

class Player():
	def __init__(self):
		self.image = shipImage
		self.x = 0
		self.y = 0
		self.w = shipSize[0]
		self.h = shipSize[1]
		self.velocity = 1
		self.hp = 100
		self.rateOfFire = 800
		self.lastShoot = 0

	def Place(self, x_, y_):
		self.x = x_
		self.y = y_

	def Move(self, direction):
		newPosX = self.x + self.velocity * direction
		if(newPosX >= 0 + self.w/2 and newPosX <= width - self.w* 1.5):
			self.x = newPosX

	def Shoot(self):
		if((time.time() - self.lastShoot)*1000 > self.rateOfFire):
			sounds['shoot'].play()
			newBullet = Bullet(self.x + self.w/2, self.y, -1, 2.3)
			bullets.append(newBullet)
			self.lastShoot = time.time()

	def Show(self):
		surface.blit(self.image, (self.x, self.y))
		#pygame.draw.rect(surface, (255,255,0), (self.x, self.y, self.w, self.h))

class Bullet():
	def __init__(self, x, y, direction, vel):
		self.x = x
		self.y = y
		self.velocity = vel
		self.direction = direction

	def Move(self):
		self.y += self.velocity*self.direction

	def Explode(self):
		bullets.remove(self)

	def Show(self):
		pygame.draw.line(surface, (255,0,0), (self.x, self.y), (self.x, self.y + 8*self.direction), 2)


class Enemy():
	def __init__(self, fleet, imageNum):
		self.image = [list(invaderImages.keys())[imageNum], list(invaderImages.keys())[imageNum+1]]
		self.stage = 0
		self.fleet = fleet
		self.x = 90
		self.y = 0
		self.w = list(invaderImages.values())[1][0]
		self.h = list(invaderImages.values())[1][1]
		self.hp = 50
		self.rateOfFire = 4000
		self.lastShoot = 0

	def ChangeStage(self):
		self.stage += 1
		if(self.stage == 2):
			self.stage = 0

	def Shoot(self):
		if((time.time() - self.lastShoot)*1000 > self.rateOfFire):
			newBullet = Bullet(self.x + self.w/2, self.y + self.h, 1, 0.8)
			bullets.append(newBullet)
			self.lastShoot = time.time()

	def Explode(self):
		sounds['invaderkilled'].play()
		self.fleet.ships[self.fleet.ships.index(self)] = None
		self.fleet.shipAmount -= 1
		self.fleet.DetectReadyShips()
		self.fleet.ArrangeSidePositions()

	def Show(self):
		surface.blit(self.image[self.stage], (self.x, self.y))
		#pygame.draw.rect(surface, (255,255,255), (self.x, self.y, self.w, self.h))


class EnemyFleet():
	def __init__(self, shipAmount, row = 1):
		self.ships = []
		self.shipAmount = shipAmount
		self.velX = 5
		self.velY = 8
		self.lastMove = 0
		self.rateOfMove = 20
		self.row = row
		self.shipLine = int(shipAmount/row)

		self.dirX = 1
		self.x = 50
		self.y = 20
		self.offsetX = 34
		self.offsetY = 24
		self.missingFromLeft = 0
		self.missingFromRight = 0
		self.offsetBetweenShips = 30

		self.readyToFire = []
		self.rateOfFire = 800
		self.lastShoot = 0

		self.soundStage = 0

	def CreateTheFleet(self):
		imageNum = 0
		for i in range(self.shipAmount):
			ship = Enemy(self, imageNum)
			self.ships.append(ship)
			if(((i+1) % (2*self.shipLine)) == 0):
				imageNum += 2

	def PlaceTheFleet(self):
		for i in range(self.row):
			for j in range(self.shipLine):
				self.ships[self.shipLine*i+j].y = self.y + self.offsetY*i
				self.ships[self.shipLine*i+j].x = self.x + self.offsetX*j
		self.DetectReadyShips()

	def ArrangeSidePositions(self):
		self.missingFromLeft = 0
		for i in range(self.shipLine):
			rowCheck = 0
			for j in range(self.row):
				if(self.ships[j*self.shipLine+i] == None):
					rowCheck+=1
			if(rowCheck==self.row):
				self.missingFromLeft+=1
			else:
				break

		self.missingFromRight = 0
		for i in range(self.shipLine-1, -1, -1):
			rowCheck = 0
			for j in range(self.row):
				if(self.ships[j*self.shipLine+i] == None):
					rowCheck+=1
			if(rowCheck==self.row):
				self.missingFromRight+=1
			else:
				break

	def Move(self):
		if((time.time() - self.lastMove)*1000 > self.rateOfMove*self.shipAmount):
			if(len(self.readyToFire) != 0):
				sounds[f'fastinvader{self.soundStage}'].play()
			if((self.dirX == -1 and self.x < self.offsetX - self.offsetX*self.missingFromLeft) or (self.dirX == 1 and self.x > width - self.offsetX - self.offsetBetweenShips*(self.shipLine) + self.offsetX*self.missingFromRight )):
				self.y += self.velY
				for ship in self.ships:
					if(ship != None):
						ship.ChangeStage()
						ship.y += self.velY
				self.dirX *= -1
			else:
				self.x += self.velX*self.dirX
				for i, ship in enumerate(self.ships):
					if(ship != None):
						ship.ChangeStage()
						ship.x += self.velX*self.dirX
			self.lastMove = time.time()
			self.soundStage += 1
			if(self.soundStage == 4): self.soundStage = 0


	def DetectReadyShips(self):
		self.readyToFire.clear()
		for i, ship in enumerate(self.ships):
			if(ship != None):
				check = divmod(i, self.shipLine)
				if(check[0] == self.row-1):
					self.readyToFire.append(ship)
				else:
					ready = True
					for j in range(1, self.row - check[0]):
						if(self.ships[i+j*self.shipLine] != None):
							ready = False
					if(ready):
						self.readyToFire.append(ship)
				
	def Shoot(self):
		if((time.time() - self.lastShoot)*1000 > self.rateOfFire):
			if(len(self.readyToFire) > 2):
				random.choice(self.readyToFire).Shoot()
				self.lastShoot = time.time()

	def Show(self):
		for ship in self.ships:
			if(ship != None):
				ship.Show()

class Block():
	def __init__(self, barrier, x, y):
		self.x = x
		self.y = y
		self.w = 6
		self.h = 8
		self.barrier = barrier

	def Explode(self):
		self.barrier.blocks.remove(self)

	def Show(self):
		pygame.draw.rect(surface, (0,255,0), (self.x, self.y, self.w, self.h))

class Barrier():
	def __init__(self, x, y, column, row):
		self.x = x
		self.y = y
		self.w = 6
		self.h = 8
		self.column = column
		self.row = row
		self.blocks = []

	def Place(self):
		barriers.append(self)
		for col in range(self.column):
			for row in range(self.row):
				newBlock = Block(self, self.x+col*self.w, self.y+row*self.h)
				self.blocks.append(newBlock)

	def Show(self):
		for block in self.blocks:
			block.Show()