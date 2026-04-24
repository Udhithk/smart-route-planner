# smart_route_planner.py

import heapq
import math

# -------------------------------
# Graph Class
# -------------------------------
class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v, weight):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))  # undirected graph

    def get_neighbors(self, node):
        return self.graph.get(node, [])


# -------------------------------
# Dijkstra Algorithm
# -------------------------------
def dijkstra(graph, start, end):
    pq = [(0, start)]
    distances = {node: float('inf') for node in graph.graph}
    parent = {node: None for node in graph.graph}

    distances[start] = 0

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        if current_node == end:
            break

        for neighbor, weight in graph.get_neighbors(current_node):
            distance = current_dist + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parent[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    return reconstruct_path(parent, start, end), distances[end]


# -------------------------------
# A* Algorithm
# -------------------------------
def heuristic(a, b, coordinates):
    # Euclidean distance
    (x1, y1) = coordinates[a]
    (x2, y2) = coordinates[b]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def a_star(graph, start, end, coordinates):
    pq = [(0, start)]
    g_cost = {node: float('inf') for node in graph.graph}
    parent = {node: None for node in graph.graph}

    g_cost[start] = 0

    while pq:
        _, current = heapq.heappop(pq)

        if current == end:
            break

        for neighbor, weight in graph.get_neighbors(current):
            tentative_g = g_cost[current] + weight

            if tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                f_cost = tentative_g + heuristic(neighbor, end, coordinates)
                parent[neighbor] = current
                heapq.heappush(pq, (f_cost, neighbor))

    return reconstruct_path(parent, start, end), g_cost[end]


# -------------------------------
# Path Reconstruction
# -------------------------------
def reconstruct_path(parent, start, end):
    path = []
    current = end

    while current:
        path.append(current)
        current = parent[current]

    path.reverse()

    if path[0] == start:
        return path
    return []


# -------------------------------
# Traffic Simulation
# -------------------------------
def apply_traffic(graph, u, v, new_weight):
    for i, (neighbor, weight) in enumerate(graph.graph[u]):
        if neighbor == v:
            graph.graph[u][i] = (v, new_weight)

    for i, (neighbor, weight) in enumerate(graph.graph[v]):
        if neighbor == u:
            graph.graph[v][i] = (u, new_weight)


# -------------------------------
# Example Usage
# -------------------------------
if __name__ == "__main__":
    g = Graph()

    # Add edges (node1, node2, distance)
    g.add_edge("A", "B", 4)
    g.add_edge("A", "C", 2)
    g.add_edge("B", "C", 5)
    g.add_edge("B", "D", 10)
    g.add_edge("C", "E", 3)
    g.add_edge("E", "D", 4)
    g.add_edge("D", "F", 11)

    # Coordinates for A* heuristic
    coordinates = {
        "A": (0, 0),
        "B": (2, 2),
        "C": (1, 1),
        "D": (5, 3),
        "E": (3, 2),
        "F": (6, 4)
    }

    start = "A"
    end = "F"

    print("----- Dijkstra -----")
    path, dist = dijkstra(g, start, end)
    print("Path:", path)
    print("Distance:", dist)

    print("\n----- A* -----")
    path, dist = a_star(g, start, end, coordinates)
    print("Path:", path)
    print("Distance:", dist)

    print("\n----- Applying Traffic (C -> E becomes slower) -----")
    apply_traffic(g, "C", "E", 10)

    path, dist = dijkstra(g, start, end)
    print("New Path:", path)
    print("New Distance:", dist)