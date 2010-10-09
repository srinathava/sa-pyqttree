#!/usr/bin/env python

import sys

from timingTree import parseTimingInfo
from summarizeStages import CompNode
from diffTrees import DiffCell
from TreeModel import viewTree

def main():
    lhs = CompNode([parseTimingInfo(sys.argv[1])])
    rhs = CompNode([parseTimingInfo(sys.argv[2])])

    diffRoot = DiffCell(lhs, rhs)
    viewTree(diffRoot, 'Stage Summary Difference')

if __name__ == "__main__":
    main()
