"""Task: define an RNN and a linear layer to predict the next x actions.

Input: (batch, HISTORY, number of features).
1. Use nn.RNN(..., batch_first=True).
2. Select the last output: outputs[:, -1, :].
3. Apply nn.Linear(hidden_size, future * 4).
4. Reshape to (batch, future, 4). Return LOGITS, not softmax probabilities.
The supplied pipeline handles training, validation and plotting.
"""
import torch
from torch import nn


class StudentRNN(nn.Module):
    def __init__(self, input_size, hidden_size, future):
        super().__init__()
        # TODO: store future and define the recurrent/output layers.
        self.future = future
        self.rnn = nn.RNN(input_size=input_size, hidden_size=hidden_size, batch_first=True)
        self.output_layer = nn.Linear(hidden_size, future * 4)

    def forward(self, observations):
        # TODO: recurrent outputs -> last output -> action logits.
        outputs, _ = self.rnn(observations)
        predictions = self.output_layer(outputs[:, -1, :])
        return predictions.view(-1, self.future, 4)


ActionRNN = StudentRNN

if __name__ == '__main__':
    from supplied_pipeline import train_cli
    train_cli('rnn', ActionRNN)
