from collections import defaultdict
from itertools import chain


class NamePickerInTables:

    def __init__(self):
        self.picker = defaultdict(dict)

    def addIndexColumn(self, indexColumn: int):
        self.picker[indexColumn] = {
            "names": [],
            "countOfRealName": 0
        }

    def getIndexesColumn(self) -> list:
        return list(self.picker.keys())

    def addName(self, indexColumn: int, name: str):
        self.picker[indexColumn]["names"].append(name)

    def countRealName(self, indexColumn: int):
        self.picker[indexColumn]["countOfRealName"] += 1

    def isColumnName(self, indexColumn: int) -> bool:
        return indexColumn in self.picker.keys()

    def isRealColumName(self, indexColumn: int, threshold: float) -> bool:
        return (self.isColumnName(indexColumn)
                and len(self.picker[indexColumn]["names"]) > 0
                and self.picker[indexColumn]["countOfRealName"] / len(self.picker[indexColumn]["names"]) > threshold)

    def getAllNames(self, threshold: float) -> list:
        return list(chain.from_iterable([
            dataName['names'] for (_, dataName) in self.picker.items() if
            len(dataName['names']) > 0 and dataName["countOfRealName"] / len(dataName['names']) > threshold
        ])
        )

    def addIndexesColumn(self, indexes: list):
        for index in indexes:
            self.addIndexColumn(index)

    def clear(self):
        self.picker.clear()

    def isEmpty(self) -> bool:
        return not bool(self.picker)
