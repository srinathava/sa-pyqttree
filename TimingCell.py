class TimingCell:
    def __init__(self, stageName, startTime, parent=None):
        self.stageName = stageName
        self.startTime = startTime
        self.endTime = startTime
        self.parent = parent
        self.children = []
        self.rowNum = 0
        self.elapsedTime = 0

        if self.parent:
            self.parent.children.append(self)

    @property
    def data(self):
        return (self.stageName, self.rowNum, self.elapsedTime)

    def finalize(self, endTime):
        self.endTime = endTime
        self.elapsedTime = self.endTime - self.startTime

        if not self.children:
            return

        origChildren = self.children
        newChildren = []
        self.children = []

        prevTime = self.startTime
        unaccounted_name = '%s_UNACCOUNTED' % self.stageName
        nChildren = 0
        for ch in origChildren:
            if ch.startTime - prevTime > 0.02*self.elapsedTime:
                nChildren += 1
                cellName = '%s_UNACCOUNTED_%d' % (self.stageName, nChildren)
                unaccounted = TimingCell(cellName, prevTime, self)
                unaccounted.finalize(ch.startTime)

            nChildren += 1
            self.children.append(ch)
            prevTime = ch.endTime

        if self.endTime - prevTime > 0.02*self.elapsedTime:
            nChildren += 1
            cellName = '%s_UNACCOUNTED_%d' % (self.stageName, nChildren)
            unaccounted = TimingCell(cellName, prevTime, self)
            unaccounted.finalize(self.endTime)

        # totalChildTime = 0
        # for ch in self.children:
        #     totalChildTime += ch.elapsedTime
        # if self.elapsedTime - totalChildTime > 0.05*self.elapsedTime:
        #     nChildren += 1
        #     cellName = '%s_SELF_%d' % (self.stageName, nChildren)
        #     unaccounted = TimingCell(cellName, prevTime, self)
        #     unaccounted.finalize(self.endTime)

        for i in range(len(self.children)):
            self.children[i].rowNum = i

    def __repr__(self):
        return '<TimingCell(%s)>' % self.stageName
