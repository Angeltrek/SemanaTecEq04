"""Tic Tac Toe

Exercises

1. Give the X and O a different color and width.
2. What happens when someone taps a taken spot?
3. How would you detect when someone has won?
4. How could you create a computer player?
"""

# Importing specific functions from the turtle graphics library
from turtle import up, goto, down, circle, update
from turtle import setup, hideturtle, tracer, onscreenclick, done
from turtle import color
# Importing the line function from the freegames library
from freegames import line

# Set to store the coordinates of occupied cells
taken_positions = set()


def grid():
    """Draw tic-tac-toe grid."""
    line(-67, 200, -67, -200)
    line(67, 200, 67, -200)
    line(-200, -67, 200, -67)
    line(-200, 67, 200, 67)


def drawx(x, y, size=60):
    """Draw X player."""
    # Set color for the cross
    color('red')
    # Move to starting point to draw the first diagonal line of the X
    up()
    goto(x - size / 2, y - size / 2)
    down()
    # Draw first line of the X
    goto(x + size / 2, y + size / 2)
    # Move to starting point for the second diagonal line of the X
    up()
    goto(x + size / 2, y - size / 2)
    down()
    # Draw second line of the X
    goto(x - size / 2, y + size / 2)
    # Add the cell coordinates to the set of occupied cells
    taken_positions.add((x, y))


def drawo(x, y, size=60):
    """Draw O player ."""
    # Set color for the circle
    color('green')
    # Move to starting point to draw the circle
    up()
    goto(x, y - size / 2)
    down()
    # Draw the circle with specified size
    circle(size / 2)
    # Add the cell coordinates to the set of occupied cells
    taken_positions.add((x, y))


def floor(value):
    """Round value down to grid with square size 133."""
    return ((value + 200) // 133) * 133 - 200


# Dictionary to keep track of the current player (0 for X, 1 for O)
state = {'player': 0}
# List of functions to draw X and O, respectively
players = [drawx, drawo]


def tap(x, y):
    """Draw X or O in tapped square."""
    # Align the tapped coordinates with the nearest grid cell
    x = round(x / 133) * 133
    y = round(y / 133) * 133
    # Check if the selected cell is already occupied
    if (x, y) in taken_positions:
        print("Oh no, the box is occupied")
        return
    # Determine the current player and draw the corresponding symbol
    player = state['player']
    draw = players[player]
    draw(x, y)
    # Update the screen to reflect changes
    update()
    # Switch to the other player for the next turn
    state['player'] = not player


# Set up the drawing window with specific size and position
setup(420, 420, 370, 0)
# Hide the turtle to avoid showing the cursor
hideturtle()
# Disable automatic drawing updates for better performance
tracer(False)
# Draw the initial grid
grid()
# Update the screen to display the grid
update()
# Set up the screen to call the tap function when clicked
onscreenclick(tap)
# Keep the window open
done()
