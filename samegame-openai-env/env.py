from enum import Enum
import gym
from gym import spaces
import random
import sys

class Colors(Enum):
    RED = 1
    YELLOW = 2
    BLUE = 3
    GREEN = 4
    PURPLE = 5

class Env(gym.Env):

    def __init__(self, random_seed = 420):
        self.width = 15
        self.height = 15
        self.num_colors = len(Colors)
        self.action_space = spaces.Tuple((spaces.Discrete(self.width), spaces.Discrete(self.height)))
        self.board = [["0" for x in range(self.height)] for y in range(self.height)]
        self._randomize_board(random_seed)
        self.possible_moves = list()

    def _randomize_board(self, random_seed):
        random.seed(random_seed)
        for x in range(self.width):
            for y in range(self.height):
                self.board[x][y] = str(random.randint(1, 5))

    def _collapse(self):
        # collapse downward
        for x in range(self.width):
            col_str = "".join(self.board[x])
            col_str = col_str.replace('0', '')
            col_str = col_str.ljust(self.width, '0')
            self.board[x] = list(col_str)
        # collapse left if column is empty
        x = 0
        while x < self.width:
            if all(elem == "0" for elem in self.board[x]):
                col = self.board.pop(x)
                self.board[self.width - 1] = col
                x -= 1
            x += 1 

    def _is_board_empty(self):
        return all([all(elem == "0" for elem in col) for col in self.board])

    def _is_game_over(self):
        for x in range(self.width):
            for y in range(self.height):
                color = self.board[x][y]
                if color is "0":
                    break
                # check above
                if y + 1 < self.height and self.board[x][y+1] == color:
                    return False
                # check right
                if x + 1 < self.width and self.board[x+1][y] == color:
                    return False 
        return True

    def _aggregate(self, key, adj_dict):
        l = list()
        if key in adj_dict:
            for elem in adj_dict[key]:
                l.append(elem)
                l += self._aggregate(elem, adj_dict)
        return l

    def get_possible_moves(self):
        adj_dict = dict()
        for x in range(self.width):
            for y in range(self.height):
                color = self.board[x][y]
                if color is "0":
                    break
                # check above
                if y + 1 < self.height and self.board[x][y+1] == color:
                    if (x, y) not in adj_dict:
                        adj_dict[(x, y)] = list()
                    adj_dict[(x,y)].append((x, y+1)) 
                # check right
                if x + 1 < self.width and self.board[x+1][y] == color:
                    if (x, y) not in adj_dict:
                        adj_dict[(x, y)] = list()
                    adj_dict[(x,y)].append((x+1, y))
        moves = list()
        covered = set()
        for key in adj_dict:
            if key not in covered:
                l = [key] + self._aggregate(key, adj_dict)
                for elem in l:
                    covered.add(elem)
                moves.append(l)
        return [elem[0] for elem in moves]

    def step(self, action):
        """Take an action in the environment
        Args:
            self: this object
            action: an (x, y) integer tuple specifying the board position to play
        Returns:
            An observation object, the reward for taking the specified action,
            a boolean flag denoting whether or not the game is over, and a dict of
            diagnostic information
        """
        assert self.action_space.contains(action)
        reward = 3
        done = False
        return self._get_obs(), reward, done, {}

    def _get_obs(self):
        """Returns an observation of the current game state

        Args:
            self: this object
        Returns:
            A 15x15 matrix of colors
        """
        return self.board

    def render(self, mode='human'):
        outfile = StringIO() if mode == 'ansi' else sys.stdout
        # top border
        outfile.write('*' * (self.width * 2 + 3) + '\n')
        for y in range(self.height - 1, -1, -1):
            outfile.write('| ')
            for x in range(0, self.width):
                outfile.write(self.board[x][y] + ' ')
            outfile.write('|\n')
        outfile.write('*' * (self.width * 2 + 3) + '\n')