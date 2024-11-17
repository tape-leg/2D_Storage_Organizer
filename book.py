class Book:
    def __init__(self, name, height, width):
        self.name = name
        self.height = height
        self.width = width


class Shelf:
    def __init__(self, name, height, width, max_width, content):
        self.name = name
        self.height = height
        self.width = width
        self.max_width = max_width
        self.content = content