class BaseTreeItem:
    def child(self, row):
        return self.children[row]

    def data(self, col):
        return self.dataItems()[col]

    def childCount(self):
        return len(self.children)

    def columnCount(self):
        return len(self.dataItems())

    def ownRowNum(self):
        if self.parentItem:
            return self.parentItem.children.index(self)

        return 0
