"""Task: return the last history observations and the NEXT future actions.

features: (game_turns, feature_count), encoded by supplied code.
actions: (game_turns,), where actions[t] causes state t -> state t+1.
t: index of the final OBSERVED state. Both slices must include index t.
Return arrays of shapes (history, feature_count) and (future,).
The caller handles game boundaries and excludes terminal-horizon examples.
"""
import numpy as np


def student_make_example(features, actions, t, history, future):
    inputs = features[t - history + 1:t + 1]
    outputs = actions[t + 1:t + 1 + future]
    return inputs, outputs
    

if __name__ == '__main__':
    from supplied_pipeline import prepare
    prepare(student_make_example)
