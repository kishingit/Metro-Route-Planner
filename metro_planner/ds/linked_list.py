class RouteNode:
    def __init__(self, station_name, line="Purple", distance_from_prev=0.0):
        self.station_name = station_name
        self.line = line
        self.distance_from_prev = distance_from_prev
        self.next = None

class RouteLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, station_name, line="Purple", distance=0.0):
        new_node = RouteNode(station_name, line, distance)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1

    def to_list(self):
        result = []
        curr = self.head
        while curr:
            result.append({
                "station_name": curr.station_name,
                "line": curr.line,
                "distance": curr.distance_from_prev
            })
            curr = curr.next
        return result

    @classmethod
    def from_path_and_graph(cls, path, graph):
        rll = cls()
        if not path:
            return rll

        # First station
        first_station = path[0]
        st_obj = graph.stations.get(first_station)
        first_line = st_obj.line if st_obj else "Purple"
        rll.append(first_station, first_line, 0.0)

        for i in range(1, len(path)):
            u, v = path[i-1], path[i]
            dist = 0.0
            line = "Purple"
            for edge in graph.adj.get(u, []):
                if edge['node'] == v:
                    dist = edge['dist']
                    line = edge['line']
                    break
            rll.append(v, line, dist)
        return rll
