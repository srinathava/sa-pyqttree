from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class TreeModel(QAbstractItemModel):
    '''
    Needs to be instantiated with a class which has the interface defined
    by TreeItem
    '''
    def __init__(self, root, parent=None):
        QAbstractItemModel.__init__(self, parent)
        self.root = root

    def columnCount(self, parentIndex):
        if parentIndex.isValid():
            return len(parentIndex.internalPointer().data)
        else:
            return len(self.root.data)

    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        if role != Qt.DisplayRole:
            return QVariant()

        treeItem = index.internalPointer()
        return QVariant(treeItem.data[index.column()])

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.root.data[section])

        return QVariant()

    def index(self, row, column, parentIndex):
        if not self.hasIndex(row, column, parentIndex):
            return QModelIndex()

        if not parentIndex.isValid():
            parentItem = self.root
        else:
            parentItem = parentIndex.internalPointer()

        if row < len(parentItem.children):
            childItem = parentItem.children[row]
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        treeItem = index.internalPointer()
        parentItem = treeItem.parent
        if parentItem == self.root:
            return QModelIndex()

        return self.createIndex(parentItem.ownRowNum(), 0, parentItem)

    def rowCount(self, parentIndex):
        if parentIndex.column() > 0:
            return 0

        if not parentIndex.isValid():
            parentItem = self.root
        else:
            parentItem = parentIndex.internalPointer()

        return len(parentItem.children)

def viewTree(root, name):
    app = QApplication(sys.argv)
    view = QTreeView()
    model = TreeModel(root)
    proxyModel = QSortFilterProxyModel()
    proxyModel.setSourceModel(model)

    view.setModel(proxyModel)
    view.setWindowTitle(name)
    view.show()
    view.setSortingEnabled(True)

    app.exec_()
