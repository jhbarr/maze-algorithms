import pygame
import math
from queue import Queue
from queue import PriorityQueue

import random


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))


RED = (255, 0,0)
GREEN = (0,255,0)
ORANGE =  (240, 165, 0)#(255, 165,0)
TURQUOISE = (207, 117, 0)#(64, 224, 208)
WHITE = (211,211,211)#(255, 255,255)
BLACK = (26, 28, 32)#(0,0,0)
PURPLE = (240, 165, 0) #(147,112,219)

class Spot:

    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.width = width
        self.total_rows = total_rows
        self.neighbors = []


    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN #maybe change the colors

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = GREEN

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width)) #may cause an error tim did win

    def spot_neighbors(self, grid, width):
        #x = row
        #y = col
        self.neighbors = []

        if (0<=self.col+1<=width-1) and grid[self.row][self.col+1].color != BLACK:
            self.neighbors.append(grid[self.row][self.col+1])

        if (0<=self.col-1<=width-1) and grid[self.row][self.col-1].color != BLACK:
            self.neighbors.append(grid[self.row][self.col-1])

        if (0<=self.row+1<=width-1) and grid[self.row+1][self.col].color != BLACK:
            self.neighbors.append(grid[self.row+1][self.col])

        if (0<=self.row-1<=width-1) and grid[self.row-1][self.col].color != BLACK:
            self.neighbors.append(grid[self.row-1][self.col])

        return self.neighbors

    def __lt__(self, other):
        return False






def make_grid(rows, width):
    grid = []
    gap = width / rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, width):
    gap = width / rows
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

def Draw(win, grid, rows, width):
    win.fill(WHITE)


    for row in grid:
        for spot in row:
            spot.draw(win)

    #draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width / rows
    y, x = pos

    row = int(y // gap)
    col = int(x // gap)

    return row, col




#---------------------------------- BFS ALGORITHM CODE -----------------------------------------
"""

def movements(hor, vert, moveset):
    for move in moveset:
        if move=="u":
            vert-=1
        elif move=="d":
            vert+=1
        elif move=="r":
            hor+=1
        elif move=="l":
            hor-=1
    return vert, hor



def check_if_valid(hor, vert, moveset, width, grid):
    vertical_movement = movements(hor, vert, moveset)[0]
    horizontal_movement = movements(hor, vert, moveset)[1]


    if not (0<= vertical_movement <=width-1) or not (0<= horizontal_movement <= width-1):
        return False
    elif grid[horizontal_movement][vertical_movement].color == BLACK:
        return False
    elif grid[horizontal_movement][vertical_movement].color == RED:
        return False
    else:
        if grid[horizontal_movement][vertical_movement].color != ORANGE and grid[horizontal_movement][vertical_movement].color != TURQUOISE:
            grid[horizontal_movement][vertical_movement].make_closed()
        return True



def chek_repitition(movement):
    repeat = ["du", "ud", "rl", "lr"]
    for i in repeat:
        if i in movement:
            return False
    return True


def end_maze_with_queue(hor, vert, moveset, grid, end_hor, end_vert):

    for i in moveset.queue:
        vertical_movement = movements(hor, vert, i)[0]
        horizontal_movement = movements(hor, vert, i)[1]

        if grid[horizontal_movement][vertical_movement] == grid[end_hor][end_vert]:
            return True

    return False


def map_maze(hor, vert, moveset, grid, win, width):
    for move in moveset[:-1]:
        if move=="u":
            vert-=1
        elif move=="d":
            vert+=1
        elif move=="r":
            hor+=1
        elif move=="l":
            hor-=1

        Draw(win, grid, width, 800)
        grid[hor][vert].make_path()




def main_bfs_algorithm(hor, vert, width, grid, end_hor, end_vert, win):
    move_set = Queue()
    move_set.put("")

    t=False
    while t == False:

        Draw(win, grid, width, 800)

        if not end_maze_with_queue(hor, vert, move_set, grid, end_hor, end_vert):
            moves = move_set.get()
            for k in ["u", "d", "r", "l"]:

                if check_if_valid(hor, vert, moves + k, width, grid) and chek_repitition(moves + k):
                    move_set.put(moves + k)
                else:
                    pass

            l = []
            for i in move_set.queue:
                l.append(i)
        else:
            t = True



    final_list = []
    for i in move_set.queue:
        final_list.append(i)

    print(final_list[-1])

    map_maze(hor, vert, final_list[-1], grid, win, width)

"""
def map_b_maze(start_node, end_node, parents, win, grid, width):
    current = end_node
    path_length = 0
    while True:
        if current == start_node:
            break

        if current != start_node:
            parents[current].color = PURPLE
            current = parents[current]
            Draw(win, grid, width, 800)
        start_node.color = ORANGE
        end_node.color = TURQUOISE
        path_length+=1

    print("Path length: " + str(path_length) + ", Nodes visited: " + str(len([j for i in grid for j in i if j.color == RED]) + path_length))


def main_b_algorithm(start_node,end_node, grid, width, win):
    move_set = Queue()
    move_set.put(start_node)

    move_set_list = {start_node}
    parents = {}

    while not move_set.empty():
        Draw(win, grid, width, 800)

        current = move_set.get()
        neighbors = current.spot_neighbors(grid, width)

        if current == end_node:
            map_b_maze(start_node, end_node, parents, win, grid, width)
            return True

        for n in neighbors:
            if n.color != RED:
                if n not in move_set_list:
                    parents[n] = current

                    move_set.put(n)
                    move_set_list.add(n)
                    if n != end_node:
                        n.make_open()

        if current != start_node and current != end_node:
            current.make_closed()




#-------------------------------------------A* ALGORITHM CODE----------------------------------------------

def h(current_pos, ending_pos):
    x = abs(current_pos[0]-ending_pos[0])
    y = abs(current_pos[1]-ending_pos[1])

    return x+y

def map_a_maze(start_node, end_node, parents, win, grid, width):
    current = end_node
    path_length = 0
    while True:
        if current == start_node:
            break

        if current != start_node:
            parents[current].color = PURPLE
            current = parents[current]
            Draw(win, grid, width, 800)
        start_node.color = ORANGE
        end_node.color = TURQUOISE
        path_length+=1

    print("Path length: " + str(path_length) + ", Nodes visited: " + str(len([j for i in grid for j in i if j.color == RED]) + path_length))




def main_a_algorithm(start_node,end_node, grid, width, win):
    count = 0

    open_list = PriorityQueue()
    open_list.put((0, 0, start_node))

    open_list_dic = {start_node}
    parents = {}

    gScore = {spot : float('inf') for row in grid for spot in row}
    gScore[start_node] = 0

    fScore = {spot : float('inf') for row in grid for spot in row}
    fScore[start_node] = h(start_node.get_pos(), end_node.get_pos())



    while not open_list.empty():
        Draw(win, grid, width, 800)

        current = open_list.get()[2]
        open_list_dic.remove(current)


        neighbors = current.spot_neighbors(grid, width)

        if current == end_node:
            map_a_maze(start_node, end_node, parents, win, grid, width)
            return True

        for n in neighbors:
            t_gScore = gScore[current] + 1
            if t_gScore < gScore[n]:
                gScore[n] = t_gScore
                fScore[n] = t_gScore + h(n.get_pos(), end_node.get_pos())

                if n not in open_list_dic:
                    parents[n] = current
                    count +=1

                    open_list.put((fScore[n], gScore[n], n))
                    open_list_dic.add(n)
                    n.make_open()


        if current != start_node:
            current.make_closed()






#------------------------------------------HUERISTIC ONLY ALGORITHM CODE-------------------------------------

def h2(current_pos, ending_pos):
    x = (current_pos[0] - ending_pos[0])**2
    y = (current_pos[1] - ending_pos[1]) ** 2


    return int(math.sqrt(x+y))



def map_h_maze(start_node, end_node, parents, win, grid, width):
    current = end_node
    path_length = 0
    while True:
        if current == start_node:
            break

        if current != start_node:
            parents[current].color = PURPLE
            current = parents[current]
            Draw(win, grid, width, 800)
        end_node.color = TURQUOISE
        start_node.color = ORANGE
        path_length +=1

    print("Path length: "+ str(path_length) + ", Nodes visited: "+ str(len([j for i in grid for j in i if j.color == RED])+path_length))


def main_h_algorithm(start_node,end_node, grid, width, win):
    count = 0

    open_list = PriorityQueue()
    open_list.put((0, start_node))

    open_list_dic = {start_node}
    parents = {}

    hScore = {spot : h2(spot.get_pos(), end_node.get_pos()) for row in grid for spot in row}

    while not open_list.empty():
        Draw(win, grid, width, 800)

        current = open_list.get()[1]

        open_list_dic.remove(current)

        neighbors = current.spot_neighbors(grid,width)

        if current == end_node:
            map_h_maze(start_node, end_node, parents, win, grid, width)
            return True

        for n in neighbors:
            if n.color != RED:
                if n not in open_list_dic:
                    parents[n] = current
                    count+=1
                    open_list.put((hScore[n], n))
                    #print(hScore[n], count)

                    open_list_dic.add(n)
                    if n != start_node:
                        n.make_open()
        #print("\n")

        if current != start_node:
            current.make_closed()




#--------------------------------------------------MAIN CODE--------------------------------------------------










def start_pos(grid):
    for x, y in enumerate(grid):
        for a, b in enumerate(y):
            if b.color == ORANGE:
                return a, x


def end_pos(grid):
    for x, y in enumerate(grid):
        for a, b in enumerate(y):
            if b.color == TURQUOISE:
                return a, x




def main(win , width):
    #ROWS = int(input("What is the width: "))
    ROWS = 50

    grid= make_grid(ROWS, width)


    start = None
    end = None

    run = True
    started = False

    running = False

    while run:
        Draw(win, grid, ROWS, width)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if started:
                continue


            """
            for k,i in enumerate(grid): #black borders
                if k ==0 or k == ROWS-1:
                    for j in range(len(i)):
                        grid[k][j].make_barrier()
                else:
                    grid[k][0].make_barrier()
                    grid[k][-1].make_barrier()
            """


            if pygame.mouse.get_pressed()[0]: #left mouse press
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)

                spot = grid[row][col]

                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None





            if event.type == pygame.KEYDOWN:


                if event.key == pygame.K_SPACE and running == False: # algorithm goes here
                    started = True

                    starting_vert = start_pos(grid)[0]
                    starting_hor = start_pos(grid)[1]

                    ending_vert = end_pos(grid)[0]
                    ending_hor = end_pos(grid)[1]

                    start_node = grid[starting_hor][starting_vert]
                    end_node = grid[ending_hor][ending_vert]


                    pygame.display.set_caption("BFS Algorithm")
                    #main_bfs_algorithm(starting_hor, starting_vert, ROWS, grid, ending_hor, ending_vert, win)


                    main_b_algorithm(start_node, end_node, grid, ROWS, win)

                    running = True
                    started = False



                elif event.key == pygame.K_UP and running == False:  # algorithm goes here
                    started = True


                    starting_vert = start_pos(grid)[0]
                    starting_hor = start_pos(grid)[1]

                    ending_vert = end_pos(grid)[0]
                    ending_hor = end_pos(grid)[1]

                    start_node = grid[starting_hor][starting_vert]
                    end_node = grid[ending_hor][ending_vert]

                    pygame.display.set_caption("A* Algorithm")
                    main_a_algorithm(start_node, end_node, grid, ROWS, win)

                    running = True
                    started = False

                elif event.key == pygame.K_DOWN and running == False:  # algorithm goes here
                    started = True

                    starting_vert = start_pos(grid)[0]
                    starting_hor = start_pos(grid)[1]

                    ending_vert = end_pos(grid)[0]
                    ending_hor = end_pos(grid)[1]

                    start_node = grid[starting_hor][starting_vert]
                    end_node = grid[ending_hor][ending_vert]

                    pygame.display.set_caption("Heuristic only Algorithm")
                    Draw(win, grid, ROWS, width)

                    main_h_algorithm(start_node, end_node, grid, ROWS, win)

                    running = True
                    started = False


                elif event.key == pygame.K_LEFT and running == True:

                    for row in grid:
                        for spot in row:
                            if spot.color == RED or spot.color == GREEN or spot.color == PURPLE and start_node!=spot:
                                spot.color = WHITE

                    running = False








    #pygame.quit()

main(WIN, WIDTH)
