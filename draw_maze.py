import matplotlib.pyplot as plt
import numpy as np
import copy

N = 20

np.random.seed(42)

def loop_erase(w):
    if len(w) <= 1 :
        return w
    else:
        first = w[0]
        if first in w[1:]:
            index = w[1:].index(first)
            return loop_erase([first] + w[index + 2:])
        else:
            return [first] + loop_erase(w[1:])

def coordinates_to_number(vertex, size_grid = N):
    # Returns the number corresponding to the vertex of coordinates (i,j)
    i = vertex[0]
    j = vertex[1]
    return size_grid*i+j

def number_to_coordinates(k, size_grid = N):
    # Returns the coordinates coordinates corresponding to a vertex of number k
    return (k//size_grid, k%size_grid)


def get_neighbours(vertex, size_grid = N):
    # Returns the list of neighbours for the vertex of coordinates (i,j)
    i = vertex[0]
    j = vertex[1]
    if i == 0:
        if j == 0:
            return [(i,j+1), (i+1,j)]
        elif j == size_grid - 1:
            return [(0,j-1), (1,j)]
        else:
            return [(i, j-1), (i,j+1), (i+1,j)]
    elif i == size_grid - 1:
        if j == 0:
            return [(i,j+1), (i-1,j)]
        elif j == size_grid - 1:
            return [(i,j-1), (i-1,j)]
        else:
            return [(i, j-1), (i,j+1), (i-1,j)]
    elif j == 0:
        return [(i+1,j), (i-1,j), (i, j+1)]
    elif j == size_grid - 1:
        return [(i+1,j), (i-1,j), (i, j-1)]
    else:
        return [(i-1,j), (i+1,j), (i,j-1), (i, j+1)]
        
def define_neighbours_dic(vertices, size_grid = N):
    # Takes the vertices in the form (i,j) in input and returns the dictionnary of its neighbours (in the form (i,j)) 
    dic = {}
    for vertex in vertices:
        dic[vertex] = get_neighbours(vertex, size_grid = size_grid)
    return dic

def random_walk_step(vertex, neighbours):
    # Returns the vertex obtained after one step of random walk from vertex (i,j)
    i = vertex[0]
    j = vertex[1]
    neighbours_vertex = neighbours[(i,j)]
    return neighbours_vertex[np.random.randint(0, len(neighbours_vertex))]

def find_starting_point(V, vertices, size_grid = N):
    # Returns the starting point x for an iteration of the algorithm with the vertices set V. Supposes that there is a vertex missing in V
    
    for v in vertices:
        if v not in V:
            return v

exits = [[(0,0), (1,0)], [(N-1, N), (N,N)]]

def draw_interior_line(v1, v2, size_grid = N):
    # Takes into argument two vertices and draws the contour corresponding to the path v1 -> v2 (vi corresponds to a square)
    x1, y1 = v1
    x2, y2 = v2
    if x1 == x2: # vertical
        y = max(y1, y2)
        plt.plot([x1, x1 + 1], [y, y], 'b-')
    elif y1 == y2: # horizontal
        x = max(x1, x2)
        plt.plot([x, x], [y1, y1 + 1], 'b-')
            

def wilsons_algorithm(size_grid = N):
    V = [size_grid**2//2]
    E = []
    vertices = np.arange(size_grid**2)
    neighbours = define_neighbours_dic([number_to_coordinates(v, size_grid = size_grid) for v in vertices], size_grid = size_grid)
    current_vertex = find_starting_point(V, vertices, size_grid = size_grid)
    path = [current_vertex]
    current_vertex = number_to_coordinates(current_vertex, size_grid = size_grid)
    while len(V) != len(vertices):
        current_vertex = find_starting_point(V, vertices, size_grid = size_grid)
        path = [current_vertex]
        current_vertex = number_to_coordinates(current_vertex, size_grid = size_grid)
        while path[-1] not in V:
            current_vertex = random_walk_step(current_vertex, neighbours)
            path.append(coordinates_to_number(current_vertex, size_grid = size_grid))
        erased = loop_erase(path)
        V = V + erased[:-1]
        erased = erased[::-1]
        erased = [number_to_coordinates(v, size_grid = size_grid) for v in erased]
        for k in range(len(erased) - 1):
            E.append([erased[k], erased[k+1]])
    return E

def plot_tree(E):
    for e in E:
        plt.plot([v[0] for v in e], [v[1] for v in e], 'b-')
    plt.show()


def draw_maze(E, exits, path = None, size_grid = N):
    for i in range(size_grid):
        for j in range(size_grid):
            neighbours = get_neighbours((i,j), size_grid = size_grid)
            for v in neighbours:
                if ([(i,j), v] not in E) and ([v, (i,j)] not in E):
                    draw_interior_line((i,j), v, size_grid = size_grid)
    for i in range(size_grid):
        for j in [0, size_grid]:
            if ([(i,j),(i+1,j)] not in exits) and ([(i+1,j), (i,j)] not in exits):
                plt.plot([i, i+1], [j,j], 'b-')
            else:
                plt.plot([i, i+1], [j,j], color = 'lime')
    for i in [0,size_grid]:
        for j in range(size_grid):
            if ([(i,j),(i,j+1)] not in exits) and ([(i,j+1), (i,j)] not in exits):
                plt.plot([i, i], [j,j+1], 'b-')
            else:
                plt.plot([i, i], [j,j+1], color = 'lime')
    

    if path is not None:
        squares = copy.copy(path)
        for i in range(len(squares)):
            x1, y1 = squares[i]
            squares[i] = (x1 + 0.5, y1 + 0.5)
        X = [v[0] for v in squares]
        Y = [v[1] for v in squares]
        plt.plot(X,Y, color = 'red', linestyle = '-')



    plt.show()

def find_path_between(v1, v2, E, used_edges, size_grid = N):
    # Depth search 
    if v1 == v2:
        return [v2], True
    else:
        neighbours = get_neighbours(v1, size_grid = size_grid)
        possible = []
        for v in neighbours:
            if ([v, v1] in E) or ([v1, v] in E):
                if [v, v1] not in used_edges and [v1, v] not in used_edges:
                    possible.append(v)
        for v in possible:
            path, finished = find_path_between(v, v2, E, used_edges + [[v, v1], [v1, v]], size_grid = size_grid)
            if finished:
                return [v1] + path, True
        return ["Nothing found"], False
            
        


E = wilsons_algorithm(N)
exits_squares = [(0,0), (N-1, N-1)]
beginning = exits_squares[0]
ending = exits_squares[1]
exits_doors = [[beginning, (beginning[0]+1, beginning[1])], [(ending[0], ending[1] + 1), (ending[0] + 1, ending[1] + 1)]]
path, finished = find_path_between(beginning, ending, E, [])

# To draw the path replace "path = None" by "path"
draw_maze(E, exits_doors, path = None)
