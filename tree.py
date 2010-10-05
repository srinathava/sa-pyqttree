from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from BaseTreeItem import BaseTreeItem
from TreeModel import TreeModel

class TreeModel(QAbstractItemModel):
    def __init__(self, parent=None):
        QAbstractItemModel.__init__(self, parent)
        self.rootItem = None
        self.setupModelData()

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
        return treeItem.itemData[index.column()]

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.itemData[section]

        return QVariant()

    def index(self, row, column, parentIndex):
        if not self.hasIndex(row, column, parentIndex):
            return QModelIndex()

        if not parentIndex.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parentIndex.internalPointer()

        if row < len(parentItem.childCount()):
            childItem = parentItem.child(row)
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parentItem
        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parentIndex):
        if parentIndex.column() > 0:
            return 0

        if not parentIndex.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parentIndex.internalPointer()

        return parentItem.childCount()

    def setupModelData(self, fname):
        self.rootItem = BaseTreeItem(['Name', 'Time'], None)

        self.rootItem.appendChild(BaseTreeItem(['me', 'too'], self.rootItem))

        c2 = BaseTreeItem(['really', 'wow'], self.rootItem)
        self.rootItem.appendChild(c2)

        c2.appendChild(BaseTreeItem(['grand', 'kid'], c2))

        gc2 = BaseTreeItem(['grand', 'kid2'], c2)
        c2.appendChild(gc2)

        gc2.appendChild(BaseTreeItem(['grand', 'kid22'], gc2))
        gc2.appendChild(BaseTreeItem(['grand', 'kid23'], gc2))

def main():
    app = QApplication(sys.argv)
    view = QTreeView()
    view.setModel(TreeModel())
    view.setWindowTitle('Simple Tree Model')
    view.show()

    app.exec_()

if __name__ == "__main__":
    main()

