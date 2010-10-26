#!/usr/bin/env python

from TreeModel import viewTree
from TimingCell import TimingCell
import sys

def removeBeginEnd(stageId):
    (stageName, beginOrEnd) = stageId.rsplit(':', 1)
    # stageName = ':'.join(reversed(stageName.split(':')))

    return (stageName, beginOrEnd == 'begin')

def parseTimingInfo(fname):
    fp = open(fname)
    topCell = TimingCell('INIT', 0);
    stack = [topCell]

    n = 0
    for line in fp:
        n += 1
        try:
            line = line.strip()
            stageId, timeStr = line.rsplit(None, 1)
            (stageName, isBegin) = removeBeginEnd(stageId)
        except:
            print 'Error processign line %d: %s' % (n, line)
            raise

        if isBegin:
            newCell = TimingCell(stageName, float(timeStr), stack[-1])
            stack.append(newCell)
        else:
            oldCell = stack.pop()
            if oldCell.stageName != stageName:
                raise ValueError('Unexpected stage name. Expected %s, actual %s' % (stageName, oldCell.stageName))

            oldCell.finalize(float(timeStr))

    topCell.finalize(topCell.children[-1].endTime)
    return topCell

def main():
    root = parseTimingInfo(sys.argv[1])
    viewTree(root, 'Timing Tree')

if __name__ == "__main__":
    main()
