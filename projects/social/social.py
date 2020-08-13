import random

class User:
    def __init__(self, name):
        self.name = name

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        self.add_friendship_count = 0

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME
        # Add users
        for i in range(0, num_users):
            self.add_user(f"User {i}")

        # Create friendships

        possible_friendships = []

        for user_id in self.users:
            for  friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))

        random.shuffle(possible_friendships)

        N = num_users * avg_friendships // 2
        self.add_friendship_count = N
        print(f"add_friendships() ran {N} times.")
        for i in range(N):
            friendship = possible_friendships[i]
            user_id = friendship[0]
            friend_id = friendship[1]
            self.add_friendship(user_id, friend_id)


    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        q = Queue()
        visited = {}
        q.enqueue([user_id])

        while q.size() > 0:
            path = q.dequeue()
            v = path[-1]

            if v not in visited:
                visited[v] = path

                for friend in self.friendships[v]:
                    path_copy = list(path)
                    path_copy.append(friend)
                    q.enqueue(path_copy)
        return visited
        # q = Queue()
        # initial_user = {user_id: [user_id]}
        # q.enqueue(initial_user)
        

        # while q.size() > 0:
        #     current = q.dequeue()
        #     current_user = list(current.keys())[0]
        #     current_path = list(current.values())[0]
        #     visited[current_user] = current_path
        #     current_friends = self.friendships[current_user]
        #     for friend in current_friends:
        #         if friend not in visited and friend not in q.queue:
        #             q_path = current_path.copy()
        #             q_path.append(friend)
        #             q_user = {friend: q_path}
        #             q.enqueue(q_user)

        
        # return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(1000, 2)
    connections = sg.get_all_social_paths(1)
    print(f"Users in extended social network: {len(connections) -1}")
    total_social_paths = 0
    for user_id in connections:
        total_social_paths += len(connections[user_id])
    print(f"Avg length of social path: {total_social_paths / len(connections) - 1}")
    # print("*****************************************")
    # print(f"add_friendships was called {sg.add_friendship_count} times")
    # # run connections for everyone in the list. then get an average
    # # percent of total users in connections
    # social_path_count_sum = 0
    # degree_of_seperation_count_sum = 0
    # for i in sg.users:
    #     test_connections = sg.get_all_social_paths(i)
    #     paths = len(test_connections)
    #     social_path_count_sum += paths
    #     # final_connection_list = test_connections[paths -1]
    #     # # print(final_connection_list)
    #     # degree_of_seperation_count_sum += degree_of_seperation


  
    # average_social_path_count = social_path_count_sum/len(sg.users)
    # social_path_average_percent = average_social_path_count/len(sg.users)*100
    # print(f"On average, a user's social network includes {social_path_average_percent} percent of total users")
    
    # # average degree of seperation 
    # print("average DOS", degree_of_seperation_count_sum/len(sg.users))
