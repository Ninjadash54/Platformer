import turtle
import sys
import math
import random
from inspect import v
#Screen Width/Height
WIDTH = 1200
HEIGHT = 800

# The Gravity of the Platformer
GRAVITY = -0.12

#All Possible Colors Needed For this
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (11, 102, 35)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (246, 169, 15)
YG = (199, 234, 70)


# Create the screen
wn = turtle.Screen()
wn.colormode(255)
wn.title("Pr")
wn.setup(WIDTH, HEIGHT)
wn.bgcolor(BLACK)
wn.tracer(0)



# Create pen
pen = turtle.Turtle()
pen.speed(0)
pen.penup()
pen.color(WHITE)
pen.hideturtle()


# Create classes
class Sprite():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.width = width
        self.height = height
        self.color = WHITE
        self.friction = 0.99

    def goto(self, x, y):
        self.x = x
        self.y = y

    def render(self):
        pen.pencolor(self.color)
        pen.fillcolor(self.color)
        pen.penup()
        pen.goto(self.x - self.width / 2.0, self.y + self.height / 2.0)
        pen.pendown()
        pen.begin_fill()
        pen.goto(self.x + self.width / 2.0, self.y + self.height / 2.0)
        pen.goto(self.x + self.width / 2.0, self.y - self.height / 2.0)
        pen.goto(self.x - self.width / 2.0, self.y - self.height / 2.0)
        pen.goto(self.x - self.width / 2.0, self.y + self.height / 2.0)
        pen.end_fill()
        pen.penup()

    def is_aabb_collision(self, other):
        # Axis Aligned Bounding Box
        x_collision = (math.fabs(self.x - other.x) * 2) < (self.width + other.width)
        y_collision = (math.fabs(self.y - other.y) * 2) < (self.height + other.height)
        return (x_collision and y_collision)

#Player
class Player(Sprite):
    def __init__(self, x, y, width, height):
        Sprite.__init__(self, x, y, width, height)
        self.color = GREEN

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += GRAVITY

    def jump(self):
        self.dy = 7

    def left(self):
        self.dx -= 1
        if self.dx < -3:
            self.dx = -3

    def right(self):
        self.dx += 1
        if self.dx > 3:
            self.dx = 3
#Portal
class Portal(Sprite):
    def __init__(self, x, y, width, height):
        Sprite.__init__(self, x, y, width, height)
        self.color = BLUE
#Large
class Large(Sprite):
    def __init__(self, x, y, width, height):
        Sprite.__init__(self, x, y, width, height)
        self.color = BLUE
#Opener
class Opener(Sprite):
    def __init__(self, x, y, width, height):
        Sprite.__init__(self, x, y, width, height)
        self.color = WHITE
#Key
class Key(Sprite):
    def __init__(self, x, y, width, height):
        Sprite.__init__(self, x, y, width, height)
        self.color = YELLOW
#End
class End(Sprite):
    def __init__(self, x, y, width, height):
        Sprite.__init__(self, x, y, width, height)
        self.color = RED
#Tunnel For Key
class Tunnel(Sprite):
    def __init__(self, x, y, width, height):
        Sprite.__init__(self, x, y, width, height)
        self.color = WHITE



# Create font

# Create sounds

# Create game objects
end = End(-370, -180, 20,20)
open = Opener(-350, -100, 80, 200)
key = Key(-40, 0, 1, 1)
tun = Tunnel(0, -7, 600, 18)
large = Large(180, 240, 30, 60)
portal = Portal(400, -160, 20, 100)
player = Player(0, 400, 20, 40)
blocks = []
blocks.append(Sprite(0, 200, 400, 20))
blocks.append(Sprite(0, -5, 600, 20))
blocks.append(Sprite(0, -200, 1000, 20))
blocks.append(Sprite(-400, -100, 20, 200))

def player_jump():
    for block in blocks:
        if player.is_aabb_collision(block):
            player.jump()
            break




# Keyboard binding
wn.listen()
wn.onkeypress(player.left, "Left")
wn.onkeypress(player.right, "Right")
wn.onkeypress(player_jump, "Up")

# Main game loop
while True:
    # Move/Update objects
    player.move()

    # Check for collisions
    for block in blocks:
        if player.is_aabb_collision(block):
            # Player is to the left
            if player.x < block.x - block.width / 2.0 and player.dx > 0:
                player.dx = 0
                player.x = block.x - block.width / 2.0 - player.width / 2.0
            # Player is to the right
            elif player.x > block.x + block.width / 2.0 and player.dx < 0:
                player.dx = 0
                player.x = block.x + block.width / 2.0 + player.width / 2.0
            # Player is above
            elif player.y > block.y:
                player.dy = 0
                player.y = block.y + block.height / 2.0 + player.height / 2.0 - 1
                player.dx *= block.friction
            # Player is below
            elif player.y < block.y:
                player.dy = 0
                player.y = block.y - block.height / 2.0 - player.height / 2.0

    # Collision for smaller
    if player.is_aabb_collision(portal):
        if player.x < portal.x - portal.width / 2.0 and player.dx > 0:
            player.width = 10
            player.height = 20
            tun.y = 50
            key.width = 50
            key.height = 40
            key.y = 20
        elif player.x > portal.x + portal.width / 2.0 and player.dx < 0:
            player.width = 10
            player.height = 20
            tun.y = 50
            key.width = 50
            key.height = 40
            key.y = 20
        # Player is above
        elif player.y > portal.y:
            player.width = 10
            player.height = 20
            tun.y = 50
            key.width = 50
            key.height = 40
            key.y = 20

    # if player.is_aabb_collision(end):
    #     if player.x < end.x - end.width / 2.0 and player.dx > 0:
    #         wn.addshape('python2.gif')
    #         pen.shape('python2.gif')
    #         wn.mainloop()
    #     # Player is to the right
    #     elif player.x > end.x + end.width / 2.0 and player.dx < 0:
    #         wn.addshape('python2.gif')
    #         pen.shape('python2.gif')
    #         wn.mainloop()
    #     # Player is above
    #     elif player.y > end.y:
    #         wn.addshape('python2.gif')
    #         pen.shape('python2.gif')
    #         wn.mainloop()
    #     # Player is below
    #     elif player.y < end.y:
    #         yes = wn.addshape('python2.gif')
    #         pen.shape('python2.gif')
    #         wn.mainloop()

# Collision for Key
    if player.is_aabb_collision(key):
        if player.x < key.x - key.width / 2.0 and player.dx > 0:
            key.height = 0.0000001
            key.width = 0.0000001
            open.x = -300
            player.color = YG
        # Player is to the right
        elif player.x > key.x + key.width / 2.0 and player.dx < 0:
            key.height = 0.0000001
            key.width = 0.0000001
            open.x = -300
            player.color = YG
        # Player is above
        elif player.y > key.y:
            key.height = 0.0000001
            key.width = 0.0000001
            open.x = -300
            player.color = YG
        # Player is below
        elif player.y < key.y:
            key.height = 0.0000001
            key.width = 0.0000001
            open.x = -300
            player.color = YG
# Collision for Tunnel
    if player.is_aabb_collision(tun):
        # Player is to the left
        if player.x < tun.x - tun.width / 2.0 and player.dx > 0:
            player.dx = 0
            player.x = tun.x - tun.width / 2.0 - player.width / 2.0
        # Player is to the right
        elif player.x > tun.x + tun.width / 2.0 and player.dx < 0:
            player.dx = 0
            player.x = tun.x + tun.width / 2.0 + player.width / 2.0
        # Player is above
        elif player.y > tun.y:
            player.dy = 0
            player.y = tun.y + tun.height / 2.0 + player.height / 2.0 - 1
        # Player is below
        elif player.y < tun.y:
            player.dy = 0
            player.y = tun.y - tun.height / 2.0 - player.height / 2.0
# Collision for Opener
    if player.is_aabb_collision(open):
        if player.x < open.x - open.width / 2.0 and player.dx > 0:
            player.dx = 0
            player.x = open.x - open.width / 2.0 - player.width / 2.0
        # Player is to the right
        elif player.x > open.x + open.width / 2.0 and player.dx < 0:
            player.dx = 0
            player.x = open.x + open.width / 2.0 + player.width / 2.0
        # Player is above
        elif player.y > open.y:
            player.dy = 0
            player.y = open.y + open.height / 2.0 + player.height / 2.0 - 1
            player.dx *= open.friction
        # Player is below
        elif player.y < open.y:
            player.dy = 0
            player.y = open.y - open.height / 2.0 - player.height / 2.0


    # Collision for Enlarger
    if player.is_aabb_collision(large):
        # Player is to the left
        if player.x < large.x - large.width / 2.0 and player.dx > 0:
            player.width = 20
            player.height = 40
        # Player is to the right
        elif player.x > large.x + large.width / 2.0 and player.dx < 0:
            player.width = 20
            player.height = 40
        # Player is above
        elif player.y > large.y:
            player.width = 20
            player.height = 40




                # Border check the player
    if player.y < -400:
        player.goto(0, 400)
        player.dx = 0
        player.dy = 0

    # Render (Draw stuff)

    # Render objects
    # yes.render()
    tun.render()
    end.render()
    open.render()
    key.render()
    large.render()
    portal.render()
    player.render()
    for block in blocks:
        block.render()

    # Flip the display
    wn.update()

    # Clear the screen
    pen.clear()