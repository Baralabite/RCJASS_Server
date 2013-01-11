import pymunk.Space

class World(pymunk.Space):
    def __init__(self):
        pymunk.Space.__init__(self)