# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import numpy as np
from math import sqrt

from sympy.parsing.sympy_parser import null
from Exercise2.step_0_state_attributes import make_training_example

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data

recording_enabled = False
recording_seed = None
recorded_rows = []

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position



def record_state(game_state: typing.Dict, direction: str):
    """Store one example using the shared schema in step_0_state_attributes.py."""
    recorded_rows.append(make_training_example(
        game_state, direction, seed=recording_seed, label_source="rule_based_agent"
    ))


def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    print("Y: " + str(my_head["y"]))
    print("X: " + str(my_head["x"]))

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False



    if my_head["y"] == game_state['board']['height'] -1:
        print("HEAD Y IS BOARD HEIGHT")
        is_move_safe["up"] = False

    if my_head["y"] == 0:
        print("HEAD Y IS ZERO")
        is_move_safe["down"] = False

    if my_head["x"] == game_state['board']['width'] -1:
        print("HEAD X IS BOARD WIDTH")
        is_move_safe["right"] = False

    if my_head["x"] == 0:
        print("HEAD X IS ZERO")
        is_move_safe["left"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    # board_width = game_state['board']['width']
    # board_height = game_state['board']['height']

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    for body in game_state['you']['body'][1:]:
        if my_head["x"]+1 == body["x"] and my_head["y"] == body["y"]:
            is_move_safe["right"] = False
        if my_head["x"]-1 == body["x"] and my_head["y"] == body["y"] :
            is_move_safe["left"] = False
        if my_head["y"]+1 == body["y"] and my_head["x"] == body["x"]:
            is_move_safe["up"] = False
        if my_head["y"]-1 == body["y"] and my_head["x"] == body["x"]:
            is_move_safe["down"] = False

    # my_body = game_state['you']['body']

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']

    for snake in opponents:
        print(snake["body"])
        for body in snake["body"]:
            if my_head["x"]+1 == body["x"] and my_head["y"] == body["y"]:
                is_move_safe["right"] = False
            if my_head["x"]-1 == body["x"] and my_head["y"] == body["y"] :
                is_move_safe["left"] = False
            if my_head["y"]+1 == body["y"] and my_head["x"] == body["x"]:
                is_move_safe["up"] = False
            if my_head["y"]-1 == body["y"] and my_head["x"] == body["x"]:
                is_move_safe["down"] = False

    # opponents = game_state['board']['snakes']

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = move_towards_food(game_state)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']

    move_towards_food(game_state)

    if recording_enabled:
        record_state(game_state, next_move)
    return {"move": next_move}

def move_towards_food(game_state):
    board_x= game_state['board']['width']
    board_y= game_state['board']['height']

    head = game_state['you']['body'][0]
    head_x = head["x"]
    head_y = head["y"]
    head = (head_x, head_y)

    grid = np.zeros ((board_x, board_y))
    snakes = game_state['board']['snakes']

    for snake in snakes:
        for body in snake["body"][1:]:
            grid[body["x"], body["y"]] = 1

    print(grid)






    openList = []
    closedList = []
    food = game_state['board']['food'][0]
    food_x = food["x"]
    food_y =  food["y"]
    food = (food_x, food_y)


    start_node = Node(None, head)
    print(f"start_node: {start_node.position}")
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, food)
    end_node.g = end_node.h = end_node.f = 0

    openList.append(start_node)

    while len(openList) > 0:
        current_node = openList[0]
        current_index = 0
        for index, item in enumerate(openList):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        openList.pop(current_index)
        closedList.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            path = path[::-1]
            if path[1][0] > start_node.position[0]:
                return "right"
            if path[1][0] < start_node.position[0]:
                return "left"
            if path[1][1] > start_node.position[1]:
                return "up"
            if path[1][1] < start_node.position[1]:
                return "down"



        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if node_position[0] < 0 or node_position[0] >= board_x or node_position[1] < 0 or node_position[1] >= board_y:
                continue

            if grid[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(parent=current_node, position=node_position)
            children.append(new_node)
        for child in children:
            for closed_child in closedList:
                if child == closed_child:
                    continue

            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            for open_node in openList:
                if child == open_node and child.g > open_node.g:
                    continue

            openList.append(child)



# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})


