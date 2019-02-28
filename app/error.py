# -*- coding: UTF-8 -*-

class DuplicateException(Exception):
    def __init__(self, name):
        Exception.__init__(self, name)
        self.typename = name


class WrongDataException(Exception):
    def __init__(self, name):
        Exception.__init__(self, name)
        self.typename = name


class NotFoundException(Exception):
    def __init__(self, name):
        Exception.__init__(self, name)
        self.typename = name
