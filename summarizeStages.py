#!/usr/bin/env python

from timingTree import parseTimingInfo
from TreeModel import viewTree
import sys

class CompNode:
    def __init__(self, origNodes, parent=None):
        self.origNodes = origNodes
        self.parent = parent
        self.stageName = origNodes[0].stageName.rsplit(':',1)[-1]

        self._children = None

        self.elapsedTime = 0
        for n in self.origNodes:
            self.elapsedTime += n.elapsedTime

    def ownRowNum(self):
        if self.parent:
            return self.parent.children.index(self)

        return 0

    def initChildren(self):
        self._children = []

        allChildren = []
        for n in self.origNodes:
            allChildren += n.children

        fullNames = [ch.stageName for ch in allChildren]
        names = [name.rsplit(':',1)[-1] for name in fullNames]

        group = {}
        for ch in allChildren:
            stageName = ch.stageName.rsplit(':',1)[-1]
            if not stageName in group:
                group[stageName] = []

            group[stageName].append(ch)

        for name in group:
            self._children.append(CompNode(group[name], self))

    @property
    def children(self):
        if self._children is None:
            self.initChildren()
        return self._children

    @property
    def data(self):
        return (self.stageName, self.elapsedTime)

    def __repr__(self):
        return '<CompNode(%s)>' % self.stageName
        
def main():
    root = parseTimingInfo(sys.argv[1])
    viewTree(CompNode([root]), 'Stage Summary')

if __name__ == "__main__":
    main()
