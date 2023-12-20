# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

class CSignal:
    def __init__(self):
        self.connections = []

    def emit(self, *args, **kwargs):
        for connection in self.connections:
            connection()

    def connect(self, func: callable):
        self.connections.append(func)
