# Space Invaders

Little prototype version of the old arcade game Space Invaders from 1980s, made with Python's Pygame.

## License

This project is [MIT](https://github.com/ErtyumPX/SpaceInvaders/blob/main/LICENSE) licensed.

## Setup

The python script "main.py" is the launcher of the game. After you clone or download the repository, you can simply double click that file.

Beware that used Python version of this project is [3.8.3](https://www.python.org/downloads/release/python-383) and the used Pygame version is [2.0.1](https://www.pygame.org/project/5409/7928).

<img src="https://github.com/ErtyumPX/SpaceInvaders/blob/master/Assets/README/SpaceInvaders.JPG" width=50% height=50%>

<hr>

## Mechanics & Algorithms

### Enemy Fleet Movement

Invaders always acts coordinated with a certain speed. Every time they loose a fellow ship, they get faster. When they reach the end of the screen, they flip the movement to the other side.

### Enemy Attack

The game starts with an 8x6 ship placed invaders fleet. Only the ships on the front line are allowed to attack, with a reasonable cooldown. Every time an invader in the front line is eliminated, the one on the back takes over.

Plus, invaders does not shoot randomly but only if the user "protecter" are on their sight. If there is nobody in sight for some time, they start shooting randomly to limit user's movement.

### User Interface Elements

Pygame's itself does not support enhanced UI elements. The texts used in this game are from [PyGameEngine](https://github.com/ErtyumPX/PyGameEngine).

<hr>

## Inefficiencies

A one-dimensional array was used to hold invaders. This causes many lines of code when determining which invader is on the front line and which can attack. Yet this was more efficient for the movement mechanich.

Also there is a glitch with the sound effects at some certain scenerious, does not cause much problem yet it was hard to fix because sound system in Pygame is not the best.

