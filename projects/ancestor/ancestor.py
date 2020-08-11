

def earliest_ancestor(ancestors_list, starting_node):
    solution = -1
    graph = Graph()


    for pair in ancestors_list:
        graph.add_node(pair[1], pair[0])
        
    solution_set = graph.dfs(starting_node)
    print(solution_set)
    
    if len(solution_set) > 1:
        path_length = 0
        solution_path = []
        for path in solution_set:
            if len(path) > path_length:
                path_length = len(path)
                solution_path = path
            elif len(path) == path_length:
                if path[-1] < solution_path[-1]:
                    solution_path = path
        solution_array = solution_path
    else:
        solution_array = solution_set[0]

    if len(solution_array) > 1:
        solution = solution_array[-1]
    print("solution: ", solution)
    return solution
    
    


class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)


class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertices(self, vertex_id):
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        self.vertices[v1].add(v2)

    def add_node(self, v1, v2):
        if v1 not in self.vertices:
            self.add_vertices(v1)
        if v2 not in self.vertices:
            self.add_vertices(v2)
        self.vertices[v1].add(v2)

    def get_parents(self, vertex_id):
        parents_list = []
        for item in self.vertices[vertex_id]:
            parents_list.append(item)
        return parents_list

    def dfs(self, starting_vertex):
        s = Stack()
        s.push([starting_vertex])
        visited = set()
        solution_set = []

        while s.size() > 0:
            path = s.pop()
            v = path[-1]
            if v not in visited:
                if len(self.get_parents(v)) < 1:
                    solution_set.append(path)
                visited.add(v)

                for next_vertex in self.get_parents(v):
                    if next_vertex not in visited:
                        new_path = path.copy()
                        new_path.append(next_vertex)
                        s.push(new_path)


        
        return solution_set



if __name__ == '__main__':
    test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
    earliest_ancestor(test_ancestors, 1)
    earliest_ancestor(test_ancestors, 2)
    earliest_ancestor(test_ancestors, 3)
    earliest_ancestor(test_ancestors, 4)
    earliest_ancestor(test_ancestors, 5)
    earliest_ancestor(test_ancestors, 6)
    earliest_ancestor(test_ancestors, 7)
    earliest_ancestor(test_ancestors, 8)
    earliest_ancestor(test_ancestors, 9)
    earliest_ancestor(test_ancestors, 10)
    earliest_ancestor(test_ancestors, 11)