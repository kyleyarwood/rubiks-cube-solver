from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor, QIcon, QPixmap
from colour import Colour
from solver import Solver
from cube import Cube

class App(QWidget):
    def __init__(self):
        self.width = 1440
        self.height = 720
        self.WINDOW_WIDTH = 8
        self.WINDOW_BAR_HEIGHT = 23+7
        self.selected_colour = Colour.W
        self.colour_lists = [['red', 'white', 'blue'], ['orange', 'yellow', 'green']]
        self.colour_map = {Colour.Y: "yellow", 
                    Colour.W: "white", 
                    Colour.G: "green",
                    Colour.B: "blue",
                    Colour.R: "red",
                    Colour.O: "orange"}
        super().__init__()
        self.window = QWidget(self)
        self.twoDCubeMapLayoutLabels = []
        self.colourSelectorLayoutLabels = []
        self.selectedColourLabel = None
        self.solution = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Rubik's Cube Solver")
        self.setGeometry(0, 0, self.width, self.height)
        self.window.setFocus()
        self.window.setLayout(self.init_layout())
        self.show()

    def init_layout(self):
        overall_layout = QVBoxLayout()
        layout = QHBoxLayout()
        layout.setSpacing(200)
        layout.addLayout(self.twoDCubeMapLayout())
        layout.addLayout(self.colourSelectorLayout())
        layout.addLayout(self.selectedColourLayout())
        overall_layout.addLayout(layout)
        overall_layout.addWidget(self.solve_button())

        solution_widget = self.get_solution_widget()
        if solution_widget is not None:
            overall_layout.addWidget(solution_widget)
        return overall_layout

    def selectedColourLayout(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        le = QLineEdit()#readOnly=True)
        le.setText("SELECTED COLOUR:")
        layout.addWidget(le)
        label = QLabel(self)
        pixmap = QPixmap('../img/white.png')
        pixmap = pixmap.scaledToHeight(60).scaledToWidth(60)
        label.setPixmap(pixmap)
        layout.addWidget(label)
        self.selectedColourLabel = label
        return layout

    def solve_button(self):
        button = QPushButton("Solve")
        button.clicked.connect(self.solve_puzzle)
        return button

    def solve_puzzle(self):
        solver = Solver(cube=Cube(self.get_cube_state()))
        solution = solver.solve()
        self.solution.setText(' '.join(solution))
        self.window.repaint()

    def get_cube_state(self):
        cube_state = [[[None for i in range(3)] for j in range(3)] for k in range(6)]
        for i,piece in enumerate(self.twoDCubeMapLayoutLabels):
            if 0 <= i < 9:
                cube_state[1][i%3][i//3] = piece[5]
            elif 9 <= i < 45:
                k = (i-9)%12
                if 0 <= k < 3:
                    cube_state[0][k][(i-9)//12] = piece[5]
                elif 3 <= k < 6:
                    cube_state[2][k-3][(i-9)//12] = piece[5]
                elif 6 <= k < 9:
                    cube_state[4][k-6][(i-9)//12] = piece[5]
                else:
                    cube_state[5][k-9][(i-9)//12] = piece[5]
            else:
                cube_state[3][i%3][(i-45)//3] = piece[5]
            
        return cube_state


    def get_solution_widget(self):
        self.solution = QLineEdit()
        self.solution.setText("Solution will show here.")
        return self.solution

    def colourSelectorLayout(self):
        layout = QHBoxLayout()
        layout.setSpacing(10)
        horiz_gap,vert_gap,start_i,start_j = 70,170,581,50
        cube_dim=60
        reverse_colour_map = {name: colour for colour,name in self.colour_map.items()}
        for i,colour_list in enumerate(self.colour_lists):
            vlayout = QVBoxLayout()
            vlayout.setSpacing(10)
            for j,colour in enumerate(colour_list):
                label = QLabel(self)
                pixmap = QPixmap('../img/' + colour + '.png')
                pixmap = pixmap.scaledToHeight(60).scaledToWidth(60)
                label.setPixmap(pixmap)
                vlayout.addWidget(label)
                self.colourSelectorLayoutLabels.append(
                    [label,
                    start_i+i*(horiz_gap),
                    start_j+j*(vert_gap),
                    start_i+i*(horiz_gap)+cube_dim,
                    start_j+j*(vert_gap)+cube_dim,
                    reverse_colour_map[colour]]
                )
            layout.addLayout(vlayout)
        return layout

    def twoDCubeMapLayout(self):
        layout = QHBoxLayout()
        layout.setSpacing(2)
        cube_width = cube_height = 40
        gap = 2
        for i in range(9):
            vlayout = QVBoxLayout()
            vlayout.setSpacing(2)
            for j in range(12):
                label = QLabel(self)
                pixmap = QPixmap('../img/black.png') if 3<=i<6 or 3<=j<6 else QPixmap('../img/grey.png')
                if 3 <= i < 6 or 3 <= j < 6:
                    self.twoDCubeMapLayoutLabels.append(
                        [label,
                        i*(cube_width+gap)+self.WINDOW_WIDTH,
                        j*(cube_height+gap)+self.WINDOW_WIDTH,
                        i*(cube_width+gap)+cube_width+self.WINDOW_WIDTH,
                        j*(cube_height+gap)+cube_height+self.WINDOW_WIDTH,
                        None])
                pixmap = pixmap.scaledToHeight(40).scaledToWidth(40)
                label.setPixmap(pixmap)
                vlayout.addWidget(label)
            layout.addLayout(vlayout)
        return layout

    def mouseReleaseEvent(self, event):
        if event.button() != 1:
            return
        cursor_pos,window_pos = QCursor().pos(), self.pos()
        print(cursor_pos, window_pos)
        i = self.get_cube_piece_label(cursor_pos, window_pos)
        if i is not None:
            self.set_cube_piece_colour(i)
            return
        colour = self.get_colour_selection(cursor_pos, window_pos)
        if colour is not None:
            self.set_selected_colour(colour)

    def get_colour_selection(self, cursor_pos, window_pos):
        x_rel = cursor_pos.x() - window_pos.x() - self.WINDOW_WIDTH
        y_rel = cursor_pos.y() - window_pos.y() - self.WINDOW_BAR_HEIGHT
        for label in self.colourSelectorLayoutLabels:
            print(label)
            if label[1] <= x_rel <= label[3] and label[2] <= y_rel <= label[4]:
                return label[5]
        return None

    def set_cube_piece_colour(self, i):
        pixmap = QPixmap('../img/' + self.colour_map[self.selected_colour] + '.png')
        pixmap = pixmap.scaledToHeight(40).scaledToWidth(40)
        self.twoDCubeMapLayoutLabels[i][0].setPixmap(pixmap)
        self.twoDCubeMapLayoutLabels[i][5] = self.selected_colour
        self.window.repaint()

    def get_cube_piece_label(self, cursor_pos, window_pos):
        x_rel = cursor_pos.x() - window_pos.x() - self.WINDOW_WIDTH
        y_rel = cursor_pos.y() - window_pos.y() - self.WINDOW_BAR_HEIGHT
        for i,label in enumerate(self.twoDCubeMapLayoutLabels):
            if label[1] <= x_rel <= label[3] and label[2] <= y_rel <= label[4]:
                print(i)
                return i
        return None

    def set_selected_colour(self, colour):
        self.selected_colour = colour
        pixmap = QPixmap("../img/" + self.colour_map[colour] + ".png")
        pixmap = pixmap.scaledToWidth(60).scaledToHeight(60)
        self.selectedColourLabel.setPixmap(pixmap)
        self.window.repaint()
