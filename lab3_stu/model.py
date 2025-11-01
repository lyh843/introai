import torch
import torch.nn as nn 
import numpy as np

class DeepQNetwork():
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
        self.learning_rate = 0.01
        self.num_hiddens = 100
        self.parameters = [
            np.random.randn(self.state_size, self.num_hiddens) * 0.01,
            np.zeros(self.num_hiddens),
            np.random.randn(self.num_hiddens, self.num_actions) * 0.01,
            np.zeros(self.num_actions)
        ]
        self.numTrainingGames = 2000
        self.batch_size = 20
        
        # Adam optimizer state
        self.m = [np.zeros_like(p) for p in self.parameters]
        self.v = [np.zeros_like(p) for p in self.parameters]
        self.beta1 = 0.9
        self.beta2 = 0.999
        self.epsilon = 1e-8
        self.iter = 0

    def set_weights(self, layers):
        self.parameters = []
        for i in range(len(layers)):
            self.parameters.append(layers[i])

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
        
        # 处理 nn.Constant 对象
        if hasattr(states, 'data'):
            states = states.data
        elif hasattr(states, 'value'):
            states = states.value
        else:
            states = np.array(states)
            
        if hasattr(Q_target, 'data'):
            Q_target = Q_target.data
        elif hasattr(Q_target, 'value'):
            Q_target = Q_target.value
        else:
            Q_target = np.array(Q_target)
        
        # 确保维度正确
        if states.ndim == 1:
            states = states.reshape(1, -1)
        if Q_target.ndim == 1:
            Q_target = Q_target.reshape(1, -1)
                
        loss = np.mean((self.run(states) - Q_target)**2)
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
        
        # 处理 nn.Constant 对象
        if hasattr(states, 'data'):
            states = states.data
        elif hasattr(states, 'value'):
            states = states.value
        else:
            states = np.array(states)
        
        # 确保是二维数组
        if states.ndim == 1:
            states = states.reshape(1, -1)
        
                
        w1, b1, w2, b2 = self.parameters
        mid_result = states @ w1 + b1
        mid_result = np.maximum(mid_result, 0)
        result = mid_result @ w2 + b2
        return np.array(result)
        

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
        # 处理 nn.Constant 对象
        if hasattr(states, 'data'):
            states = states.data
        elif hasattr(states, 'value'):
            states = states.value
        else:
            states = np.array(states)
            
        if hasattr(Q_target, 'data'):
            Q_target = Q_target.data
        elif hasattr(Q_target, 'value'):
            Q_target = Q_target.value
        else:
            Q_target = np.array(Q_target)
        
        # 确保维度正确
        if states.ndim == 1:
            states = states.reshape(1, -1)
        if Q_target.ndim == 1:
            Q_target = Q_target.reshape(1, -1)
        
        
        states = np.array(states)  # 转成 ndarray
        self.iter += 1
        Q_cal = self.run(states)
        
        batch_size = states.shape[0]
        dL_dz2 = 2 * (Q_cal - Q_target) / batch_size
        
        w1, b1, w2, b2 = self.parameters
        z1 = states @ w1 + b1
        a1 = np.maximum(z1, 0)
        
        dL_dw2 = a1.T @ dL_dz2
        dL_db2 = np.sum(dL_dz2, axis=0)
        
        dz1 = dL_dz2 @ w2.T
        dz1[z1 <= 0] = 0
        dL_dw1 = states.T @ dz1
        dL_db1 = np.sum(dz1, axis=0)
        
        grads = [dL_dw1, dL_db1, dL_dw2, dL_db2]
        
        for i in range(len(self.parameters)):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * grads[i]
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * (grads[i] ** 2)
            m_hat = self.m[i] / (1 - self.beta1 ** self.iter)
            v_hat = self.v[i] / (1 - self.beta2 ** self.iter)
            self.parameters[i] -= self.learning_rate * m_hat / (np.sqrt(v_hat) + self.epsilon)
        
        
        
