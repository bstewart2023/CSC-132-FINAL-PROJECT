###############################################################################
# Collaborators: Corey Belk-Scroggins, Garrett Jones and Brianna Stewart
# Date: 05/01/2020
# Description: Point Class for Parking Spot Coordinates
###############################################################################
class Point(object):
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @property
    def x1(self):
        return self._x1
    @x1.setter
    def x1(self, other):
        self._x1 = other
    @property
    def y1(self):
        return self._y1
    @y1.setter
    def y1(self, other):
        self._y1 = other
    @property
    def x2(self):
        return self._x2
    @x2.setter
    def x2(self, other):
        self._x2 = other
    @property
    def y2(self):
        return self._y2
    @y2.setter
    def y2(self, other):
        self._y2 = other

    def __str__(self):
        return ("({}, {}), ({}, {})".format(self._x1, self._y1, self._x2, self._y2))
