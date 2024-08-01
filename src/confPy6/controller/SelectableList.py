# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 
Description: 
"""


class SelectableList:
    def __init__(self, *args, selected_index=0, description=None, **kwargs):
        self._list = list(*args)
        #super().__init__(*args)
        if description is None:
            description = [None] * len(self._list[0])

        if isinstance(description, str):
            description = [f"{v}{description}" for v in self._list]
        elif len(self._list) != len(description):
            raise ValueError("Length of description must match length of list")


        self._selected_index = selected_index
        self._description = description

    @property
    def selected_index(self):
        return self._selected_index

    @selected_index.setter
    def selected_index(self, value):
        self._selected_index = value
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value
        #self.iter_list =

    def append(self, value, description=None):
        self._list.append(value)
        if description is None:
            description = value
        self._description.append(description)

    def remove(self, index):
        self._list.pop(index)
        self._description.pop(index)
    def __iter__(self):
        return iter([(v, d) for v, d in zip(self._list, self.description)])

    def __getitem__(self, item):
        return self._list[item]

    def __len__(self):
        return len(self._list)

    def __str__(self):
        bs = super().__str__()
        return f"<{self._selected_index}>{str(list(self.__iter__()))}>"
