import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

N = 50 # size of the grid
np.random.seed(11)
# The whole program supposes that there are not two edges connecting the same vertices
# The vertex of coordinates (i,j) (starting from (0,0)) has the number i*n + j
# Reversely the vertex number x has coordinates (x//n) + (x mod n)
# The type of graph can be changed, but some functions such as get_neighbours should also be updated in consequence

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


def get_neighbours(vertex):
    # Returns the list of neighbours for the vertex of coordinates (i,j)
    i = vertex[0]
    j = vertex[1]
    if i == 0:
        if j == 0:
            return [(i,j+1), (i+1,j)]
        elif j == N - 1:
            return [(0,j-1), (1,j)]
        else:
            return [(i, j-1), (i,j+1), (i+1,j)]
    elif i == N - 1:
        if j == 0:
            return [(i,j+1), (i-1,j)]
        elif j == N - 1:
            return [(i,j-1), (i-1,j)]
        else:
            return [(i, j-1), (i,j+1), (i-1,j)]
    elif j == 0:
        return [(i+1,j), (i-1,j), (i, j+1)]
    elif j == N - 1:
        return [(i+1,j), (i-1,j), (i, j-1)]
    else:
        return [(i-1,j), (i+1,j), (i,j-1), (i, j+1)]
        
def define_neighbours_dic(vertices):
    # Takes the vertices in the form (i,j) in input and returns the dictionnary of its neighbours (in the form (i,j)) 
    dic = {}
    for vertex in vertices:
        dic[vertex] = get_neighbours(vertex)
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
V = [0]
vertices = np.arange(N**2)
vertices_coord = [number_to_coordinates(v) for v in vertices]
neighbours = define_neighbours_dic(vertices_coord)
V = [0]
E = []
new_vertices = []
current_vertex = (0,0)
must_be_erased = False
clean_plot = False

def plot_wilsons_algorithm_online(size_grid = N):
    global vertices, vertices_coord, neighbours, V, E, new_vertices, current_vertex, must_be_erased, clean_plot
    vertices = np.arange(size_grid**2)
    vertices_coord = [number_to_coordinates(v) for v in vertices]
    neighbours = define_neighbours_dic(vertices_coord)
    V = [(3*size_grid)//2]
    E = []
    new_vertices = []
    current_vertex = (0,0)
    fig = plt.figure() # initiates figure
    line, = plt.plot([],[], ls = "-", marker = None) 

    plt.xlim(-1, N+1)
    plt.ylim(-1, N+1)

    must_be_erased = False
    clean_plot = False

    # creates the background
    def init():
        line.set_data([],[])
        return line,
    
    def animate(k):
        global vertices, vertices_coord, neighbours, V, E, new_vertices, current_vertex, must_be_erased, clean_plot
        if len(V) != len(vertices) :
            if not clean_plot:
                if not must_be_erased :
                    new_vertex = random_walk_step(current_vertex, neighbours)
                    new_vertices.append(coordinates_to_number(new_vertex))
                    plt.plot([current_vertex[0], new_vertex[0]], [current_vertex[1], new_vertex[1]], color = 'red', linestyle = '-')
                    current_vertex = new_vertex
                    if new_vertices[-1] in new_vertices[:-1]:
                        must_be_erased = True
                    elif new_vertices[-1] in V:
                        clean_plot = True
                else:
                    new_vertices = loop_erase(new_vertices)
                    plt.clf()
                    i = len(E)
                    plt.xlim(-1, N+1)
                    plt.ylim(-1, N+1)
                    for j in range(i):
                        plt.plot([v[0] for v in E[j]], [v[1] for v in E[j]], 'b-')
                    coord_new_vertices = [number_to_coordinates(v) for v in new_vertices]
                    plt.plot([v[0] for v in coord_new_vertices], [v[1] for v in coord_new_vertices], color = 'red', linestyle = '-')
                    must_be_erased = False
            else:
                V = V + new_vertices[:-1]
                erased = [number_to_coordinates(v) for v in new_vertices]
                E.append(erased)
                plt.clf()
                i = len(E)
                plt.xlim(-1, N+1)
                plt.ylim(-1, N+1)
                for j in range(i):
                    plt.plot([v[0] for v in E[j]], [v[1] for v in E[j]], 'b-')
                clean_plot = False     
                starting_point = find_starting_point(V, vertices)
                current_vertex = starting_point
                new_vertices = [current_vertex]
                current_vertex = number_to_coordinates(current_vertex)
    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=size_grid**4, blit=False, interval=0, repeat=False)
    plt.show()
                    

plot_wilsons_algorithm_online()