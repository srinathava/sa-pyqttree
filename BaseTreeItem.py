class BaseTreeItem:
    def __init__(self, data, parent):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def child(self, row):
        return self.childItems[row]

    def data(self, col):
        return itemData[col]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def parent(self):
        return self.parentItem

    def ownRowNum(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0
