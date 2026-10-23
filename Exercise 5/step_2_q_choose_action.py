"""Task: choose among all four actions with an epsilon-greedy policy.

With probability epsilon choose uniformly from 0..3; otherwise select a maximum
Q-value. Break ties randomly using rng. q_values is a length-4 NumPy array.
rng is a supplied np.random.Generator (use it rather than global randomness).
"""
import numpy as np


def choose_action(q_values, epsilon, rng):
    if rng.random() < epsilon:
        return rng.integers(4)
    else:
        max_q = np.max(q_values)
        max_indices = np.where(q_values == max_q)[0]
        return rng.choice(max_indices)

    # TODO: exploration, exploitation and random tie-breaking.



if __name__ == '__main__':
    values = np.array([0., 2., -1., 2.])
    for epsilon in [1., 0.]:
        rng = np.random.default_rng(5)
        counts = np.bincount([choose_action(values, epsilon, rng) for _ in range(1000)], minlength=4)
        print(f'epsilon={epsilon}: counts for up/down/left/right = {counts}')
    print('Explain how these counts reflect exploration and exploitation.')
