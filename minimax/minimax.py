import typing
import math
import itertools
import copy

moves = ["up", "down", "left", "right"]


def paranoid_minimax(node, depth, alpha=-math.inf, beta=math.inf):

    if depth == 0 or is_terminal(node):
        return evaluate(node)

    best_score = -math.inf

    enemies = [
        snake for snake in node["board"]["snakes"]
        if snake["id"] != node["you"]["id"]
    ]

    # MAX: Try every move for our snake
    for our_move in moves:

        worst_enemy_score = math.inf

        # MIN: Try every combination of enemy moves
        enemy_combinations = itertools.product(
            moves, repeat=len(enemies)
        )

        for enemy_moves in enemy_combinations:

            # make sure the enemy moves are connected to the correct snake
            enemy_actions = {
                enemy["id"]: move
                for enemy, move in zip(enemies, enemy_moves)
            }

            # Simulate snakes moving and return the new game state
            new_state = simulate_turn(
                node,
                our_move,
                enemy_actions
            )

            score = paranoid_minimax(
                new_state,
                depth - 1,
                alpha,
                beta
            )

            worst_enemy_score = min(
                worst_enemy_score, score
            )

            beta = min(beta, worst_enemy_score)

            if beta <= alpha:
                break

        best_score = max(best_score, worst_enemy_score)
        alpha = max(alpha, best_score)

        if beta <= alpha:
            break

    return best_score


def choose_move(game_state, depth=2): #depth on 2 is still 4094 simulated path with two enemies however pruning helps reduce this number significantly

    best_move = "up"
    best_score = -math.inf

    enemies = [
        snake for snake in game_state["board"]["snakes"]
        if snake["id"] != game_state["you"]["id"]
    ]

    for our_move in moves:

        worst_enemy_score = math.inf

        for enemy_moves in itertools.product(
            moves, repeat=len(enemies)
        ):

            enemy_actions = {
                enemy["id"]: move
                for enemy, move in zip(enemies, enemy_moves)
            }

            new_state = simulate_turn(
                game_state,
                our_move,
                enemy_actions
            )

            score = paranoid_minimax(
                new_state,
                depth - 1
            )

            worst_enemy_score = min(
                worst_enemy_score, score
            )

        if worst_enemy_score > best_score:
            best_score = worst_enemy_score
            best_move = our_move

    return best_move



def evaluate(node):
    you = node["you"]
    opponents = node["board"]["snakes"]

    if you["health"] <= 0:
        return -100000

    score = you["health"] + len(you["body"])

    for enemy in opponents:
        if enemy["id"] != you["id"]:
            score -= enemy["health"] + len(enemy["body"])

    return score

def simulate_turn(node, our_move, enemy_actions):
    # 1. Copy the current game state
    simulated_state = node.copy()
    
    snakes = simulated_state["snakes"]
    board = simulated_state["board"]

    # 2. Calculate the new head position of every snake
    # 3. Move all snakes simultaneously
    # 4. Resolve collisions
    # 5. Remove dead snakes
    # 6. Update health
    # 7. Handle food
    # 8. Return the new game state
    pass

def is_terminal(node):
    snakes = node["board"]["snakes"]

    # Our snake has died
    if not any(s["id"] == node["you"]["id"] for s in snakes):
        return True

    # We are the last snake alive (dont know about this lol)
    if len(snakes) == 1:
        return True

    return False