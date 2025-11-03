import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np


class DeepQNetwork:
    """
    A model that uses a Deep Q-value Network (DQN) to approximate Q(s,a) as part
    of reinforcement learning.
    """

    def __init__(self, state_dim, action_dim):
        self.num_actions = action_dim
        self.state_size = state_dim

        # Remember to set self.learning_rate, self.numTrainingGames,
        # self.parameters, and self.batch_size!
        "*** YOUR CODE HERE ***"
        self.learning_rate = 0.0008
        self.num_hiddens = 256
        self.numTrainingGames = 10000
        self.batch_size = 32
        
        self.parameters = nn.ParameterList(
            [
                nn.Parameter(torch.randn(self.state_size, self.num_hiddens) * 0.01),
                nn.Parameter(torch.zeros(self.num_hiddens)),
                nn.Parameter(torch.randn(self.num_hiddens, self.num_actions) * 0.01),
                nn.Parameter(torch.zeros(self.num_actions)),
            ]
        )
        
        # Adam 优化器
        self.optimizer = optim.Adam(self.parameters, lr=self.learning_rate)

    def ensure_tensor(self, x):
        if type(x).__name__ == "Constant":
            try:
                x = torch.tensor(x.data, dtype=torch.float32)
            except AttributeError:
                x = torch.tensor(list(x), dtype=torch.float32)
        elif isinstance(x, np.ndarray):
            x = torch.tensor(x, dtype=torch.float32)
        elif not isinstance(x, torch.Tensor):
            x = torch.tensor(x, dtype=torch.float32)
        if x.ndim == 1:
            x = x.unsqueeze(0)
        return x

    def set_weights(self, layers):
        self.parameters = nn.ParameterList(
            [p.clone().detach().requires_grad_() for p in layers]
        )
        self.optimizer = optim.Adam(self.parameters, lr=self.learning_rate)

    def get_loss(self, states, Q_target):
        """
        Returns the Squared Loss between Q values currently predicted
        by the network, and Q_target.
        Inputs:
            states: a (batch_size x state_dim) numpy array
            Q_target: a (batch_size x num_actions) numpy array, or None
        Output:
            loss node between Q predictions and Q_target
        """
        "*** YOUR CODE HERE ***"
        states = self.ensure_tensor(states)
        Q_target = self.ensure_tensor(Q_target)
        
        predictions = self.run(states)
        loss = torch.mean((predictions - Q_target) ** 2)
        return loss

    def run(self, states):
        """
        Runs the DQN for a batch of states.
        The DQN takes the state and returns the Q-values for all possible actions
        that can be taken. That is, if there are two actions, the network takes
        as input the state s and computes the vector [Q(s, a_1), Q(s, a_2)]
        Inputs:
            states: a (batch_size x state_dim) numpy array
            Q_target: a (batch_size x num_actions) numpy array, or None
        Output:
            result: (batch_size x num_actions) numpy array of Q-value
                scores, for each of the actions
        """
        "*** YOUR CODE HERE ***"
        states = self.ensure_tensor(states)

        w1, b1, w2, b2 = self.parameters
        mid_result1 = torch.matmul(states, w1) + b1
        mid_result1 = torch.relu(mid_result1)
        result = torch.matmul(mid_result1, w2) + b2

        return result

    def gradient_update(self, states, Q_target):
        """
        Update your parameters by one gradient step with the .update(...) function.
        Inputs:
            states: a (batch_size x state_dim) numpy array
            Q_target: a (batch_size x num_actions) numpy array, or None
        Output:
            None
        """
        "*** YOUR CODE HERE ***"

        self.optimizer.zero_grad()
        loss = self.get_loss(states, Q_target)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.parameters, 1.0)
        self.optimizer.step()
        return loss.item()
