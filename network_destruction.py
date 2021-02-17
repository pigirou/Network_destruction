
"""
Created on Tue Apr 14 13:15:52 2020

@author: Pigi
"""
import sys

class Graph:
    neighbours = dict()

    def addEdge(self,u,v):
        if u not in self.neighbours:
            self.neighbours[u] = set()
        self.neighbours[u].add(v)
        if v not in self.neighbours:
            self.neighbours[v] = set()
        self.neighbours[v].add(u)

    def get_max_degree_node(self):
        degree = -1
        id = sys.maxsize
        for node in self.neighbours:
            curDegree = len(self.neighbours[node])
            if curDegree > degree:
                degree = curDegree
                id = node
            elif curDegree == degree and node < id:
                id = node
        return id,degree

    def remove_node(self,node):
        if node in self.neighbours:
            for neighbour in self.neighbours[node]:
                self.neighbours[neighbour].remove(node)
            self.neighbours.pop(node)

    def ball(self,start,radius,border_only):
        # Use BFS like algorithm to calculate ball set
        visited = set()
        visited.add(start)
        queue = [start]
        distance = dict()
        distance[start] = 0
        # Loop until every element in the queue has distance less than the wanted radius or until the queue gets empty
        while len(queue) != 0 and distance[queue[0]] < radius:
            u = queue.pop(0)
            for v in self.neighbours[u]:
                if v not in visited:
                    visited.add(v)
                    distance[v] = distance[u] + 1
                    queue.append(v)
        if border_only:
            ret = []
            for e in distance:
                if distance[e] == radius:
                    ret.append(e)
            return ret
        else:
            return list(distance.keys())

    def collected_influence(self,i,r):
        border_elements = self.ball(i,r,True)
        sum = 0
        for j in border_elements:
            sum += len(self.neighbours[j]) - 1
        return sum * (len(self.neighbours[i]) - 1)

if __name__ == "__main__":
    # Read arguments
    use_simple_destruction = False
    RADIUS = 2 # Default radius
    ok = True
    try:
        if len(sys.argv) == 7:
            if sys.argv[1] == "-c" and sys.argv[2] == "-r":
                use_simple_destruction = True
                RADIUS = int(sys.argv[3])
                num_nodes = int(sys.argv[4])
                input_file = sys.argv[5]
            else:
                print("Usage: python network_destruction.py [-c] [-r RADIUS] num_nodes input_file")
                ok = False
        elif len(sys.argv) == 5:
            if sys.argv[1] == "-r":
                RADIUS = int(sys.argv[2])
                num_nodes = int(sys.argv[3])
                input_file = sys.argv[4]
            else:
                print("Usage: python network_destruction.py [-c] [-r RADIUS] num_nodes input_file")
                ok = False
        elif len(sys.argv) == 4:
            if sys.argv[1] == "-c":
                use_simple_destruction = True
                num_nodes = int(sys.argv[2])
                input_file = sys.argv[3]
            else:
                print("Usage: python network_destruction.py [-c] [-r RADIUS] num_nodes input_file")
                ok = False
        elif len(sys.argv) == 3:
            num_nodes = int(sys.argv[1])
            input_file = sys.argv[2]
        else:
            print("Usage: python network_destruction.py [-c] [-r RADIUS] num_nodes input_file")
            ok = False
    except ValueError:
        print("Usage: python network_destruction.py [-c] [-r RADIUS] num_nodes input_file")
        ok = False
    # If arguments check passed go on
    if ok:
        # Initialize graph
        myGraph = Graph()
        # Read graph's edges input file
        with open(input_file,"r") as input_file_handle:
            for line in input_file_handle:
                ln = line.strip().split(' ')
                u = int(ln[0])
                v = int(ln[-1])
                myGraph.addEdge(u,v)
        if use_simple_destruction:
            for i in range(num_nodes):
                removal = myGraph.get_max_degree_node()
                print(str(removal[0]) + " " + str(removal[1]))
                myGraph.remove_node(removal[0])
        else:
            # Calculate collected influence of all nodes
            CI = dict()
            for node in myGraph.neighbours:
                CI[node] = myGraph.collected_influence(node,RADIUS)
            # Loop
            for i in range(num_nodes):
                # Select the node with the maximum collected influence
                max_node = sys.maxsize
                max_influence = -1
                for node in myGraph.neighbours:
                    influence = CI[node]
                    if influence > max_influence:
                        max_influence = influence
                        max_node = node
                    elif influence == max_influence and max_node > node:
                        max_node = node
                # Get affected nodes
                affected_nodes = myGraph.ball(max_node,RADIUS + 1,False)
                if max_node in affected_nodes:
                    affected_nodes.remove(max_node)
                # Remove that node
                myGraph.remove_node(max_node)
                # Update collected influence of affected nodes
                for affected_node in affected_nodes:
                    CI[affected_node] = myGraph.collected_influence(affected_node,RADIUS)
                print(str(max_node) + " " + str(max_influence))