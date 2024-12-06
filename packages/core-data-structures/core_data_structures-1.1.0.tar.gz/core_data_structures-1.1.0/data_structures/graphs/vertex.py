# -*- coding: utf-8 -*-

from typing import Dict, List

try:
    from typing import Self

except ImportError:
    # For earlier versions...
    from typing_extensions import Self


class Vertex:
    def __init__(self, key):
        self._id = key
        self._connections = {}

    def __str__(self):
        return f"{self.id} connectedTo: {[x.id for x in self._connections]}"

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def get_weight(self, vertex: Self):
        """ Retrieve the weight to reach the neighbor """
        return self._connections[vertex]

    def get_connections(self) -> Dict:
        """ Return the connections """
        return self._connections

    def get_connections_ids(self) -> List:
        """ Return the connections ids """
        return [vertex.id for vertex in self.get_connections()]

    def add_neighbor(self, vertex: Self, weight=0):
        """ Add or update a connection """
        self._connections[vertex] = weight
