import os
import time
import math
from termcolor import colored

# This is the Canvas class. It defines some height and width, and a
# matrix of characters to keep track of where the TerminalScribes are moving
class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        # This is a grid that contains data about where the
        # TerminalScribes have visited
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]

    # Returns True if the given point is outside the boundaries of the Canvas
    def hitsWall(self, point):
        return round(point[0]) < 0 or round(point[0]) >= self._x or round(point[1]) < 0 or round(point[1]) >= self._y

    # Set the given position to the provided character on the canvas
    def setPos(self, pos, mark):
        self._canvas[round(pos[0])][round(pos[1])] = mark

    # Clear the terminal (used to create animation)
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # Clear the terminal and then print each line in the canvas
    def print(self):
        self.clear()
        for y in range(self._y):
            print(' '.join([col[y] for col in self._canvas]))

class TerminalScribe:
    def __init__(self, canvas):
        self.canvas = canvas
        self.trail = '.'
        self.mark = '*'
        self.framerate = 0.01
        self.pos = [0, 0]

        self.direction = [0,1]
    def setAngle(self, angle_deg):
        angle_rad = (angle_deg/180) * math.pi
        self.direction = [math.sin(angle_rad),-math.cos(angle_rad)]

    def moveForward(self):
        pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
        if not self.canvas.hitsWall(pos):
            self.draw(pos)

    def up(self):
        self.direction = [0,-1]
        self.moveForward()

    def down(self):
        self.direction = [0,1]
        self.moveForward()
    def right(self):
        self.direction = [1,0]
        self.moveForward()

    def left(self):
        self.direction = [-1,0]
        self.moveForward()

    def draw(self, pos):
        # Set the old position to the "trail" symbol
        self.canvas.setPos(self.pos, self.trail)
        # Update position
        self.pos = pos
        # Set the new position to the "mark" symbol
        self.canvas.setPos(self.pos, colored(self.mark, 'red'))
        # Print everything to the screen
        self.canvas.print()
        # Sleep for a little bit to create the animation
        time.sleep(self.framerate)

    def drawSquare(self, size):
        for i in range(1,size):
            self.down()
        for i in range(1,size):
            self.right()
        for i in range(1,size):
            self.up()
        for i in range(1,size):
            self.left()

    def drawRectangle(self, size_a, size_b):
        for i in range(size_a):
            self.right()
        for i in range(size_b):
            self.down()
        for i in range(size_a):
            self.left()
        for i in range(size_b):
            self.up()

    def drawCircle(self, center_x, center_y, radius):
        for i in range(0,360,5):
            self.pos = [center_x, center_y]
            self.setAngle(i)
            for j in range(radius):
                self.moveForward()

# # Create a new Canvas instance that is 30 units wide by 30 units tall
canvas = Canvas(50, 50)

# Create a new scribe and give it the Canvas object
scribe = TerminalScribe(canvas)

# scribe.drawRectangle(5,10)

# scribe.drawSquare(10)

scribe.drawCircle(25,25,10)


