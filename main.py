import turtle
import math

WIDTH = 1200
HEIGHT = 800

GRAVITY = -0.12

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (122, 37, 118)



# Create the screen
wn = turtle.Screen()
wn.colormode(255)
wn.title("Platformer")
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
        self.friction = 0.999

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

class Portal(Sprite):
    def __init__(self, x, y, width, height):
        Sprite.__init__(self, x, y, width, height)
        self.color = BLUE

class Large(Sprite):
    def __init__(self, x, y, width, height):
        Sprite.__init__(self, x, y, width, height)
        self.color = BLUE

class Key(Sprite):
    def __init__(self, x, y, width, height):
        Sprite.__init__(self, x, y, width, height)
        self.color = RED

class End(Sprite):
    def __init__(self, x, y, width, height):
        Sprite.__init__(self, x, y, width, height)
        self.color = PURPLE


# Create font

# Create sounds

# Create game objects
end = End(-40, -70, 50, 40)
key = Key(20, 20, 40, 50)
portal = Portal(400, -160, 20, 100)
player = Player(0, 400, 20, 40)
large = Large(180, 240, 30, 60)
blocks = []
blocks.append(Sprite(0, 200, 400, 20))
blocks.append(Sprite(0, 0, 600, 20))
blocks.append(Sprite(0, -200, 1000, 20))
blocks.append(Sprite(-400, -100, 100, 200))


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
    player.move()

    # Check for collisions
    for block in blocks:
        if player.is_aabb_collision(block):
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
        # Player is to the left

# Collision for smaller
if player.is_aabb_collision(portal):
    # Player is to the left
    if player.x < portal.x - portal.width / 2.0 and player.dx > 0:
        player.width = 10
        player.height = 20
    # Player is to the right
    elif player.x > portal.x + portal.width / 2.0 and player.dx < 0:
        player.width = 10
        player.height = 20
    # Player is above
    elif player.y > portal.y:
        player.width = 10
        player.height = 20

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

if player.is_aabb_collision(key):
     # Player is to the left
     if player.x < key.x - key.width / 1.0 and player.dx > 0:
         key.width = 1
         key.height = 1
#       Player is to the right
     elif player.x > key.x + key.width / 1.0 and player.dx < 0:
        key.width = 1
        key.height = 1

                # Border check the player
if player.y < -400:
    player.goto(0, 400)
    player.dx = 0
    player.dy = 0

    # Render (Draw stuff)

    # Render objects
end.render()
player.render()
key.render()
portal.render()
large.render()
for block in blocks:
    block.render()

    # Flip the display
    wn.update()

    # Clear the screen
    pen.clear()
