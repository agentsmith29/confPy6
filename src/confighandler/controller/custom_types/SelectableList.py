# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 
Description: 
"""
class SelectableList(list):
    def __init__(self, *args, selected_index=0, **kwargs):
        super().__init__(*args)
        self._selected_index = selected_index

    @property
    def selected_index(self):
        return self._selected_index

    @selected_index.setter
    def selected_index(self, value):
        self._selected_index = value

    def __str__(self):
        bs = super().__str__()
        return f"<{self._selected_index}>{str(bs)}"
