from scrambler import Scrambler
from cube import Cube
from solver import Solver
from app import App
from PyQt5.QtWidgets import *
from sys import argv

def main():
    """
    solver, scrambler = Solver(), Scrambler()
    scramble_moves = scrambler.generate_scramble_moves()
    print('\n'.join(scramble_moves))
    solver.scramble(scramble_moves)
    print(' '.join(solver.solve()))
    """
    app = QApplication(argv)
    ex = App()
    app.exec_()

if __name__ == "__main__":
    main()
