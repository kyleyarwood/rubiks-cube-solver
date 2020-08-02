from random import choice

class Scrambler:
    def __init__(self, n=3):
        self.n = n

    def generate_scramble_moves(self, num_moves=None):
        if self.n==3:
            return self.scramble3(num_moves)
        return []

    def scramble3(self, num_moves=None):
        if num_moves is None:
            num_moves = 20
        axes = {'x': ['F', 'B'], 'y': ['U', 'D'], 'z': ['L', 'R']}
        turns = ['', "'", '2']        
        axes_keys = list(axes.keys())

        last_move = ''
        last_axis = last_two_axes = ''
        moves = []
        for i in range(num_moves):
            axis = choice(axes_keys)
            while axis == last_two_axes:
                axis = choice(axes_keys)
            if axis == last_axis:
                last_two_axes = axis
            else:
                last_axis = axis
            move = choice(axes[axis])
            while move == last_move:
                move = choice(axes[axis])
            last_move = move
            moves.append(move + choice(turns))
        return moves
