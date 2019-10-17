import unittest
from tilegameproblem import TileGame
from dgraph import DGraph
from search import bfs, dfs, ids, astar, bds, tilegame_heuristic


class IOTest(unittest.TestCase):
    """
    Tests IO for search implementations. Contains basic/trivial test cases.

    Each test function instantiates a search problem (TileGame) and tests if the three test case
    contains the solution, the start state is in the solution, the end state is in the
    solution and, if applicable, if the length of the solutions are the same.

    These tests are not exhaustive and do not check if your implementation follows the
    algorithm correctly. We encourage you to create your own tests as necessary.
    """

    def _check_algorithm(self, algorithm):
        simple_state = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
        # Construct a TileGame where the start and goal states are the same
        tg = TileGame(3, simple_state, simple_state)
        path = algorithm(tg)
        self.assertEqual(
            path[0], simple_state, "Path should start with the start state"
        )
        self.assertEqual(path[-1], simple_state, "Path should end with the goal state")
        self.assertEqual(len(path), 1, "Path length should be one")

    def _simple_problem(self, algorithm, shortest):
        simple_problem = ((1, 2), (4, 3))
        goal_state = ((1, 2), (3, 4))
        # Construct a small TileGame one state away from the goal
        tg = TileGame(2, simple_problem, goal_state)
        path = algorithm(tg)
        self.assertEqual(
            path[0], simple_problem, "Path should start with the start state"
        )
        self.assertEqual(path[-1], goal_state, "Path should end with the goal state")
        if shortest:
            self.assertEqual(len(path), 2, "Path length should be two")

    def _check_dgraph(self, algorithm):
        # Construct a small DGraph one state away from the goal
        dg = DGraph([[None, 1], [1, None]], {1})
        path = algorithm(dg)
        self.assertEqual(path[0], 0, "Path should start with the start state")
        self.assertEqual(path[-1], 1, "Path should end with the goal state")
        self.assertEqual(len(path), 2, "Path length should be two")

    def test_bfs(self):
        self._check_algorithm(bfs)
        self._simple_problem(bfs, True)
        self._check_dgraph(bfs)

    def test_dfs(self):
        self._check_algorithm(dfs)
        self._simple_problem(dfs, False)
        self._check_dgraph(dfs)

    def test_bds(self):
        goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
        goal_state_small = ((1, 2), (3, 4))
        self._check_algorithm(lambda p: bds(p, goal_state))
        self._simple_problem(lambda p: bds(p, goal_state_small), True)
        self._check_dgraph(lambda p: bds(p, 1))

    def test_ids_output(self):
        self._check_algorithm(ids)
        self._simple_problem(ids, True)
        self._check_dgraph(ids)

    def test_astar_output(self):
        self._check_algorithm(lambda p: astar(p, lambda s: 0))
        self._simple_problem(lambda p: astar(p, lambda s: 0), True)
        self._check_dgraph(lambda p: astar(p, lambda s: 0))


if __name__ == "__main__":
    unittest.main()
