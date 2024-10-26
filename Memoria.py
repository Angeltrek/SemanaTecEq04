# Necessary module imports
from random import shuffle
from turtle import Screen, Turtle, ontimer, onscreenclick, addshape, clear, update, setup, shape, tracer, done, goto, stamp, up, down, color, write, hideturtle
from freegames import path

# Global variables
car = path('car.gif')  # Path to the car image
tiles = list(range(32)) * 2  # Creates a list with 32 pairs of numbers
state = {'mark': None}  # State to save the marked position
hide = [True] * 64  # List that defines if the tiles are hidden


def square(x, y):
    """Draws a white square with a black border at position (x, y)."""
    up()
    goto(x, y)
    down()
    color('black', 'white')
    begin_fill()
    for count in range(4):
        forward(50)
        left(90)
    end_fill()


def index(x, y):
    """Converts (x, y) coordinates into a tile index."""
    return int((x + 200) // 50 + ((y + 200) // 50) * 8)


def xy(count):
    """Converts the tile index into (x, y) coordinates."""
    return (count % 8) * 50 - 200, (count // 8) * 50 - 200


def tap(x, y):
    """Updates the marked tile and hidden tile status based on tap."""
    spot = index(x, y)  # Gets the tile index
    mark = state['mark']  # Gets the currently marked tile

    # Checks if there is no marked tile or it does not match the current spot
    if mark is None or mark == spot or tiles[mark] != tiles[spot]:
        state['mark'] = spot  # Marks the current tile
    else:
        hide[spot] = False  # Reveals the tiles if they match
        hide[mark] = False
        state['mark'] = None  # Resets the marked tile


def draw():
    """Draws the background image and tiles on the screen."""
    clear()  # Clears the screen
    goto(0, 0)  # Positions at the center
    shape(car)  # Sets the car image
    stamp()  # Stamps the car image

    # Draws all 8x8 tiles
    for count in range(64):
        if hide[count]:  # Draws only if the tile is hidden
            x, y = xy(count)
            square(x, y)

    mark = state['mark']

    # Draws the number of the marked tile
    if mark is not None and hide[mark]:
        x, y = xy(mark)
        up()
        goto(x + 2, y)
        color('black')
        write(tiles[mark], font=('Arial', 30, 'normal'))

    update()  # Updates the screen
    ontimer(draw, 100)  # Redraws every 100 ms


# Initial setup
shuffle(tiles)  # Shuffles the tiles
setup(420, 420, 370, 0)  # Sets up the game window
addshape(car)  # Adds the car shape
hideturtle()  # Hides the turtle cursor
tracer(False)  # Turns off the drawing animation
onscreenclick(tap)  # Calls the tap function on click
draw()  # Calls the draw function
done()  # Ends the program when the window is closed
