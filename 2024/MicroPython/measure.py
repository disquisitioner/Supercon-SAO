class Measure:
    def __init__(self):
        self.value = 0.0
        self.total = 0.0
        self.maxvalue = 0.0
        self.minvalue = 0.0
        self.average = 0.0 
        self.count = 0
        self.newminmax = True

    def include(self,value):
        self.count += 1          # we began with 0
        self.value = value
        self.total += value
        if self.newminmax == True:
            self.maxvalue = self.minvalue = value
            self.newminmax = False
        else:
            if value > self.maxvalue:
                self.maxvalue = value
            if value < self.minvalue:
                self.minvalue = value

        self.average = self.total / self.count

    def clear(self):
        self.value = self.total = self.average = 0.0
        self.count = 0
        self.maxvalue = self.minvalue = 0.0
        self.newminmax = True

    def resetAverage(self):
        self.value = self.total = self.average = 0;
        self.count = 0

    def getCurrent(self):
        return self.value

    def getAverage(self):
        return self.average

    def getMaximum(self):
        return self.maxvalue

    def getMinimum(self):
        return self.minvalue

    def getCount(self):
        return self.count

    def getTotal(self):
        return self.total