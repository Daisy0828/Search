from searchproblem import SearchProblem
import numpy as np

# The transition array search problem, implemented as a SearchProblem
# States are array configurations.
# Read the assignment handout for details.

class TArray(SearchProblem):
    def __init__(self, length):
        self.start_state = TArray.random_start(length)
        self.length = length
    ###### SEARCH PROBLEM IMPLEMENTATION ######

    def get_start_state(self):
        return self.start_state

    def is_goal_state(self, state):
        return state == tuple(np.arange(self.length).tolist())

    def get_successors(self, state):
        successors = [state[::-1]]
        state = list(state)
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                new_state = state.copy()
                temp = new_state[j]
                new_state[j] = new_state[i]
                new_state[i] = temp
                new_state = tuple(new_state)
                successors += [new_state]
        costs = [1 for i in range(len(successors))]
        return dict(list(zip(successors, costs)))

    @staticmethod
    def random_start(length):
        """
        Given the length of the transition array, produces a random start state.
        """
        return tuple(np.random.permutation(length).tolist())

    @staticmethod
    def display_array(state):
        """
        display the array in the state
        """
        return state


    @staticmethod
    def print_path(track_path):
        """
        Takes in a list of arrays and print the path separated by newlines.
        """
        for b in track_path:
            print(TArray.display_array(b))
