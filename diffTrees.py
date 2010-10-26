#!/usr/bin/env python

import sys
import difflib

from TreeModel import viewTree
from timingTree import parseTimingInfo

class DiffCell:
    def __init__(self, lhs, rhs, parent=None):
        self.lhs = lhs
        self.rhs = rhs
        self._children = None
        self._data = None
        self._parent = parent

    @property
    def parent(self):
        return self._parent

    def _initChildren(self):
        self._children = []
        if (not self.lhs) and (not self.rhs):
            return

        if (not self.lhs):
            self._children = [DiffCell(None, ch, self) for ch in self.rhs.children]
            return

        if (not self.rhs):
            self._children = [DiffCell(ch, None, self) for ch in self.lhs.children]
            return

        lhsNames = [ch.stageName for ch in self.lhs.children]
        rhsNames = [ch.stageName for ch in self.rhs.children]

        namesDiff = difflib.ndiff(lhsNames, rhsNames)
        lhsIter = iter(self.lhs.children)
        rhsIter = iter(self.rhs.children)
        for nd in namesDiff:
            if nd.startswith('- '):
                self._children.append(DiffCell(lhsIter.next(), None, self))
            elif nd.startswith('+ '):
                self._children.append(DiffCell(None, rhsIter.next(), self))
            elif nd.startswith('  '):
                self._children.append(DiffCell(lhsIter.next(), rhsIter.next(), self))

    @property
    def children(self):
        if self._children is None:
            self._initChildren()

        return self._children

    @property
    def data(self):
        if self._data is None:
            self._data = []
            if self.lhs:
                self._data.append(self.lhs.stageName)
            else:
                self._data.append(self.rhs.stageName)

            lhsTime = 0
            if self.lhs:
                self._data.append(self.lhs.elapsedTime)
                lhsTime = self.lhs.elapsedTime
            else:
                self._data.append('-')

            rhsTime = 0
            if self.rhs:
                self._data.append(self.rhs.elapsedTime)
                rhsTime = self.rhs.elapsedTime
            else:
                self._data.append('-')

            self._data.append(rhsTime - lhsTime)

        return self._data

def main():
    tlhs = parseTimingInfo(sys.argv[1])
    trhs = parseTimingInfo(sys.argv[2])

    viewTree(DiffCell(tlhs, trhs), 'Timing Difference')

if __name__ == "__main__":
    main()
