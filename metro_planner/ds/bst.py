class BSTNode:
    def __init__(self, station):
        self.station = station  # StationNode object
        self.left = None
        self.right = None

class StationBST:
    """Binary Search Tree indexing stations by Station ID for O(log N) search."""
    def __init__(self):
        self.root = None

    def insert(self, station):
        self.root = self._insert_recursive(self.root, station)

    def _insert_recursive(self, node, station):
        if node is None:
            return BSTNode(station)
        if station.station_id < node.station.station_id:
            node.left = self._insert_recursive(node.left, station)
        elif station.station_id > node.station.station_id:
            node.right = self._insert_recursive(node.right, station)
        else:
            node.station = station  # Update
        return node

    def search_by_id(self, station_id):
        curr = self.root
        while curr:
            if curr.station.station_id == station_id:
                return curr.station
            elif station_id < curr.station.station_id:
                curr = curr.left
            else:
                curr = curr.right
        return None

    def inorder_traversal(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.station)
            self._inorder(node.right, result)
