import math
import numpy as np
from typing import Dict, Set, Union, List


class BanditReward:

    def __init__(self, rwd):
        self.rwd = [rwd]
        self.n = 1

    def update_reward(self, new_rwd):
        self.rwd.append(new_rwd)
        self.n += 1

    @property
    def mean_reward(self):
        return np.mean(self.rwd)

    @property
    def all_rewards(self):
        return self.rwd


class Bandit:
    def __init__(self, explored_arms: Dict[str, BanditReward], unexplored_sentences: Set[str]):
        self.explored_arms = explored_arms
        self.unexplored_sentences = unexplored_sentences
        self.__name__ = 'Bandit'
        self.total_selections = 0

    def choose_arms_ucb(self, p: int) -> Dict[str, Dict[str, Union[float, str]]]:
        ucb_values = {}

        # Calculate UCB for explored arms
        for sentence, reward_data in self.explored_arms.items():
            mean_reward = reward_data.mean_reward
            ucb_value = mean_reward + math.sqrt((2 * math.log(self.total_selections + 1)) / reward_data.n)
            ucb_values[sentence] = ucb_value

        # Encourage exploration of unexplored arms by assigning them a high UCB value
        for sentence in self.unexplored_sentences:
            # Use a very high UCB value to encourage exploration
            ucb_values[sentence] = 1E+10

        # Sort all sentences by their UCB values in descending order and select the top p
        sorted_sentences = sorted(ucb_values, key=ucb_values.get, reverse=True)[:p]

        # Update total selections and move selected unexplored sentences to explored if they are chosen
        self.total_selections += p
        selected_arms_info = {}
        for sentence in sorted_sentences:
            if sentence in self.unexplored_sentences:
                self.unexplored_sentences.remove(sentence)
                self.explored_arms[sentence] = BanditReward(0)  # Initialize with a placeholder reward

            predicted_reward = self.explored_arms[sentence].mean_reward
            ucb_value = ucb_values[sentence]
            arm_type = 'Exploration' if ucb_value == float('inf') else 'Exploitation'
            selected_arms_info[sentence] = {'predicted_reward': predicted_reward, 'ucb_value': ucb_value, 'type': arm_type}

        return selected_arms_info

    def update_model(self, new_sentences: Set[str], new_rewards: List[float]):
        self.unexplored_sentences = self.unexplored_sentences.difference(new_sentences)
        for sen, rwd in zip(new_sentences, new_rewards):
            known_sen_rwd = self.explored_arms.get(sen, None)
            if not known_sen_rwd:
                self.explored_arms[sen] = BanditReward(rwd)
            else:
                self.explored_arms[sen].update_reward(rwd)

    def update_unexplored(self, new_sentences: Set[str]):
        # Update the unexplored sentences
        self.unexplored_sentences = self.unexplored_sentences.union(new_sentences)

    @property
    def explored_arms_rwds(self) -> Dict[str, float]:
        return {sen: ban_rwd.mean_reward for sen, ban_rwd in self.explored_arms.items()}
