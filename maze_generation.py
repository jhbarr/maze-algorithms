import pygame
from queue import PriorityQueue
from queue import Queue
from queue import LifoQueue
import math
import random

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
ROWS = 50

if ROWS %2==0:
    ROWS+=1

pygame.display.set_caption("Maze Visualizer")

print(WIDTH/ROWS)

WHITE = (211,211,211)
BLACK = (26, 28, 32)

ORANGE = (240, 165, 0)
GOLD = (207, 117, 0)

RED = (255, 0,0)
GREEN = (0,255,0)

VISITED = []

class Box:
    def __init__(self, row, col, gap, total_rows, set_number):
        self.col = col
        self.row = row
        self.gap = gap
        self.color = BLACK
        self.neighbors = []
        self.total_rows = total_rows
        self.set_number = 0
        self.bottom_connection = 0

    def __lt__(self, other):
        return False

    def get_pos(self):
        return self.row, self.col


    def make_path(self):
        self.color = WHITE
    def make_barrier(self):
        self.color = BLACK
    def make_start(self):
        self.color = ORANGE
    def make_end(self):
        self.color = GOLD
    def make_open(self):
        self.color = GREEN
    def make_closed(self):
        self.color = RED
    def reset(self):
        self.color = WHITE

    def is_start(self):
        return self.color == ORANGE
    def is_end(self):
        return self.color == GOLD
    def is_barrier(self):
        return self.color == BLACK
    def is_path(self):
        return self.color == WHITE


    def get_path_neighbors(self, grid):
        self.neighbors = []

        if (0<=self.col+2<=self.total_rows-2):
            x = grid[self.row][self.col + 2]
            y = grid[self.row][self.col + 1]
            self.neighbors.append([x, y])
            #self.neighbors.append([grid[self.row][self.col+2], "col+2"])


        if (0<=self.col-2<=self.total_rows-2):
            x = grid[self.row][self.col-2]
            y = grid[self.row][self.col-1]
            self.neighbors.append([x, y])
            #self.neighbors.append([grid[self.row][self.col-2], "col-2"])

        if (0<=self.row+2<=self.total_rows-2):
            x=grid[self.row + 2][self.col]
            y = grid[self.row + 1][self.col]
            self.neighbors.append([x, y])
            #self.neighbors.append([grid[self.row+2][self.col], "row+2"])

        if (0<=self.row-2<=self.total_rows-2):
            x = grid[self.row -2][self.col]
            y = grid[self.row -1][self.col]
            self.neighbors.append([x, y])
            #self.neighbors.append([grid[self.row+2][self.col], "row-2"])

        return self.neighbors


    def get_neighbors(self, grid):
        self.neighbors = []

        if (0 <= self.col + 1 <= self.total_rows-1) and grid[self.row][self.col + 1].color != BLACK:
            self.neighbors.append(grid[self.row][self.col + 1])

        if (0 <= self.col - 1 <= self.total_rows-1) and grid[self.row][self.col - 1].color != BLACK:
            self.neighbors.append(grid[self.row][self.col - 1])

        if (0 <= self.row + 1 <= self.total_rows-1) and grid[self.row + 1][self.col].color != BLACK:
            self.neighbors.append(grid[self.row + 1][self.col])

        if (0 <= self.row - 1 <= self.total_rows-1) and grid[self.row - 1][self.col].color != BLACK:
            self.neighbors.append(grid[self.row - 1][self.col])

        return self.neighbors



    def draw(self, win):
        pygame.draw.rect(win, self.color, ((self.row*self.gap, self.col*self.gap, self.gap, self.gap)))




def make_grid(win, width, rows):
    grid = []
    gap = width/rows

    set = 0

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            box = Box(i,j,gap,rows, set)
            grid[i].append(box)

    for i in range(1, rows-1):
        for j in range(1, rows-1):
            grid[i][j].set_number = set
            set+=1
    return grid


def draw_grid(win, rows, width):
    gap = width / rows
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))


def draw(win, width, grid, rows):
    win.fill(BLACK)

    for i in grid:
        for box in i:
            box.draw(win)
    #draw_grid(win,rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width / rows
    y, x = pos

    row = int(y//gap)
    col = int(x//gap)

    return row, col









#-------------------------------------------MAZE GENERATION CODE---------------------------------------


def make_maze(win,width,grid,rows):
    print(grid[1][3].set_number)

    MAIN_STACK = []

    MAIN_STACK.append(grid[1][1])
    grid[1][1].make_path()

    while len(MAIN_STACK) > 0:
        draw(win, width, grid, rows)
        #pygame.time.wait(40)

        current = MAIN_STACK[-1]
        current.make_path()
        neighbors = [n for n in current.get_path_neighbors(grid) if not n[0].is_path()]

        if len(neighbors)==0:
            MAIN_STACK.remove(current)
        else:
            neighbor = random.choice(neighbors)
            n = neighbor[0]
            ns = neighbor[1]

            MAIN_STACK.append(n)
            n.color = RED
            ns.make_path()

    grid[rows-1][rows-2].make_path()
    grid[0][1].make_path()



def make_maze_prims(win,width,grid,rows):

    FRONTIER = []
    FRONTIER.append(grid[1][1])

    while len(FRONTIER) > 0:
        draw(win, width, grid, rows)

        current = random.choice(FRONTIER)
        FRONTIER.remove(current)

        f_neighbors = [n for n in current.get_path_neighbors(grid) if n[0] not in VISITED and n[0] not in FRONTIER]
        v_neighbors = [n for n in current.get_path_neighbors(grid) if n[0] in VISITED]

        if len(v_neighbors) == 0:
            for n in f_neighbors:
                FRONTIER.append(n[0])
                n[0].color = RED
            VISITED.append(current)
            current.make_path()

        else:
            current.make_path()
            VISITED.append(current)

            for n in f_neighbors:
                FRONTIER.append(n[0])
                n[0].color = RED

            v_n = random.choice(v_neighbors)

            v_n[1].make_path()
            VISITED.append(v_n[1])















def make_maze_el(win, width, grid, rows):

    for j in range(1, rows-2):

        set_dict = {}

        for i in range(1, rows-1):
            if j % 2 == 1 and i % 2 == 1:

                s = grid[i][j].set_number
                if s in set_dict:
                    set_dict[s].append(grid[i][j])
                    grid[i][j].color = WHITE
                else:
                    set_dict[s] = [grid[i][j]]
                    grid[i][j].color = WHITE

        for i in range(1, rows-1):
            if j%2==1 and i%2==1:

                draw(win, width, grid, rows)
                pygame.time.wait(60)

                s = grid[i][j].set_number
                grid[i][j].color = WHITE

                try:
                    r = random.randint(0,3)
                    if (r==1 or r==2 or r==3) and grid[i+2][j].set_number != grid[i][j].set_number:

                        set_dict[s].append(grid[i + 2][j])
                        set_dict[grid[i + 2][j].set_number].remove(grid[i + 2][j])

                        for q in set_dict[grid[i+2][j].set_number]:
                            q.set_number = grid[i][j].set_number
                            set_dict[s].append(q)
                            set_dict[grid[i + 2][j].set_number].remove(q)

                        del set_dict[grid[i + 2][j].set_number]
                        grid[i + 2][j].set_number = grid[i][j].set_number


                        #grid[i + 2][j].color = WHITE
                        grid[i + 1][j].color = WHITE

                except:
                    pass

        for i,j in set_dict.items():
            if len(j)==1:
                try:
                    x,y = j[0].get_pos()

                    set_dict[j[0].set_number].append(grid[x][y+2])
                    grid[x][y + 2].set_number = j[0].set_number

                    grid[x][y + 1].color = WHITE
                    grid[x][y + 2].color = WHITE
                except:
                    pass

            else:
                try:
                    l = len(j)-1

                    for i in range(random.randint(1, l)):
                        x,y = j[random.randint(1,l)].get_pos()

                        set_dict[grid[x][y].set_number].append(grid[x][y + 2])
                        grid[x][y + 2].set_number = grid[x][y].set_number

                        grid[x][y + 1].color = WHITE
                        grid[x][y + 2].color = WHITE
                except:
                    pass





def e_support(grid, set_dict, s, i, j):

    set_dict[s].append(grid[i + 2][j])
    set_dict[grid[i + 2][j].set_number].remove(grid[i + 2][j])

    for q in set_dict[grid[i + 2][j].set_number]:
        set_dict[grid[i + 2][j].set_number].remove(q)
        q.set_number = s
        set_dict[s].append(q)

    del set_dict[grid[i + 2][j].set_number]
    grid[i + 2][j].set_number = s

    grid[i + 2][j].color = WHITE
    grid[i + 1][j].color = WHITE


def make_maze_e(win, width, grid, rows):
    for j in range(rows):

        set_dict = {}

        for i in range(rows):
            if j%2==1 and i%2==1:
                s = grid[i][j].set_number

                if s in set_dict:
                    set_dict[s].append(grid[i][j])
                else:
                    set_dict[s] = [grid[i][j]]

        for i in range(1, rows):
            if j%2==1 and i%2==1:

                draw(win, width, grid, rows)
                #pygame.time.wait(60)

                s = grid[i][j].set_number
                grid[i][j].color = WHITE

                try:
                    r = random.randint(0,3)
                    if (r==1 or r==2 or r==3) and (j<rows-2) and grid[i+2][j] not in set_dict[s]:
                        e_support(grid, set_dict, s, i, j)

                    elif j==rows-2 and grid[i+2][j] not in set_dict[s]:
                        e_support(grid, set_dict, s, i, j)
                        #print(set_dict)

                except:
                    pass





        for i in set_dict.values():

            try:
                if len(i)==1:
                    x, y = i[0].get_pos()
                    grid[x][y + 2].set_number = i[0].set_number
                    grid[x][y + 1].color = WHITE

                else:
                    l = len(i)
                    r = random.randint(1, l)

                    choices = [i for i in range(0, l-1)]

                    for q in range(0, r):
                        w = random.choice(choices)
                        x, y = i[w].get_pos()

                        grid[x][y + 2].set_number = grid[x][y].set_number
                        grid[x][y+2].color = WHITE
                        grid[x][y + 1].color = WHITE

                        choices.remove(w)

            except:
                pass




























            #------------------------------------------------MAZE SOLVING CODE--------------------------------------

def map_maze(start_node, end_node, parents, win, grid, width):
    current = end_node
    path_length = 0
    while True:
        if current == start_node:
            break

        if current != start_node:
            parents[current].color = ORANGE
            current = parents[current]
            draw(win, width, grid, ROWS)


        end_node.color = GOLD
        start_node.color = ORANGE
        path_length +=1
    print("Path length: " + str(path_length) + ", Nodes visited: " + str(len([j for i in grid for j in i if j.color == RED]) + path_length))

    for row in grid:
        for box in row:
            if box.color == RED or box.color == GREEN:
                box.color = WHITE

def h(current_pos, ending_pos):
    x = (current_pos[0] - ending_pos[0]) ** 2
    y = (current_pos[1] - ending_pos[1]) ** 2

    return int(math.sqrt(x + y))

def h_algorithm(start_node, end_node, grid, width, win):

    open_list = PriorityQueue()
    open_list.put((0, start_node))

    open_list_dic = {start_node}
    parents = {}

    hScore = {box: h(box.get_pos(), end_node.get_pos()) for row in grid for box in row}

    while not open_list.empty():
        draw(win, 800, grid, ROWS)
        #pygame.time.wait(25)

        current = open_list.get()[1]

        open_list_dic.remove(current)

        neighbors = current.get_neighbors(grid)

        if current == end_node:
            map_maze(start_node, end_node, parents, win, grid, width)
            return

        for n in neighbors:
            if n.color != RED:
                if n not in open_list_dic:
                    parents[n] = current
                    open_list.put((hScore[n], n))

                    open_list_dic.add(n)
                    if n != start_node:
                        n.color = GREEN

        if current != start_node:
            current.color = RED




def b_algorithm(start_node, end_node, grid, width, win):
    open_list = Queue()
    open_list.put(start_node)

    open_list_dic = {start_node}
    parents = {}

    while not open_list.empty():
        draw(win, 800, grid, ROWS)

        current = open_list.get()
        open_list_dic.remove(current)

        neighbors = current.get_neighbors(grid)

        if current == end_node:
            map_maze(start_node, end_node, parents, win, grid, width)
            return True

        for n in neighbors:
            if n.color != RED:
                if n not in open_list_dic:
                    parents[n] = current

                    open_list.put(n)
                    open_list_dic.add(n)
                    if n != end_node:
                        n.color = GREEN

        if current != start_node and current != end_node:
            current.color = RED


def a_algorithm(start_node, end_node, grid, width, win):
    open_list = PriorityQueue()
    open_list.put((0, 0, start_node))

    open_list_dic ={start_node}
    parents = {}

    g_score = {box : float('inf') for row in grid for box in row}
    g_score[start_node] = 0
    f_score = {box : float('inf') for row in grid for box in row}
    f_score[start_node] = h(start_node.get_pos(), end_node.get_pos())

    while not open_list.empty():
        draw(win, 800, grid, ROWS)

        current = open_list.get()[2]
        open_list_dic.remove(current)

        neighbors = current.get_neighbors(grid)

        if current == end_node:
            map_maze(start_node, end_node, parents, win, grid, width)
            return

        for n in neighbors:
            if n.color != RED:
                t_gscore = g_score[current] + 1
                if t_gscore < g_score[n]:
                    g_score[n] = t_gscore
                    f_score[n] = h(n.get_pos(), end_node.get_pos())

                    if n not in open_list_dic:
                        parents[n] = current

                        open_list.put((f_score[n], g_score[n], n))
                        open_list_dic.add(n)
                        if n != end_node:
                            n.color = GREEN

        if current != start_node and current != end_node:
            current.color = RED











#----------------------------------------MAIN CODE---------------------------

def start_pos(grid):
    for x, y in enumerate(grid):
        for a, b in enumerate(y):
            if b.is_start():
                return a, x


def end_pos(grid):
    for x, y in enumerate(grid):
        for a, b in enumerate(y):
            if b.is_end():
                return a, x

maze_created = False

start = None
end = None

started = False
run = True
running = False

grid = make_grid(WIN, WIDTH, ROWS)
while run:
    draw(WIN, WIDTH, grid, ROWS)


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if started:
            continue

        if pygame.mouse.get_pressed()[0] and maze_created:
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, ROWS, WIDTH)

            box = grid[row][col]

            if not start and box != end and not box.is_barrier():
                start = box
                start.make_start()

            elif not end and box != start and not box.is_barrier():
                end = box
                end.make_end()

        elif pygame.mouse.get_pressed()[2] and maze_created:
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, ROWS, WIDTH)

            box = grid[row][col]
            box.reset()
            if box == start:
                start = None
            elif box == end:
                end = None


        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and not maze_created:
                i = random.randint(2,2)
                if i == 1:
                    make_maze(WIN, WIDTH, grid, ROWS)
                else:
                    make_maze(WIN, WIDTH, grid, ROWS)
                maze_created = True

            elif event.key == pygame.K_SPACE and maze_created:

                start = None
                end = None

                for row in grid:
                    for box in row:
                        box.color = BLACK

                VISITED.clear()

                i = random.randint(2,2)
                if i==1:
                    make_maze_e(WIN, WIDTH, grid, ROWS)
                else:
                    make_maze_e(WIN, WIDTH, grid, ROWS)

                running = False



            elif event.key == pygame.K_UP and maze_created and not running:
                started = True

                starting_vert = start_pos(grid)[0]
                starting_hor = start_pos(grid)[1]

                ending_vert = end_pos(grid)[0]
                ending_hor = end_pos(grid)[1]

                start_node = grid[starting_hor][starting_vert]
                end_node = grid[ending_hor][ending_vert]

                h_algorithm(start_node, end_node, grid, WIDTH, WIN)

                running = True
                started = False

            elif event.key == pygame.K_DOWN and maze_created and not running:
                started = True

                starting_vert = start_pos(grid)[0]
                starting_hor = start_pos(grid)[1]

                ending_vert = end_pos(grid)[0]
                ending_hor = end_pos(grid)[1]

                start_node = grid[starting_hor][starting_vert]
                end_node = grid[ending_hor][ending_vert]

                b_algorithm(start_node, end_node, grid, WIDTH, WIN)


                running = True
                started = False

            elif event.key == pygame.K_RIGHT and maze_created and not running:
                started = True

                starting_vert = start_pos(grid)[0]
                starting_hor = start_pos(grid)[1]

                ending_vert = end_pos(grid)[0]
                ending_hor = end_pos(grid)[1]

                start_node = grid[starting_hor][starting_vert]
                end_node = grid[ending_hor][ending_vert]

                a_algorithm(start_node, end_node, grid, WIDTH, WIN)


                running = True
                started = False

            elif event.key == pygame.K_LEFT and maze_created and running:

                for row in grid:
                    for box in row:
                        if box .color == RED or box.color == GREEN or box.color == ORANGE and start_node!=box:
                                box.color = WHITE

                running = False










