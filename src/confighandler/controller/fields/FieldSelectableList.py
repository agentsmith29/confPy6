# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""
import re
from ast import literal_eval

import confighandler as ch


class FieldSelectableList(ch.Field):
    def __init__(self, value: ch.SelectableList, friendly_name: str = None, description: str = None):
        super().__init__(value, friendly_name, description)
        self.view = ch.FieldViewSelectableList(self)

    def get_list(self) -> list:
        return list(self._value)

    def get_current_index(self) -> list:
        return self._value.selected_index

    def get_selectable_list(self) -> ch.SelectableList:
        return self._value

    @property
    def value(self):
        return self._value[self._value.selected_index]

    @property
    def _value_to_emit(self):
        return self._value.selected_index

    def _set(self, value, list = None, description = None):
        if list is not None:
            self._value = ch.SelectableList(list, selected_index=value, description=description)
            self.csig_field_changed.emit(self._value_to_emit)

        self._value.selected_index = value

    def _yaml_repr(self):
        return str(f"{self._value}")

    def serialize(self):
        """Used for serializing instances. Returns the current field as a yaml-line."""
        return f"{self.name}: {self._yaml_repr()} # -> {self.value} # {self.friendly_name}: {self.description}"

    def _field_parser(self, val):
        pattern = r'<(\d+)>\s*\[(.*?)\]'
        match = re.match(pattern, val)
        sel_index = match.group(1)
        list_val_and_desc = self._convert_back_to_list_with_desc(match.group(2))
        list_val, list_dec = self._split_lists(list_val_and_desc)
        # return ch.SelectableList(literal_eval(value), selected_index=sel_index)
        return {"value": int(sel_index), "list": list_val, "description": list_dec}
        # return sel_index

    def  _convert_back_to_list_with_desc(self, str_match):
        pattern = r'\(([^,]+),\s*\'([^\']+)\'\)\s*(?:,|$)'
        matches = re.findall(pattern, str_match)
        return [(literal_eval(match[0]), match[1]) for match in matches]

    def _split_lists(sellf, tuple_list):
        first_list, second_list = zip(*tuple_list)
        return list(first_list), list(second_list)