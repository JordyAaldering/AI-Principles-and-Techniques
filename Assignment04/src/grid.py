from field import Field

class Grid():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.size = width * height
        
        self.values = [Field.EMPTY] * self.size
