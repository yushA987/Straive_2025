class Classify:
    def classifyy(self, num):
        if num % 2 == 0:
            return "even"
        elif num % 3 == 0:
            return "divisible by 3"
        else:
            return "other"
