from colour import Color


class Colors:
    def __init__(self, nCLusters=1):
        self.colorList = self.getRadientList(nCLusters)
        self.lenght = nCLusters

    def getRadientList(self, nCLusters):
        resultList = []
        green = Color('green')
        colors = green.range_to(Color("red"), nCLusters)
        for color in colors:
            resultList.append(color.get_hex())
        return resultList

    def getColorList(self):
        return self.colorList

    def lenght(self):
        return self.lenght()
