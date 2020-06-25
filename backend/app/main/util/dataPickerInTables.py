from app.main.util.heuristicMeasures     import MAXIMUM_NUMBER_OF_POSSIBLE_NAMES_FOR_A_QUERY
from app.main.util.heuristicMeasures     import SAMPLE_DATA_TO_CHOOSE_NAMES


from collections import defaultdict
from itertools import chain
from random import sample 

class DataPickerInTables:

    def __init__(self):
        self.picker = defaultdict(dict)

    def addIndexColumn(self, indexColumn: int):
        self.picker[indexColumn] = {
            "names": [],
        }

    def addIndexesColumn(self, indexes: list):
        for index in indexes:
            self.picker[index] = {
                "names": [],
            }

    def getIndexesColumn(self) -> list:
        return list(self.picker.keys())

    def addName(self, indexColumn: int, name: str):
        self.picker[indexColumn]["names"].append(name)

    def isColumnName(self, indexColumn: int) -> bool:
        return indexColumn in self.picker.keys()

    def _getNamesSample(self, key: int) -> list:
        sampling = self.picker[key]["names"]
        if len(sampling) > MAXIMUM_NUMBER_OF_POSSIBLE_NAMES_FOR_A_QUERY:
            sampling = sample(sampling,round(len(sampling) * SAMPLE_DATA_TO_CHOOSE_NAMES))
        return sampling

    def isRealColumName(self, funtion: classmethod, indexColumn: int, threshold: float) -> bool:
        sample = self._getNamesSample(indexColumn)
        return (self.isColumnName(indexColumn)
                and len(self.picker[indexColumn]["names"]) > 0
                and len(funtion(sample)) / len(sample) > threshold)

    def getAllNames(self,funtion: classmethod, threshold: float) -> list:
        return list(chain.from_iterable([
            dataName['names'] for (key, dataName) in self.picker.items() if
            len(dataName['names']) > 0 and 
            len(funtion(self._getNamesSample(key))) / len(self._getNamesSample(key)) > threshold
        ])
        )

    def clear(self):
        self.picker.clear()

    def isEmpty(self) -> bool:
        return not bool(self.picker)
