from cube import Cube
from scrambler import Scrambler
from colour import Colour

class Solver:
    def __init__(self, cube=None):
        if cube is None:
            cube = Cube()
        self.cube = cube
        self.move_fns = {"F": self.cube.F,
            "F2": self.cube.F2,
            "F'": self.cube.F_prime,
            "B": self.cube.B,
            "B2": self.cube.B2,
            "B'": self.cube.B_prime,
            "L": self.cube.L,
            "L2": self.cube.L2,
            "L'": self.cube.L_prime,
            "R": self.cube.R,
            "R2": self.cube.R2,
            "R'": self.cube.R_prime,
            "U": self.cube.U,
            "U2": self.cube.U2,
            "U'": self.cube.U_prime,
            "D": self.cube.D,
            "D2": self.cube.D2,
            "D'": self.cube.D_prime,
            "x": self.cube.x,
            "x2": self.cube.x2,
            "x'": self.cube.x_prime,
            "y": self.cube.y,
            "y2": self.cube.y2,
            "y'": self.cube.y_prime,
            "z": self.cube.z,
            "z2": self.cube.z2,
            "z'": self.cube.z_prime}

    def scramble(self, scramble_moves):
        for move in scramble_moves:
            self.move_fns[move]()

    def solve(self):
        solve_moves = self.first_layer()
        solve_moves += self.second_layer()
        solve_moves += self.last_layer()
        print("FINAL STATE:\n\n" + str(self.cube))
        return solve_moves

    def first_layer(self):
        solve_moves = self.white_cross()
        solve_moves += self.corners()
        return solve_moves

    def second_layer(self):
        solve_moves = []
        for c1,c2 in [(Colour.G,Colour.O),(Colour.R,Colour.G),(Colour.B,Colour.R),(Colour.O,Colour.B)]:
            solve_moves.append("y'")
            self.move_fns[solve_moves[-1]]()
            solve_moves += self.edge(c1,c2)
        return solve_moves

    def edge(self, c1, c2):
        solve_moves = []
        if self.is_correct_piece((0,0,1,5,2,1),c2,c1):
            solve_moves += ["F'", "U'", 'F', 'U', 'R', 'U', "R'"]
        elif self.is_correct_piece((0,1,2,3,0,1),c2,c1):
            solve_moves += ["U'", "F'", "U'", 'F', 'U', 'R', 'U', "R'"]
        elif self.is_correct_piece((0,2,1,2,0,1),c2,c1):
            solve_moves += ['U2', "F'", "U'", 'F', 'U', 'R', 'U', "R'"]
        elif self.is_correct_piece((0,1,0,1,0,1),c2,c1):
            solve_moves += ['U', "F'", "U'", 'F', 'U', 'R', 'U', "R'"]
        elif self.is_correct_piece((1,0,1,0,1,0),c2,c1):
            solve_moves += ['R', 'U', "R'", "U'", "F'", "U'", 'F']
        elif self.is_correct_piece((1,1,2,2,1,0),c2,c1):
            solve_moves += ["L'", "U'", 'L', 'U', 'F', 'U', "F'", "U'", 'R', 'U', "R'", "U'", "F'", "U'", 'F']
        elif self.is_correct_piece((1,1,0,5,1,0),c2,c1):
            solve_moves += ["B'", 'U', 'B', 'U', 'L', "U'", "L'", "U'", "F'", "U'", 'F', 'U', 'R', 'U', "R'"]
        elif self.is_correct_piece((2,0,1,0,2,1),c2,c1):
            solve_moves += ['U', 'R', 'U', "R'", "U'", "F'", "U'", 'F']
        elif self.is_correct_piece((2,1,0,1,1,2),c2,c1):
            solve_moves += ["L'", "U'", 'L', 'U', 'F', 'U', "F2", "U'", 'F', 'U', 'R', 'U', "R'"]
        elif self.is_correct_piece((3,0,1,0,1,2),c2,c1):
            solve_moves += ['U2', 'R', 'U', "R'", "U'", "F'", "U'", 'F']
        elif self.is_correct_piece((3,1,2,5,1,2),c2,c1):
            solve_moves += ['B', 'U', "B'", "U'", "R'", "U'", 'R', 'U', "F'", "U'", 'F', 'U', 'R', 'U', "R'"]
        elif self.is_correct_piece((3,1,0,2,1,2),c2,c1):
            solve_moves += ['R', 'U', "R'", 'U2', 'R', 'U2', "R'", 'U', "F'", "U'", 'F']
        elif self.is_correct_piece((5,2,1,0,0,1),c2,c1):
            solve_moves += ["U'", 'R', 'U', "R'", "U'", "F'", "U'", 'F']
        elif self.is_correct_piece((5,1,0,1,1,0),c2,c1):
            solve_moves += ["B'", "U'", 'B', 'U', 'L', 'U', "L'", 'U2', 'R', 'U', "R'", "U'", "F'", "U'", 'F']
        elif self.is_correct_piece((5,1,2,3,1,2),c2,c1):
            solve_moves += ["R'", 'U', 'R', 'U', 'B', "U'", "B'", 'U2', "F'", "U'", 'F', 'U', 'R', 'U', "R'"]

        for move in solve_moves:
            self.move_fns[move]()

        return solve_moves

    def last_layer(self):
        solve_moves = self.oll()
        solve_moves += self.pll()
        return solve_moves

    def white_cross(self):
        solve_moves = []
        if self.cube.state[0][1][1] == Colour.W:
            solve_moves.append('x2')
        elif self.cube.state[1][1][1] == Colour.W:
            solve_moves.append("z'")
        elif self.cube.state[2][1][1] == Colour.W:
            solve_moves.append("x'")
        elif self.cube.state[3][1][1] == Colour.W:
            solve_moves.append('z')
        elif self.cube.state[5][1][1] == Colour.W:
            solve_moves.append('x')
        if solve_moves:
            self.move_fns[solve_moves[0]]()

        for colour in [Colour.G, Colour.R, Colour.B, Colour.O]:
            orientation_move = True
            if self.cube.state[1][1][1] == colour:
                solve_moves.append("y'")
            elif self.cube.state[3][1][1] == colour:
                solve_moves.append("y")
            elif self.cube.state[5][1][1] == colour:
                solve_moves.append("y2")
            else:
                orientation_move = False

            if orientation_move:
                self.move_fns[solve_moves[-1]]()

            solve_moves += self.cross_piece(colour)

        return solve_moves

    def cross_piece(self, colour):
        solve_moves = []
        if self.is_correct_piece((4,1,0,1,2,1), colour):
            solve_moves += ['L2', "U'", 'F2']
        elif self.is_correct_piece((4,2,1,5,0,1), colour):
            solve_moves += ['B2', 'U2', 'F2']
        elif self.is_correct_piece((4,1,2,3,2,1), colour):
            solve_moves += ['R2', 'U', 'F2']
        elif self.is_correct_piece((1,2,1,4,1,0), colour):
            solve_moves += ["L'", "F'"]
        elif self.is_correct_piece((1,1,2,2,1,0), colour):
            solve_moves += ["F'"]
        elif self.is_correct_piece((1,0,1,0,1,0), colour):
            solve_moves += ['L', "F'", "L'"]
        elif self.is_correct_piece((1,1,0,5,1,0), colour):
            solve_moves += ['L2', "F'", 'L2']
        elif self.is_correct_piece((2,1,0,1,1,2), colour):
            solve_moves += ["L'", "U'", 'L', 'F2']
        elif self.is_correct_piece((2,0,1,0,2,1), colour):
            solve_moves += ["U'", "R'", 'F', 'R']
        elif self.is_correct_piece((2,1,2,3,1,0), colour):
            solve_moves += ['R', 'U', "R'", 'F2']
        elif self.is_correct_piece((2,2,1,4,0,1), colour):
            solve_moves += ["F'", 'R', 'U', "R'", 'F2']
        elif self.is_correct_piece((3,2,1,4,1,2), colour):
            solve_moves += ['R', 'F']
        elif self.is_correct_piece((3,1,0,2,1,2), colour):
            solve_moves += ['F']
        elif self.is_correct_piece((3,0,1,0,1,2), colour):
            solve_moves += ["R'", 'F', 'R']
        elif self.is_correct_piece((3,1,2,5,1,2), colour):
            solve_moves += ['R2', 'F', 'R2']
        elif self.is_correct_piece((0,2,1,2,0,1), colour):
            solve_moves += ['F2']
        elif self.is_correct_piece((0,1,0,1,0,1), colour):
            solve_moves += ["U'", 'F2']
        elif self.is_correct_piece((0,0,1,5,2,1), colour):
            solve_moves += ['U2', 'F2']
        elif self.is_correct_piece((0,1,2,3,0,1), colour):
            solve_moves += ['U', 'F2']
        elif self.is_correct_piece((5,0,1,4,2,1), colour):
            solve_moves += ['B', 'D', 'R', "D'", "B'"]
        elif self.is_correct_piece((5,1,2,3,1,2), colour):
            solve_moves += ['D', 'R', "D'"]
        elif self.is_correct_piece((5,1,0,1,1,0), colour):
            solve_moves += ["D'", "L'", 'D']
        elif self.is_correct_piece((5,2,1,0,0,1), colour):
            solve_moves += ["B'", 'D', 'R', "D'", 'B']
    
        for move in solve_moves:
            self.move_fns[move]()

        return solve_moves

    def is_correct_piece(self, ids, colour, base_colour=Colour.W):
        return self.cube.state[ids[0]][ids[1]][ids[2]] == base_colour and self.cube.state[ids[3]][ids[4]][ids[5]] == colour

    def corners(self):
        solve_moves = []
        for colour in [Colour.G, Colour.R, Colour.B, Colour.O]:
            solve_moves.append("y'")
            self.move_fns[solve_moves[-1]]()
            solve_moves += self.corner(colour)
        return solve_moves

    def corner(self, colour):
        solve_moves = []
        if self.is_correct_piece((0,0,0,1,0,0), colour):
            solve_moves += ['U2', 'R', 'U2', "R'", "U'", 'R', 'U', "R'"]
        elif self.is_correct_piece((0,0,2,5,2,2), colour):
            solve_moves += ['U', 'R', 'U2', "R'", "U'", 'R', 'U', "R'"]
        elif self.is_correct_piece((0,2,2,3,0,0), colour):
            solve_moves += ['R', 'U2', "R'", "U'", 'R', 'U', "R'"]
        elif self.is_correct_piece((0,2,0,2,0,0), colour):
            solve_moves += ["U'", 'R', 'U2', "R'", "U'", 'R', 'U', "R'"]
        elif self.is_correct_piece((1,0,0,5,2,0), colour):
            solve_moves += ['U2', 'R', 'U', "R'"]
        elif self.is_correct_piece((1,0,2,0,2,0), colour):
            solve_moves += ['R', "U'", "R'"]
        elif self.is_correct_piece((1,2,2,2,2,0), colour):
            solve_moves += ["L'", "U'", 'L', 'U', 'R', "U'", "R'"]
        elif self.is_correct_piece((1,2,0,4,2,0), colour):
            solve_moves += ['L', 'U2', "L'", 'R', 'U', "R'"]
        elif self.is_correct_piece((2,0,0,1,0,2), colour):
            solve_moves += ["U'", 'R', 'U', "R'"]
        elif self.is_correct_piece((2,0,2,0,2,2), colour):
            solve_moves += ["R'", 'F', 'R', "F'"]
        elif self.is_correct_piece((2,2,2,3,2,0), colour):
            solve_moves += ["F'", 'U2', 'F', 'R', 'U2', "R'"]
        elif self.is_correct_piece((2,2,0,4,0,0), colour):
            solve_moves += ['F', 'U', "F'", 'U2', 'R', 'U', "R'"]
        elif self.is_correct_piece((3,0,0,2,0,2), colour):
            solve_moves += ['R', 'U', "R'"]
        elif self.is_correct_piece((3,0,2,0,0,2), colour):
            solve_moves += ['U2', 'R', "U'", "R'"]
        elif self.is_correct_piece((3,2,2,5,0,2), colour):
            solve_moves += ["R'", 'U2', 'R2', "U'", "R'"]
        elif self.is_correct_piece((3,2,0,4,0,2), colour):
            solve_moves += ['R', 'U', "R'", "U'", 'R', 'U', "R'"]
        elif self.is_correct_piece((4,0,0,1,2,2), colour):
            solve_moves += ["L'", "U'", 'L', 'R', 'U', "R'"]
        elif self.is_correct_piece((4,2,2,3,2,2), colour):
            solve_moves += ['B', 'U2', "B'", 'R', "U'", "R'"]
        elif self.is_correct_piece((4,2,0,5,0,0), colour):
            solve_moves += ['L', 'U', "L'", 'U2', 'R', "U'", "R'"]
        elif self.is_correct_piece((5,0,0,1,2,0), colour):
            solve_moves += ["B'", "U'", 'B', 'R', "U'", "R'"]
        elif self.is_correct_piece((5,0,2,4,2,2), colour):
            solve_moves += ['B', 'U', "B'", 'R', 'U', "R'"]
        elif self.is_correct_piece((5,2,2,3,0,2), colour):
            solve_moves += ['U', 'R', 'U', "R'"]
        elif self.is_correct_piece((5,2,0,0,0,0), colour):
            solve_moves += ['R', 'U2', "R'"]

        for move in solve_moves:
            self.move_fns[move]()

        return solve_moves

    def oll(self):
        solve_moves = self.yellow_cross()
        solve_moves += self.yellow_corners()
        return solve_moves

    def yellow_cross(self):
        solve_moves = []
        classification = self.classify(self.cube.state[0])
        if classification=='T':
            "do nothing"
        elif self.cube.state[0][0][1]==Colour.Y and self.cube.state[0][2][1]==Colour.Y:
            solve_moves.append('U')
        elif self.cube.state[0][0][1] == Colour.Y and self.cube.state[0][1][2]==Colour.Y:
            solve_moves.append("U'")
        elif self.cube.state[0][1][2]==Colour.Y and self.cube.state[0][2][1]==Colour.Y:
            solve_moves.append('U2')
        elif self.cube.state[0][2][1]==Colour.Y and self.cube.state[0][1][0]==Colour.Y:
            solve_moves.append('U')

        if classification=='O':
            solve_moves += ['F', 'U', 'R', "U'", "R'", "F'", "U'", 'F', 'R', 'U', "R'", "U'", "F'"]
        elif classification=='B':
            solve_moves += ['F', 'R', 'U', "R'", "U'", "F'"]
        elif classification=='L':
            solve_moves += ['F', 'U', 'R', "U'", "R'", "F'"]

        for move in solve_moves:
            self.move_fns[move]()

        return solve_moves

    def classify(self, face):
        k = sum(face[i][j]==Colour.Y for i,j in [(0,1),(1,2),(2,1),(1,0)])
        if k == 0:
            return 'O'
        if k==2 and (face[1][0]==face[1][2]==Colour.Y or face[0][1]==face[2][1]==Colour.Y):
            return 'B'
        return 'L' if k==2 else 'T'

    def yellow_corners(self):
        solve_moves = []
        corners_oriented = self.get_corners_oriented()
        while corners_oriented != 4:
            if corners_oriented==3:
                return solve_moves
            solve_moves += self.turn_and_perform_oll_alg(corners_oriented)
            corners_oriented = self.get_corners_oriented()
        return solve_moves

    def turn_and_perform_oll_alg(self, corners_oriented):
        solve_moves = []
        if corners_oriented == 1:
            if self.cube.state[0][0][0]==Colour.Y:
                solve_moves.append("U'")
            elif self.cube.state[0][0][2]==Colour.Y:
                solve_moves.append('U2')
            elif self.cube.state[0][2][2]==Colour.Y:
                solve_moves.append('U')
        elif corners_oriented == 2:
            if self.cube.state[0][0][2]==self.cube.state[0][2][0]==Colour.Y:
                solve_moves.append('U')
            elif self.cube.state[0][0][0]==self.cube.state[0][2][0]==Colour.Y:
                solve_moves.append('U')
            elif self.cube.state[0][2][0]==self.cube.state[0][2][2]==Colour.Y:
                solve_moves.append('U2')
            elif self.cube.state[0][2][2]==self.cube.state[0][0][2]==Colour.Y:
                solve_moves.append("U'")
        elif corners_oriented == 3:
            return ['JJJ']
        solve_moves += ['R', 'U', "R'", 'U', 'R', 'U2', "R'"]

        for move in solve_moves:
            self.move_fns[move]()
        return solve_moves

    def get_corners_oriented(self):
        return sum(self.cube.state[0][i][j]==Colour.Y for i,j in [(0,0),(0,2),(2,0),(2,2)])

    def pll(self):
        solve_moves = []
        solve_moves += self.pair_up_sides()
        print("BEFORE SOLVING LAST FACES:\n\n" + str(self.cube))
        solve_moves += self.solve_middle_of_last_faces()
        solve_moves += self.AUF()
        return solve_moves

    def pair_up_sides(self):
        solve_moves = []
        num_paired_up_sides = self.get_num_paired_up_sides()
        while num_paired_up_sides != 4:
            solve_moves += self.pair_up_sides_alg()
            num_paired_up_sides = self.get_num_paired_up_sides()
        return solve_moves

    def get_num_paired_up_sides(self):
        return sum(self.cube.state[i][0][0]==self.cube.state[i][0][2] for i in range(1,4)) + (self.cube.state[5][2][0]==self.cube.state[5][2][2])

    def pair_up_sides_alg(self):
        solve_moves = []
        if self.cube.state[1][0][0]==self.cube.state[1][0][2]:
            solve_moves.append('U')
        elif self.cube.state[2][0][0]==self.cube.state[2][0][2]:
            solve_moves.append('U2')
        elif self.cube.state[3][0][0]==self.cube.state[3][0][2]:
            solve_moves.append("U'")
        solve_moves += ["R'", 'F', "R'", 'B2', 'R', "F'", "R'", 'B2', 'R2']
        for move in solve_moves:
            self.move_fns[move]()
        return solve_moves

    def get_num_last_faces_solved(self):
        return sum(self.cube.state[i][0][0]==self.cube.state[i][0][1] for i in range(1,4)) + (self.cube.state[5][2][0]==self.cube.state[5][2][1])

    def solve_middle_of_last_faces(self):
        solve_moves = []
        num_last_faces_solved = self.get_num_last_faces_solved()
        while num_last_faces_solved != 4:
            solve_moves += self.solve_middle_alg()
            num_last_faces_solved = self.get_num_last_faces_solved()
        return solve_moves

    def solve_middle_alg(self):
        solve_moves = []
        if self.cube.state[5][2][0]==self.cube.state[5][2][1]:
            solve_moves.append('U')
        elif self.cube.state[1][0][0]==self.cube.state[1][0][1]:
            solve_moves.append('U2')
        elif self.cube.state[2][0][0]==self.cube.state[2][0][1]:
            solve_moves.append("U'")
        solve_moves += ['L2', "U'", "F'", 'B', 'L2', 'F', "B'", 'U', 'L2']
        
        for move in solve_moves:
            self.move_fns[move]()
        
        return solve_moves

    def AUF(self):
        solve_moves = []
        if self.cube.state[1][0][0]==Colour.R:
            solve_moves.append('U')
        elif self.cube.state[2][0][0]==Colour.R:
            solve_moves.append('U2')
        elif self.cube.state[3][0][0]==Colour.R:
            solve_moves.append("U'")
        else:
            return []
        self.move_fns[solve_moves[0]]()
        return solve_moves
