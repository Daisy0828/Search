# NOTE TO STUDENT: Please read the handout before continuing.

from tilegameproblem import TileGame
from dgraph import DGraph
from tarray import TArray
from queue import Queue, LifoQueue, PriorityQueue


### GENERAL SEARCH IMPLEMENTATIONS - NOT SPECIFIC TO THE TILEGAME PROBLEM ###
class Node:
    def __init__(self, state, path_cost, parent = None):
        self.__state = state
        if parent == None:
            self.__parent = None
        else:
            self.__parent = parent
        self.__path_cost = path_cost
    def get_state(self):
        return self.__state
    def get_parent(self):
        return self.__parent
    def get_path_cost(self):
        return self.__path_cost

def bfs(problem):
    """
    Implement breadth-first search.

    Input:
        problem - the problem on which the search is conducted, a SearchProblem

    Output: a list of states representing the path of the solution

    """
    result = []
    state = problem.get_start_state()
    node = Node(state, 0)

    if problem.is_goal_state(node.get_state()):
        result.append(node.get_state())
        return result
    frontier = Queue()
    frontier.put(node)
    explored = set()
    goal_found = False
    explored.add(state)

    while not goal_found:
        if frontier.empty():
            break
        node = frontier.get()
        for child_state, one_step_cost in problem.get_successors(node.get_state()).items():
            child = Node(child_state, node.get_path_cost() + one_step_cost, node)
            if child.get_state() not in explored:
                if problem.is_goal_state(child.get_state()):
                    node = child
                    goal_found = True
                    break
                else:
                    frontier.put(child)
                    explored.add(child_state)

    if goal_found:
        while node.get_parent() is not None:
            result.append(node.get_state())
            node = node.get_parent()
        result.append(node.get_state())
        result.reverse()
    return result

def dfs(problem):
    """
    Implement depth-first search.

    Input:
        problem - the problem on which the search is conducted, a SearchProblem

    Output: a list of states representing the path of the solution

    """
    result = []
    state = problem.get_start_state()
    node = Node(state, 0)

    if problem.is_goal_state(node.get_state()):
        result.append(node.get_state())
        return result
    frontier = LifoQueue()
    frontier.put(node)
    explored = set()
    goal_found = False

    while not goal_found:
        if frontier.empty():
            break
        node = frontier.get()
        for child_state, one_step_cost in problem.get_successors(node.get_state()).items():
            child = Node(child_state, node.get_path_cost() + one_step_cost, node)
            if child.get_state() not in explored:
                if problem.is_goal_state(child.get_state()):
                    node = child
                    goal_found = True
                    break
                else:
                    frontier.put(child)
                    explored.add(child_state)

    if goal_found:
        while node.get_parent() is not None:
            result.append(node.get_state())
            node = node.get_parent()
        result.append(node.get_state())
        result.reverse()
    return result

def ids(problem):
    """
    Implement iterative deepening search.

    Input:
        problem - the problem on which the search is conducted, a SearchProblem

    Output: a list of states representing the path of the solution

    """
    depth = 0
    resultList = []


    while True:
        node = Node(problem.get_start_state(), 0)
        explored = {}
        explored[node.get_state()] = depth
        result = dls(problem, node, depth, explored)
        if result is not None:
            node = result
            while node.get_parent() is not None:
                resultList.append(node.get_state())
                node = node.get_parent()
            resultList.append(node.get_state())
            resultList.reverse()
            break

        depth = depth + 1
    return resultList


def dls(problem, node, depth, explored):
    if depth == 0:
        if problem.is_goal_state(node.get_state()):
            return node
        else:
            return None
    elif depth > 0:
        for child_state, one_step_cost in problem.get_successors(node.get_state()).items():
            child = Node(child_state, node.get_path_cost() + one_step_cost, node)
            if child_state not in explored.keys() or depth - 1 > explored[child_state]:
                explored[child_state] = depth - 1
                result = dls(problem, child, depth - 1, explored)
                #explored.pop(child_state)
                if result is not None:
                    return result

        return None

def bfs_helper(node, queue, problem, visited, otherVisited, level):
    if node.get_state() in otherVisited:
        return node, otherVisited[node.get_state()]
    for child_state, one_step_cost in problem.get_successors(node.get_state()).items():
        child = Node(child_state, node.get_path_cost() + one_step_cost, node)
        if child_state not in visited:
            queue.put((child, level+1))
            visited[child_state] = child
    return None, None

def bds(problem, goal):
    """
    Implement bi-directional search.

    The input 'goal' is a goal state (not a search problem, just a state)
    from which to begin the search toward the start state.

    Assume that the input search problem can be thought of as
    an undirected graph. That is, all actions in the search problem
    are reversible.

    Input:
        problem - the problem on which the search is conducted, a SearchProblem
        goal - the goal state, a state

    Output: a list of states representing the path of the solution

    """
    result = []
    state = problem.get_start_state()
    nodeStart = Node(state, 0)
    nodeGoal = Node(goal, 0)
    node = nodeStart

    if problem.is_goal_state(node.get_state()):
        result.append(node.get_state())
        return result
    begin_queue = Queue()
    end_queue = Queue()
    begin_queue.put((nodeStart, 0))
    end_queue.put((nodeGoal, 0))
    begin_dict = {}
    end_dict = {}
    begin_dict[nodeStart.get_state()] = nodeStart
    end_dict[nodeGoal.get_state()] = nodeGoal
    found = False
    (begin_node, begin_level) = begin_queue.get()
    (end_node, end_level) = end_queue.get()
    ans_front_node = None
    ans_end_node = None
    ans_cost = 10000000
    ans_begin_level = 1000000
    ans_end_level = 1000000
    more_begin = True
    more_end = True
    while True:
        if found and not more_end and not more_begin:
            break

        if more_begin:
            ans_front, ans_end = bfs_helper(begin_node, begin_queue, problem, begin_dict, end_dict, begin_level)
            if ans_front is not None:
                if not found:
                    ans_begin_level = begin_level
                    ans_end_level = end_level
                found = True
                this_cost = ans_front.get_path_cost() + ans_end.get_path_cost()
                if this_cost < ans_cost:
                    ans_cost = this_cost
                    ans_front_node = ans_front
                    ans_end_node = ans_end
            if begin_queue.empty():
                more_begin = False
                continue
            (begin_node, begin_level) = begin_queue.get()
            if begin_level > ans_begin_level:
                begin_level -= 1
                more_begin = False

        if more_end:
            ans_end, ans_front = bfs_helper(end_node, end_queue, problem, end_dict, begin_dict, end_level)
            if ans_end is not None:
                if not found:
                    ans_begin_level = begin_level
                    ans_end_level = end_level
                found = True
                this_cost = ans_front.get_path_cost() + ans_end.get_path_cost()
                if this_cost < ans_cost:
                    ans_cost = this_cost
                    ans_front_node = ans_front
                    ans_end_node = ans_end
            if end_queue.empty():
                more_end = False
                continue
            (end_node, end_level) = end_queue.get()
            if end_level > ans_end_level:
                end_level -= 1
                more_end = False

    if not found:
        return result

    node = ans_front_node
    while node is not None:
        result.append(node.get_state())
        node = node.get_parent()
    result.reverse()
    node = ans_end_node.get_parent()
    while node is not None:
        result.append(node.get_state())
        node = node.get_parent()
    return result


def astar(problem, heur):
    """
    Implement A* search.

    The given heuristic function will take in a state of the search problem
    and produce a real number.

    Your implementation should be able to work with any heuristic
    that is for the given search problem (but, of course, without a
    guarantee of optimality if the heuristic is not admissible).

    Input:
        problem - the problem on which the search is conducted, a SearchProblem
        heur - a heuristic function that takes in a state as input and outputs a number

    Output: a list of states representing the path of the solution

    """
    open_dict = {}
    closed_dict = {}
    queue = PriorityQueue()
    current_state = problem.get_start_state()
    node = Node(current_state, 0)
    index = 0
    queue.put((0 + heur(current_state), index, node))
    index += 1
    open_dict[current_state] = node
    #open_set = set()
    #open_set.add(node)
    #closed_set = set()
    found = False
    current = None
    while not queue.empty():
        current = queue.get()[2]
        #current = min(open_set, key=lambda o:o.get_path_cost() + heur(o.get_state()))
        current_state = current.get_state()
        #if current.get_path_cost() != open_dict[current.get_state()].get_path_cost():
            #continue
        if current_state not in open_dict or current.get_path_cost() != open_dict[current_state].get_path_cost():
            continue
        if problem.is_goal_state(current.get_state()):
            found = True
            break
        #open_set.remove(current)
        open_dict.pop(current.get_state())
        closed_dict[current_state] = current
        #closed_set.add(current_state)
        for child_state, one_step_cost in problem.get_successors(current.get_state()).items():
            if child_state in closed_dict:
                continue
            if child_state in open_dict:
                cost = current.get_path_cost() + one_step_cost
                if cost < open_dict[child_state].get_path_cost():
                    child = Node(child_state, cost, current)
                    open_dict[child_state] = child
                    #open_set.add(child)
                    queue.put((cost+heur(child_state), index, child))
                    index += 1
            else:
                cost = current.get_path_cost() + one_step_cost
                child = Node(child_state, cost, current)
                open_dict[child_state] = child
                #open_set.add(child)
                queue.put((cost+heur(child_state), index, child))
                index += 1
    result = []
    if not found:
        return result
    node = current
    while node is not None:
        result.append(node.get_state())
        node = node.get_parent()
    result.reverse()
    return result

### SPECIFIC TO THE TILEGAME PROBLEM ###


def tilegame_heuristic(state):
    """
    Produces a number for the given tile game state representing
    an estimate of the cost to get to the goal state.

    Input:
        state - the tilegame state to evaluate. Consult handout for how the tilegame state is represented

    Output: a number (int, float, etc.)

    """
    list = TileGame.tuple_to_list(state)
    dim = len(list)
    step = 0
    for i in range(dim):
        for j in range(dim):
            correct_i = int((list[i][j] - 1) / dim)
            correct_j = (list[i][j] - 1) % dim
            step += (abs(i - correct_i) + abs(j - correct_j))
    return int(step / 2)


### YOUR SANDBOX ###


def main():
    """
    Do whatever you want in here; this is for you.
    The examples below shows how your functions might be used.
    """

    # initialize a random transition array of length 8

    import time
    t = time.time()
    ta = TArray(9)
    # compute path using bfs
    #bfs_path = bfs(ta)
    #print(len(bfs_path))
    #print(time.time() - t)
    #t = time.time()
    #ta = TileGame(3)
    #pathAStar = astar(ta, tilegame_heuristic)
    #print("Path of A star")
    #TArray.print_path(pathAStar)
    #print(len(pathAStar))
    # display path

    pathBfs = bfs(ta)
    print("Path of BFS")
    TArray.print_path(pathBfs)

    #pathDfs = dfs(ta)
    #print("Path of dFS")
    #TArray.print_path(pathDfs)
    #print(time.time() - t)

    #pathIds = ids(ta)
    #print("Path of IDS")
    #TArray.print_path(pathIds)
    #print(time.time() - t)

    goal_state = (0,1,2,3,4,5,6,7,8)
    pathBds = bds(ta, goal_state)
    print("Path of BDS")
    TArray.print_path(pathBds)
    print(time.time() - t)

    # initialize a random 3x3 TileGame problem
    #simple_problem = ((1,2,3),(4,5,6),(7,8,9))
    goal_state = ((1,2,3),(4,5,6),(7,8,9))
    tg = TileGame(3)
    path = astar(tg, tilegame_heuristic)
    TileGame.print_pretty_path(path)


    #tg = TileGame(3)
    #print(TileGame.board_to_pretty_string(tg.get_start_state()))
    #path = dfs(tg,goal_state)
    #print (path[0])
    # compute path using bds
    #path = bds(tg, ((1,2,3), (4,5,6), (7,8,9)))
    # display path
    #TileGame.print_pretty_path(path)

    # initialize a small DGraph
    #small_dgraph = DGraph([[None, 1], [1, None]], {1})
    # print the path using bfs
    #print(bfs(small_dgraph))

if __name__ == "__main__":
    main()