from app.main.util.semanticWordLists import listOfVectorWords
from app.main.service.languageBuilder import LanguageBuilder
from app.main.util.heuristicMeasures import MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES
import pandas as pd


class typeOfColumn:
    def __init__(self, key:str, isName:bool):
        self.key = key
        self.isName = isName

class ColumnSelectorDataFrame:

    def getPossibleColumnsNames(self, df: pd.DataFrame) -> typeOfColumn:
        for key, typeColumn in zip(df.keys(), df.dtypes):
            if typeColumn == object:
                listOfWordSemantics = list(
                        filter(
                                lambda x: LanguageBuilder().semanticSimilarity(key, x) > MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES,
                                listOfVectorWords
                            )
                    )
                if listOfWordSemantics:
                    yield typeOfColumn(key,True)
                yield typeOfColumn(key,False)

    def columnSearch(self, df: pd.DataFrame, comparateFuntion: classmethod) -> int:
        return len(comparateFuntion(list(df)))

    
