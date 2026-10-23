"""Task: encode one Battlesnake observation as a tuple of six small integers.

Return (safe_up, safe_down, safe_left, safe_right, food_x, food_y).
Use supplied safe_directions() for the first four flags (0 or 1).
For each food coordinate use 0=smaller, 1=equal, 2=larger than the head coordinate.
If there is no food, use (1, 1). With several apples select the nearest by
Manhattan distance, breaking ties by x and then y.

Do not put absolute coordinates, whole body lists or turn numbers in the key.
This will massively increase the number of observable states and make training very hard.
We will try this once we introduced deep reinforcement learning next week.
"""
from supplied_environment import safe_directions


def encode_state(observation):
    head = observation['you']['head']
    food = observation['board']['food']
    if not food:
        food_x, food_y = 1, 1
    else:
        nearest_food = min(food, key=lambda p: (abs(p['x']-head['x'])+abs(p['y']-head['y']), p['x'], p['y']))





        if nearest_food['x'] < head['x']:
            food_x = 0
        elif nearest_food['x'] == head['x']:
            food_x = 1
        else:
            food_x = 2

        if nearest_food['y'] < head['y']:
            food_y = 0
        elif nearest_food['y'] == head['y']:
            food_y = 1
        else:
            food_y = 2


    safe_up, safe_down, safe_left, safe_right = safe_directions(observation)
    return(safe_up, safe_down, safe_left, safe_right, food_x, food_y)
    # TODO: access observation['you']['head'] and observation['board']['food'].
    # TODO: combine safety flags and relative food direction into a tuple.



if __name__ == '__main__':
    from supplied_environment import SoloBattlesnake
    observation, _ = SoloBattlesnake().reset(seed=7)
    key = encode_state(observation)
    print('Encoded observation:', key)
    assert len(key) == 6 and all(0 <= k < n for k,n in zip(key, (2,2,2,2,3,3)))
    print('Maximum: 144 encoded states and 576 state-action values.')
