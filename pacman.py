"""Pacman, classic arcade game.

Exercises

1. Change the board.
2. Change the number of ghosts.
3. Change where pacman starts.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter.
"""

from random import choice
from collections import deque
from turtle import bgcolor, clear, up, goto, dot, update, ontimer, \
                   setup, hideturtle, tracer, listen, onkey, done, Turtle
from freegames import floor, vector


# Initialize game state and main variables
state = {'score': 0}  # Score tracker
path = Turtle(visible=False)  # Turtle used to draw paths
writer = Turtle(visible=False)  # Turtle used to write the score
aim = vector(5, 0)  # Pacman's initial direction (moving right)
pacman = vector(-40, 0)  # Pacman's initial position


# Define the ghosts with their initial positions and directions
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
    [vector(100, 80), vector(0, -5)],
    [vector(-180, 80), vector(-5, 0)],
]


#  Tile
#  layout: 0 represents a wall
#  1 represents a path with a dot
#  2 is an empty path
#  fmt: off
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
# fmt: on


def square(x, y):
    """Draw square using path at (x, y)."""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    #  Draw the four sides of the square
    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


def offset(point):
    """Return offset of point in tiles."""
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


def valid(point):
    """Return True if point is valid in tiles."""
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


def world():
    """Draw world using path."""
    bgcolor('black')  # Set the background color to black
    path.color('blue')  # Set the path color to blue (walls)

    # Iterate over the tiles and draw squares for paths and walls
    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')


def move():
    """Move pacman and all ghosts."""
    writer.undo()  # Erase previous score
    writer.write(state['score'])  # Update score

    clear()  # Clear the screen

    # Move Pacman if the next position is valid (no wall)
    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    # Move each ghost
    for point, course in ghosts:
        move_ghost_smart(point, course)
        if valid(point + course):
            point.move(course)
        else:
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()  # Refresh the screen

    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return

    ontimer(move, 150)


def change(x, y):
    """Change pacman aim if valid."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


def bfs(start, goal):
    """Find the shortest path for the ghost to reach Pacman using BFS."""
    queue = deque([tuple(start)])
    visited = set([tuple(start)])
    # Dictionary to store parent nodes for path reconstruction
    parents = {}
    # Possible movement directions: right, left, up, and down
    directions = [vector(20, 0), vector(-20, 0),
                  vector(0, 20), vector(0, -20)]
    # Continue until there are no more nodes in the queue
    while queue:
        current = queue.popleft()  # Dequeue the first element

        if current == tuple(goal):
            path = []
            # Reconstruct the path by backtracking from the goal to the start
            while current in parents:
                path.append(vector(*current))
                current = parents[current]
            path.reverse()  # Reverse the path to get it from start to goal
            return path

        # Explore all possible neighbors in the four directions
        for direction in directions:
            neighbor = (current[0] + direction.x, current[1] + direction.y)
            if (valid(vector(neighbor[0], neighbor[1]))
                    and neighbor not in visited):
                # Mark the neighbor as visited and add it to the queue
                visited.add(neighbor)
                queue.append(neighbor)
                # Store the current node as the parent of the neighbor
                parents[neighbor] = current

    return []  # Return an empty list if no path was found


def move_ghost_smart(ghost, course):
    """Mueve el fantasma de manera inteligente hacia Pacman."""
    path_to_pacman = bfs(vector(int(ghost.x), int(ghost.y)),
                         vector(int(pacman.x), int(pacman.y)))
    if path_to_pacman:
        next_step = path_to_pacman[0]
        course.x = next_step.x - ghost.x
        course.y = next_step.y - ghost.y
    else:
        options = [vector(20, 0), vector(-20, 0),
                   vector(0, 20), vector(0, -20)]
        plan = choice(options)
        course.x = plan.x
        course.y = plan.y


# Set up the game window
setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()  # Listen for keyboard inputs


# Bind arrow keys to change pacman's direction
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')


# Draw the world and start the game loop
world()
move()
done()  # Finish the game