from colour import Colour

"""
0: the top face
1: the left face
2: the front face
3: the right face
4: the bottom face
5: the back face
"""

class Cube:
    def __init__(self, state=None):
        #TODO: validation of state
        if state is None:
            colours = [Colour.W, Colour.O, Colour.G, Colour.R, Colour.Y, Colour.B]
            state = []
            for colour in colours:
                state.append([[colour for i in range(3)] for j in range(3)])
        self.state = state

    def x(self):
        temp = self.state[0]
        self.state[0] = self.state[2]
        self.state[2] = self.state[4]
        self.state[4] = self.state[5]
        self.state[5] = temp
        self.reorientR(3)
        self.reorientL(1)

    def x2(self):
        self.x()
        self.x()

    def x_prime(self):
        for _ in range(3):
            self.x()

    def y(self):
        temp = self.state[2]
        self.state[2] = self.state[3]
        self.state[3] = self.state[5]
        self.reorientR(3)
        self.reorientR(3)
        self.state[5] = self.state[1]
        self.reorientR(5)
        self.reorientR(5)
        self.state[1] = temp
        self.reorientR(0)
        self.reorientL(4)

    def y2(self):
        self.y()
        self.y()

    def y_prime(self):
        for _ in range(3):
            self.y()

    def z(self):
        self.x()
        self.y()
        self.x_prime()

    def z2(self):
        self.z()
        self.z()

    def z_prime(self):
        for _ in range(3):
            self.z()

    def R(self):
        self.reorientR(3)
        for i in range(3):
            temp = self.state[0][i][2]
            self.state[0][i][2] = self.state[2][i][2]
            self.state[2][i][2] = self.state[4][i][2]
            self.state[4][i][2] = self.state[5][i][2]
            self.state[5][i][2] = temp

    def R2(self):
        self.R()
        self.R()

    def R_prime(self):
        for _ in range(3):
            self.R()

    def L(self):
        self.y2()
        self.R()
        self.y2()

    def L2(self):
        self.L()
        self.L()

    def L_prime(self):
        for _ in range(3):
            self.L()
    
    def U(self):
        self.z()
        self.R()
        self.z_prime()

    def U2(self):
        self.U()
        self.U()

    def U_prime(self):
        for _ in range(3):
            self.U()

    def D(self):
        self.x2()
        self.U()
        self.x2()

    def D2(self):
        self.D()
        self.D()

    def D_prime(self):
        for _ in range(3):    
            self.D()

    def F(self):
        self.y_prime()
        self.R()
        self.y()

    def F2(self):
        self.F()
        self.F()

    def F_prime(self):
        for _ in range(3):
            self.F()

    def B(self):
        self.y2()
        self.F()
        self.y2()

    def B2(self):
        self.B()
        self.B()

    def B_prime(self):
        for _ in range(3):
            self.B()

    def reorientR(self, face):
        #corners
        temp = self.state[face][0][0]
        self.state[face][0][0] = self.state[face][2][0]
        self.state[face][2][0] = self.state[face][2][2]
        self.state[face][2][2] = self.state[face][0][2]
        self.state[face][0][2] = temp

        #edges
        temp = self.state[face][0][1]
        self.state[face][0][1] = self.state[face][1][0]
        self.state[face][1][0] = self.state[face][2][1]
        self.state[face][2][1] = self.state[face][1][2]
        self.state[face][1][2] = temp
        

    def reorientL(self, face):
        for _ in range(3):
            self.reorientR(face)

    def swap_columns(self, face):
        for i in range(3):
            self.state[face][i][0],self.state[face][i][2] = self.state[face][i][2],self.state[face][i][0]

    def __str__(self):
        result = []
        s = ' '*3
        s += ('\n' + ' '*3).join(''.join(x.name for x in row) for row in self.state[0])
        result.append(s)
        for row in range(3):
            s = ""
            for face in range(1,4):
                s += ''.join(x.name for x in self.state[face][row])
            result.append(s)
        for face in range(4,6):
            s = ' '*3
            s += ('\n' + ' '*3).join(''.join(x.name for x in row) for row in self.state[face])
            result.append(s)
        return '\n'.join(result)
