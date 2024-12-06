# -*- coding: utf-8 -*-

import json
from queue import Queue
from typing import Any, Dict, List

from .vertex import Vertex


class Graph:
    def __init__(self):
        self.vertices = {}

    @classmethod
    def create_example_graph(cls):
        """
                    A
                  /   \
                 B --- C
                  \   /
                    D
                  /   \
                 E --- F
        """

        return cls.build_graph({
            "A": ["B", "C"],
            "B": ["C", "D"],
            "C": ["D"],
            "D": ["E", "F"],
            "E": ["F"]
        })

    def __iter__(self):
        return iter(self.vertices.values())

    def __contains__(self, key):
        return key in self.vertices

    def __str__(self):
        return json.dumps({
            key: [x for x in vertex.get_connections_ids()] for key, vertex in self.vertices.items()
        })

    def __repr__(self):
        return json.dumps({
            key: [x for x in vertex.get_connections_ids()] for key, vertex in self.vertices.items()
        })

    @classmethod
    def build_graph(cls, graph_definition: Dict[Any, List]):
        """
        Create a Graph

        :param graph_definition: Graph definition
        :return: The Graph.

        >>> str(Graph.create_example_graph())
        '{"A": ["B", "C"], "B": ["C", "D"], "C": ["D"], "D": ["E", "F"], "E": ["F"], "F": []}'
        """

        graph = cls()
        for key, vertices in graph_definition.items():
            for vertex in vertices:
                graph.add_edge(key, vertex)

        return graph

    def add_vertex(self, key) -> Vertex:
        if key not in self.vertices:
            self.vertices[key] = Vertex(key)

        return self.vertices[key]

    def get_vertex(self, key) -> Vertex:
        """ Return a vertex by key """
        return self.vertices.get(key, None)

    def get_vertices(self) -> Dict:
        """ Return all vertices """
        return self.vertices

    def add_edge(self, key_vertex1, key_vertex2, weight=0):
        if key_vertex1 not in self.vertices:
            self.add_vertex(key_vertex1)

        if key_vertex2 not in self.vertices:
            self.add_vertex(key_vertex2)

        self.vertices[key_vertex1].add_neighbor(self.vertices[key_vertex2], weight)

    def breadth_first_search(self, node):
        """
        Algorithm used for tree traversal on graphs or tree data structures.

        :param node: Initial node.
        :return: List of visited nodes.

        >>> Graph.create_example_graph().breadth_first_search("A")
        ['A', 'B', 'C', 'D', 'E', 'F']
        """

        visited, queue = [node], Queue()
        queue.put(node)

        while not queue.empty():
            queue.get()
            for neighbour in self.get_vertices():
                if neighbour not in visited:
                    visited.append(neighbour)
                    queue.put(neighbour)

        return visited

    def depth_first_search(self, node_id, visited: List = None):
        """
        Depth First Traversal Algorithm...

        :param node_id: Initial node.
        :param visited: Set of visited nodes.
        :return: List of visited nodes.

        >>> Graph.create_example_graph().depth_first_search("A")
        ['A', 'B', 'C', 'D', 'E', 'F']
        """

        if not visited:
            visited = []

        visited.append(node_id)

        for neighbour in self.vertices[node_id].get_connections():
            if neighbour.id not in visited:
                self.depth_first_search(neighbour.id, visited)

        return visited

    def find_path(self, start, end, path: List = None):
        if not path:
            path = []

        """
        Determine a path between two nodes...

        :param start: Start node.
        :param end: End node.
        :param path:
        :return: The path.

        >>> Graph.create_example_graph().find_path("A", "D")
        ["A", "B", "C", "D"]
        """

        path = path + [start]
        if start == end:
            return path

        if start not in self:
            return None

        for node in self.get_vertex(start).get_connections():
            if node.id not in path:
                new_path = self.find_path(node.id, end, path)
                if new_path:
                    return new_path

        return None

    def find_all_paths(self, start, end, path: List = None):
        if not path:
            path = []

        """
        Determine all paths between two nodes...

        :param start: Start node.
        :param end: End node.
        :param path:
        :return: The path.

        >>> Graph.create_example_graph().find_all_paths("A", "D")
        [["A", "B", "C", "D"], ["A", "B", "D"], ["A", "C", "D"]]
        """

        path = path + [start]
        if start == end:
            return [path]

        if start not in self:
            return []

        paths = []
        for node in self.get_vertex(start).get_connections():
            if node.id not in path:
                new_paths = self.find_all_paths(node.id, end, path)
                paths.extend(new_paths)

        return paths

    def find_shortest_path(self, start, end):
        """
        Find the shortest path between two nodes...

        :param start: Start node.
        :param end: End node.
        :return: Shortest path.

        >>> Graph.create_example_graph().find_shortest_path("A", "F")
        ['A', 'B', 'D', 'F']

        >>> Graph.create_example_graph().find_shortest_path("B", "E")
        ['B', 'D', 'E']
        """

        dist, q = {start: [start]}, Queue()
        q.put(start)

        while not q.empty():
            key = q.get()
            for next_ in self.get_vertex(key).get_connections():
                next_ = next_.id
                if next_ not in dist:
                    dist[next_] = dist[key] + [next_]
                    q.put(next_)

        return dist.get(end)
