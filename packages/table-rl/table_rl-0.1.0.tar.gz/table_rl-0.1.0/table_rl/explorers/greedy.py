import numpy as np
from table_rl import explorer


class GreedyExplorer(explorer.Explorer):
    """Explorer that takes the greedy action always.

    Args:
      num_actions: number of actions
    """

    def __init__(self, num_actions):
        self.num_actions = num_actions

    def select_action(self, obs, action_values) -> int:
        best_action_indices = np.flatnonzero(action_values == np.max(action_values))
        action = np.random.choice(best_action_indices)
        return action

    def observe(self, obs, reward, terminated, truncated, training_mode):
        """Select an action.

        Args:
          obs: next state/observation
          reward: reward received
          terminated: bool indicating environment termination
          truncated: bool indicating episode truncation
          training_mode: bool indicating whether the agent is training
        """
        pass