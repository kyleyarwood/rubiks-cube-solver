from scrambler import Scrambler
from cube import Cube
from solver import Solver

def main():
    solver, scrambler = Solver(), Scrambler()
    scramble_moves = scrambler.generate_scramble_moves()
    print('\n'.join(scramble_moves))
    solver.scramble(scramble_moves)
    print(' '.join(solver.solve()))

if __name__ == "__main__":
    main()
