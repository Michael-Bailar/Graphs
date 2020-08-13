"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        # Add a vertex to the graph.
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        # Add a directed edge to the graph.
        self.vertices[v1].add(v2)

    def get_neighbors(self, vertex_id):
        # Get all neighbors (edges) of a vertex.
        neighbors_list = []
        for item in self.vertices[vertex_id]:
            neighbors_list.append(item)
        return neighbors_list
        
    def bft(self, starting_vertex):
        # create an empty queue and enqueue the starting vertex
        q = Queue()
        q.enqueue(starting_vertex)

        # create a set to store the visited vertices
        visited = set()

        # while the queue is not empty
        while q.size() > 0:
            # dequeue the first vertex
            v = q.dequeue()

            # if the vertex has not been visited
            if v not in visited:
                # mark the vertex as visited
                visited.add(v)
                # print the vertex
                print(v)

                # add all of it's neigbors to the queue
                for next_vertex in self.get_neighbors(v):
                    q.enqueue(next_vertex)


    def dft(self, starting_vertex):
        # create an empty queue and enqueue the starting vertex
        s = Stack()
        s.push(starting_vertex)

        # create a set to store the visited vertices
        visited = set()

        # while the queue is not empty
        while s.size() > 0:
            # dequeue the first vertex
            v = s.pop()

            # if the vertex has not been visited
            if v not in visited:
                # mark the vertex as visited
                visited.add(v)
                # print the vertex
                print(v)

                # add all of it's neigbors to the queue
                for next_vertex in self.get_neighbors(v):
                    s.push(next_vertex)

    def dft_recursive(self, starting_vertex, visited=None):
        if visited is None:
            visited = set()

        visited.add(starting_vertex)
        print(starting_vertex)

        for v in self.get_neighbors(starting_vertex):
            if v not in visited:
                self.dft_recursive(v, visited)

        # s = Stack()
        # visited = set()

        # def dft(vertex):
        #     print(vertex)
        #     visited.add(vertex)
        #     for neighbor in self.get_neighbors(vertex):
        #         if neighbor not in visited:
        #             s.push(neighbor)
        #         if s.size() > 0:
        #             next_vertex = s.pop()  
        #             dft(next_vertex)

        dft(starting_vertex) 

    def bfs(self, starting_vertex, destination_vertex):
        # Return a list containing the shortest path from starting_vertex to
        # destination_vertex in breath-first order.
        # create an empty queue and enqueue PATH to the starting vertex ID
        q = Queue()
        q.enqueue([starting_vertex])
        # create a set to store visited vertices
        visited = set()

        # while the queue is not empty
        while q.size() > 0:
            # dequeu the first PATH
            path = q.dequeue()
            # grab the last vertex from the path
            v = path[-1]
            # check if the vertex has not been visited
            if v not in visited:
                # is this vertex the target?
                if v == destination_vertex:
                    # return the path
                    return path
                # mark it as visited
                visited.add(v)

                # then add a Path to it's neighbors to the back of the queue
                for next_vertex in self.get_neighbors(v):
                    if next_vertex not in visited:
                        # make a copy of the path
                        new_path = path.copy()
                        # append the neighbor to the back of the path
                        new_path.append(next_vertex)
                        # enqueue out the new path
                        q.enqueue(new_path)
        return None

    def dfs(self, starting_vertex, destination_vertex):
        # Return a list containing a path from starting_vertex to destination_vertex
        # in depth-first order.
        # create an empty stack and enqueue PATH to the starting vertex ID
        s = Stack()
        s.push([starting_vertex])
        # create a set to store visited vertices
        visited = set()

        # while the stack is not empty
        while s.size() > 0:
            # pop the first PATH
            path = s.pop()
            # grab the last vertex from the path
            v = path[-1]
            # check if the vertex has not been visited
            if v not in visited:
                # is this vertex the target?
                if v == destination_vertex:
                    # return the path
                    return path
                # mark it as visited
                visited.add(v)

                # then add a Path to it's neighbors to the top of the stack
                for next_vertex in self.get_neighbors(v):
                    if next_vertex not in visited:
                        # make a copy of the path
                        new_path = path.copy()
                        # append the neighbor to the back of the path
                        new_path.append(next_vertex)
                        # push in the new path
                        s.push(new_path)
        return None

    def dfs_recursive(self, starting_vertex, destination_vertex):
        # Return a list containing a path from starting_vertex to destination_vertex
        # in depth-first order.
        # This should be done using recursion.
        s = Stack()
        visited = set()

        def dft(path, destination_vertex):
            v = path[-1]
            if v == destination_vertex:
                print(path)
                return(path)
            else:
                visited.add(v)
                for neighbor in self.get_neighbors(v):
                    if neighbor not in visited:
                        new_path = path.copy()
                        new_path.append(neighbor)
                        s.push(new_path)
                    if s.size() > 0:
                        next_path = s.pop()
                        dft(next_path, destination_vertex)
            return None
        dft([starting_vertex], destination_vertex)
        return None

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    # print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    # print("bft")
    # graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    # print("dft")
    # graph.dft(1)
    # print("recurse")
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    # print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    # print(graph.dfs(1, 6))
    # print(graph.dfs_recursive(1, 6))
