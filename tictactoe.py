"""Tic Tac Toe

Exercises

1. Give the X and O a different color and width.
2. What happens when someone taps a taken spot?
3. How would you detect when someone has won?
4. How could you create a computer player?
"""

# Adjusted the library
from turtle import up, goto, down, circle, update
from turtle import setup, hideturtle, tracer, onscreenclick, done
from turtle import color

from freegames import line

# Set to store the coordinates of occupied cells
taken_positions = set()


def grid():
    """Draw tic-tac-toe grid."""
    line(-67, 200, -67, -200)
    line(67, 200, 67, -200)
    line(-200, -67, 200, -67)
    line(-200, 67, 200, 67)


def drawx(x, y):
    """Draw X player."""
    # Set color for the cross
    color('red')
    line(x, y, x + 133, y + 133)
    line(x, y + 133, x + 133, y)
    # Add the cell coordinates to the set of occupied cells
    taken_positions.add((x, y))


def drawo(x, y):
    """Draw O player."""
    # Set color for the circle
    color('green')
    up()
    goto(x + 67, y + 5)
    down()
    circle(62)
    # Add the cell coordinates to the set of occupied cells
    taken_positions.add((x, y))


def floor(value):
    """Round value down to grid with square size 133."""
    return ((value + 200) // 133) * 133 - 200


state = {'player': 0}
players = [drawx, drawo]


def tap(x, y):
    """Draw X or O in tapped square."""
    x = floor(x)
    y = floor(y)
    # Check if the selected cell is already occupied
    if (x, y) in taken_positions:
        print("Oh no, the box is occupied")
        return
    # Determine the current player and draw the corresponding symbol
    player = state['player']
    draw = players[player]
    draw(x, y)
    update()
    state['player'] = not player


setup(420, 420, 370, 0)
hideturtle()
tracer(False)
grid()
update()
onscreenclick(tap)
done()
