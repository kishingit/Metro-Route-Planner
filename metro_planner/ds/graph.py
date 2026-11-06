import heapq
from collections import deque

class StationNode:
    def __init__(self, station_id, name, line="Purple", x=0, y=0):
        self.station_id = station_id
        self.name = name
        self.line = line
        self.x = x
        self.y = y

    def to_dict(self):
        return {
            "id": self.station_id,
            "name": self.name,
            "line": self.line,
            "x": self.x,
            "y": self.y
        }

    def __repr__(self):
        return f"[{self.station_id}] {self.name} ({self.line} Line)"

class MetroGraph:
    def __init__(self):
        self.adj = {}          # name -> list of dicts: {'node': neighbor_name, 'dist': float, 'line': str}
        self.stations = {}     # station_name -> StationNode

    def add_station(self, station):
        self.stations[station.name] = station
        if station.name not in self.adj:
            self.adj[station.name] = []

    def add_edge(self, u, v, distance, line="Purple"):
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []

        self.adj[u].append({'node': v, 'dist': float(distance), 'line': line})
        self.adj[v].append({'node': u, 'dist': float(distance), 'line': line})

    def bfs(self, source, destination):
        """Finds route with Minimum Number of Stops using BFS."""
        if source not in self.adj or destination not in self.adj:
            return None, 0, 0, 0

        visited = {source}
        parent = {source: None}
        edge_used = {source: None}
        queue = deque([source])

        found = False
        while queue:
            curr = queue.popleft()
            if curr == destination:
                found = True
                break

            for edge in self.adj[curr]:
                nbr = edge['node']
                if nbr not in visited:
                    visited.add(nbr)
                    parent[nbr] = curr
                    edge_used[nbr] = edge
                    queue.append(nbr)

        if not found:
            return None, 0, 0, 0

        path = []
        curr = destination
        total_dist = 0.0
        
        while curr:
            path.append(curr)
            if parent[curr]:
                total_dist += edge_used[curr]['dist']
            curr = parent[curr]

        path.reverse()
        stops = len(path) - 1
        interchanges = self._count_interchanges(path)
        return path, round(total_dist, 2), stops, interchanges

    def dijkstra(self, source, destination):
        """Finds route with Minimum Total Distance using Dijkstra's Algorithm."""
        if source not in self.adj or destination not in self.adj:
            return None, 0, 0, 0

        distances = {node: float('inf') for node in self.adj}
        distances[source] = 0
        parent = {node: None for node in self.adj}
        edge_used = {node: None for node in self.adj}

        # Priority Queue stores: (distance, node_name)
        pq = [(0, source)]
        visited = set()

        while pq:
            curr_dist, curr_node = heapq.heappop(pq)

            if curr_node in visited:
                continue
            visited.add(curr_node)

            if curr_node == destination:
                break

            for edge in self.adj[curr_node]:
                nbr = edge['node']
                weight = edge['dist']
                if distances[curr_node] + weight < distances[nbr]:
                    distances[nbr] = distances[curr_node] + weight
                    parent[nbr] = curr_node
                    edge_used[nbr] = edge
                    heapq.heappush(pq, (distances[nbr], nbr))

        if distances[destination] == float('inf'):
            return None, 0, 0, 0

        path = []
        curr = destination
        while curr:
            path.append(curr)
            curr = parent[curr]

        path.reverse()
        stops = len(path) - 1
        interchanges = self._count_interchanges(path)
        return path, round(distances[destination], 2), stops, interchanges

    def dfs(self, start):
        """Network Traversal using DFS."""
        if start not in self.adj:
            return []
        
        visited = []
        stack = [start]
        seen = {start}

        while stack:
            curr = stack.pop()
            visited.append(curr)

            for edge in reversed(self.adj[curr]):
                nbr = edge['node']
                if nbr not in seen:
                    seen.add(nbr)
                    stack.append(nbr)
        return visited

    def _count_interchanges(self, path):
        if len(path) < 3:
            return 0
        interchanges = 0
        for i in range(1, len(path) - 1):
            prev_s, curr_s, next_s = path[i-1], path[i], path[i+1]
            prev_line = self._get_line_between(prev_s, curr_s)
            next_line = self._get_line_between(curr_s, next_s)
            if prev_line and next_line and prev_line != next_line:
                interchanges += 1
        return interchanges

    def _get_line_between(self, u, v):
        for edge in self.adj.get(u, []):
            if edge['node'] == v:
                return edge['line']
        return None
