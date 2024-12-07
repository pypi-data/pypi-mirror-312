from abc import ABCMeta, abstractmethod


class Explorer(object, metaclass=ABCMeta):
    """Abstract explorer."""

    @abstractmethod
    def select_action(self, obs, action_values=None):
        """Select an action.

        Args:
          action_values: np.ndarray of action-values
        """
        raise NotImplementedError()

    def observe(self, obs, reward, terminated, truncated, training_mode):
        """Select an action.

        Args:
          obs: next state/observation
          reward: reward received
          terminated: bool indicating environment termination
          truncated: bool indicating episode truncation
          training_mode: bool indicating whether the agent is training
        """
        raise NotImplementedError()
