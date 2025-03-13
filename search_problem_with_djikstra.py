from collections import deque

class Problem():
    def __init__(self, knowledge, start_node, end_node):
        self.knowledge = knowledge
        self.start_node = start_node
        self.end_node = end_node

    #retrieving graph
    def get_map(self):
        return self.knowledge

    #retrieving start_node
    def get_startNode(self):
        return self.start_node

    #retrieving end_node
    def get_endNode(self):
        return self.end_node

    #action function mapping
    def actionFunc(self, node, actiontype):
        map = self.get_map()
        if node in map:
            ch_nodes = map[node]
            if(actiontype == "turnLeft"):
                return ch_nodes[0]
            elif(actiontype == "goStraight"):
                return ch_nodes[1]
            else:
                return ch_nodes[2]

   #Depth-First Search Implementation    
    def DFS(self, map, node, reached=None, result=None):
        
        if reached is None:
            reached = set()
        if result is None:
            result = []
        
        reached.add(node)
        result.append(node)

        
        if node == self.get_endNode():
            return result, True
        
        if node.get_action() is not None:
            for action in node.get_action():
                leafnode = self.actionFunc(node, action)
                leafnode.set_parent(node)

                if leafnode not in reached:
                    result_path, found = self.DFS(map, leafnode, reached, result)
                    if found:
                        return result_path, True

        return result, False
  
    #Breadth-First Search Implementation
    def BFS(self, map, node):
        
        reached = set()
        result = []
        queue = deque()
        
        reached.add(node)
        result.append(node)
        queue.append(node)

        while queue:
            node = queue.popleft()

            if node == self.get_endNode():
                return result, True
            
            if node.get_action() is not None:
                for action in node.get_action():
                    leafnode = self.actionFunc(node, action)

                    leafnode.set_parent(node)
                    if leafnode not in reached:
                        reached.add(leafnode)
                        queue.append(leafnode)
                        result.append(leafnode)

                    if leafnode == self.get_endNode():
                        return result, True
        
        return result, False

    def minimum(self, unexplored):
        return min(unexplored, key=unexplored.get)

    def dijkstra(self, map, start_node, end_node):
        unexplored = {node: float('inf') for node in map}
        unexplored[start_node] = 0
        shortest_path = {}

        while unexplored:
            current_node = self.minimum(unexplored)

            if current_node == end_node:
                break

            if map[current_node] is not None:
                for neighbor in map[current_node]:
                    distance = unexplored[current_node] + 1  # Gunakan 1 sebagai bobot default jika tidak ada bobot spesifik
                    if distance < unexplored.get(neighbor, float('inf')):
                        unexplored[neighbor] = distance
                        shortest_path[neighbor] = current_node

            del unexplored[current_node]

        # Rekonstruksi jalur terpendek
        path = []
        node = end_node
        while node in shortest_path:
            path.insert(0, node)
            node = shortest_path[node]
        path.insert(0, start_node)

        return path if path[-1] == end_node else None
    
    def get_ChildNodes(self, method):
        map = self.get_map()
        start_node = self.get_startNode()
        end_node = self.get_endNode()
        if method == "DFS":
            result, status = self.DFS(map, start_node)
        elif method == "BFS":
            result, status = self.BFS(map, start_node)
        elif method == "D":
            result = self.dijkstra(map, start_node, end_node)
            status = result is not None
        else:
            raise ValueError("Metode tidak dikenal")
        return result, status



class Node():
    def __init__(self, state, action):
        self.state = state
        self.action = action
        self.parent = ""
        

    def get_state(self):
        return self.state
    
    def get_parent(self):
        return self.parent

    def set_parent(self, node):
        self.parent = node

    def get_action(self):
        return self.action



def main():
    node_0 = Node("A", ["turnLeft", "goStraight"])
    node_1 = Node("B", ["turnLeft", "goStraight", "turnRight"])
    node_2 = Node("C", ["turnLeft", "goStraight"])
    node_3 = Node("D", None)
    node_4 = Node("E", None)
    node_5 = Node("F", None)
    node_6 = Node("G", None)
    
    
    knowledge = {node_0:[node_1, node_2],
                 node_1:[node_3, node_4, node_5],
                 node_2:[node_5, node_6],
                 node_3:None,
                 node_4:None,
                 node_5:None,
                 node_6:None

                    }
    

    pathFinding = Problem(knowledge, start_node=node_0, end_node=node_5)

    path_list, status = pathFinding.get_ChildNodes(method="D")
    
    if status:
        for pt in path_list:
            print(pt.get_state())
    else:
        print("Target not found")




if __name__ == "__main__":
    main()