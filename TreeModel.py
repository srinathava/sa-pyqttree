from PyQt4.QtCore import *
from PyQt4.QtGui import *

class TreeModel(QAbstractItemModel):
    '''
    Needs to be instantiated with a class which has the interface defined
    by TreeItem
    '''
    def __init__(self, rootItem, parent=None):
        QAbstractItemModel.__init__(self, parent)
        self.rootItem = rootItem

    def columnCount(self, parentIndex):
        if parentIndex.isValid():
            return parentIndex.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        if role != Qt.DisplayRole:
            return QVariant()

        treeItem = index.internalPointer()
        return treeItem.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)

        return QVariant()

    def index(self, row, column, parentIndex):
        if not self.hasIndex(row, column, parentIndex):
            return QModelIndex()

        if not parentIndex.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parentIndex.internalPointer()

        if row < parentItem.childCount():
            childItem = parentItem.child(row)
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()
        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.ownRowNum(), 0, parentItem)

    def rowCount(self, parentIndex):
        if parentIndex.column() > 0:
            return 0

        if not parentIndex.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parentIndex.internalPointer()

        return parentItem.childCount()
