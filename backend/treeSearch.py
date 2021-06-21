import numpy as np

class Problem:
	def __init__(self, problem, heuristics, goal):
		self.problem = problem
		self.heuristics = heuristics
		self.goal = goal

	def successor(self, state):
		return self.problem[state]

class Node:
	def __init__(self, problem, parent, state, board_state):
		self.parent = parent
		self.state = state
		self.board_state = board_state
		if parent:
			self.path_cost = parent.path_cost + problem.step_cost(parent.state, state)
			self.depth = parent.depth + 1
		else:
			self.path_cost = 0
			self.depth = 0

class Puzzle(Problem):
	def __init__(self, n):
		self.n = n
		super().__init__(self.makeProblem(), self.generate_heuristics(), self.n_goal())

	def makeProblem(self):
		problem = {}
		for i in range(self.n+1):
			l = int(np.sqrt(self.n+1))
			x = i // l
			y = i % l
			problem[(x,y)] = []
			if x - 1 >= 0:
				problem[(x,y)].append((x-1,y))
			if x + 1 < l:
				problem[(x,y)].append((x+1,y))
			if y - 1 >= 0:
				problem[(x,y)].append((x,y-1))
			if y + 1 < l:
				problem[(x,y)].append((x,y+1))
		return problem

	def generate_heuristics(self):
		heuristics = {}
		for i in range(self.n+1):
			l = int(np.sqrt(self.n+1))
			x = i // l
			y = i % l
			heuristics[(x,y)] = {}
			for j in range(self.n+1):
				x_j = j // l
				y_j = j % l
				if not (x_j == x and y_j == y):
					heuristics[(x,y)][(x_j, y_j)] = np.abs(x - x_j) + np.abs(y - y_j)
		return heuristics

	def step_cost(self, p_state, state):
		return 1

	def n_goal(self):
		board = []
		for i in range(self.n+1):
			l = int(np.sqrt(self.n+1))
			x = i // l
			y = i % l
			board.append((x,y))
		return board

	def generate_puzzle(self):
		board = []
		for i in range(self.n+1):
			l = int(np.sqrt(self.n+1))
			x = i // l
			y = i % l
			board.append((x,y))
		for i in range(self.n*3):
			swap_i = np.random.randint(0, len(self.problem[board[0]]))
			swap = self.problem[board[0]][swap_i]
			for j in range(len(board)):
				if board[j] == swap:
					board[j] = board[0]
					board[0] = swap
					break
		return board

	def print_board(self, node):
		l = int(np.sqrt(self.n+1))
		board = np.zeros((l,l))
		for i in range(len(node.board_state)):
			x, y = node.board_state[i]
			board[x][y] = i
		print(board)
		return None

	# estimated cost
	def est_cost(self, node):
		cost = 0
		# count = 0
		for i in range(len(node.board_state)):
			if node.board_state[i] != self.goal[i]:
				# count += 1
				cost += self.heuristics[node.board_state[i]][self.goal[i]]
		return cost

	def search_square(self, node, new_state):
		new_board_state = node.board_state.copy()
		tmp = new_board_state[0]
		new_board_state[0] = new_state
		for i in range(1, len(new_board_state)):
			if new_board_state[i] == new_state:
				new_board_state[i] = tmp
				return new_board_state

	def goal_test(self, node):
		return node.board_state == self.goal

	# need think over
	def remove_first(self, fringe):
		fringe.sort(key = lambda x: self.est_cost(x) + x.path_cost)
		ret = fringe[0]
		del(fringe[0])
		return ret

def A_search(problem, start):
	if start == None:
		start = problem.generate_puzzle()
		# return None
	fringe = [Node(problem, None, start[0], start)]
	while fringe:
		node = problem.remove_first(fringe)
		print("Traversing {}, depth: {}, estimated cost: {}".format(node.state, node.depth, problem.est_cost(node)+node.path_cost))
		problem.print_board(node)
		if problem.goal_test(node) == True:
			print("Puzzle solved within {} steps!".format(node.path_cost))
			result = []
			n = node
			while n:
				result.append(n.state)
				n = n.parent
			result.reverse()
			print("Puzzle:", start)
			print("Solution:", result)
			return start, result
		for n in problem.successor(node.state):
			new_board_state = problem.search_square(node, n)
			fringe.append(Node(problem, node, n, new_board_state))
	return None, None

if __name__ == '__main__':
	A_search(Puzzle(8), None)
	# A_search(Puzzle(15))
