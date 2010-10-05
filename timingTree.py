from PyQt4.QtGui import *
from TreeModel import TreeModel
from TimingCell import TimingCell
import sys

def removeBeginEnd(stageId):
    (stageName, beginOrEnd) = stageId.rsplit('_', 1)
    return (stageName, beginOrEnd == 'begin')

def parseTimingInfo(fname):
    fp = open(fname)
    line = fp.readline().strip()

    stageId, timeStr = line.split()
    topCell = TimingCell(stageId, float(timeStr))

    stack = [topCell]

    for line in fp:
        line = line.strip()
        stageId, timeStr = line.split()

        (stageName, isBegin) = removeBeginEnd(stageId)
        if isBegin:
            newCell = TimingCell(stageName, float(timeStr), stack[-1])
            stack.append(newCell)
        else:
            oldCell = stack.pop()
            if oldCell.stageName != stageName:
                raise ValueError('Unexpected stage name. Expected %s, actual %s' % (stageName, oldCell.stageName))

            oldCell.finalize(float(timeStr))

    return topCell

def main():
    topCell = parseTimingInfo(sys.argv[1])
    topCell.dump()

    app = QApplication(sys.argv)
    view = QTreeView()
    view.setModel(TreeModel(topCell))
    view.setWindowTitle('Timing Information')
    view.show()

    app.exec_()

if __name__ == "__main__":
    main()
