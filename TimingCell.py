class TimingCell:
    def __init__(self, stageName, startTime, parent=None):
        self.stageName = stageName
        self.startTime = startTime
        self.endTime = startTime
        self.parentItem = parent
        self.children = []

        if self.parentItem:
            self.parentItem.children.append(self)

    def child(self, row):
        return self.children[row]

    def data(self, col):
        if col == 0:
            return self.stageName
        else:
            return (self.endTime - self.startTime)

    def childCount(self):
        return len(self.children)

    def columnCount(self):
        return 2

    def parent(self):
        return self.parentItem

    def ownRowNum(self):
        if self.parentItem:
            return self.parentItem.children.index(self)

        return 0

    def finalize(self, endTime):
        self.endTime = endTime
        self.children.sort(key=lambda item: (item.endTime - item.startTime))

    def dump(self, depth=0):
        print '%s %s\t%lf' % ('   '*depth, self.stageName,
                (self.endTime - self.startTime))
        for c in self.children:
            c.dump(depth+1)
