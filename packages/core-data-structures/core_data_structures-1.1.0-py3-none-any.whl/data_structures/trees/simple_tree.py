# -*- coding: utf-8 -*-

from typing import Dict


class Tree(Dict):
    """ Basic implementation based on Dictionary """

    def __missing__(self, key):
        value = self[key] = type(self)()
        return value
