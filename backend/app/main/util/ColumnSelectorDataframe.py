from app.main.util.semanticWordLists  import listOfVectorWords
from app.main.service.languageBuilder import LanguageBuilder
from app.main.util.heuristicMeasures  import MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES

import pandas as pd


class typeOfColumn:
    def __init__(self, key:str, isName:bool):
        self.key    = key
        self.isName = isName

class ColumnSelectorDataFrame:
    """  
    Class for detecting columns of possible names
    """

    def getPossibleColumnsNames(self, df: pd.DataFrame) -> typeOfColumn:
        """  
        You get the possible columns containing any name or surname
        :param df: pandas DataFrame
        :return: typeOfColumn
        """

        for key, typeColumn in zip(df.keys(), df.dtypes):
            if typeColumn == object:
                listOfWordSemantics = list(
                        filter(
                                lambda x: LanguageBuilder().semanticSimilarity(key.lower(), x) > MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES,
                                listOfVectorWords
                            )
                    )
                if listOfWordSemantics:
                    yield typeOfColumn(key,True)
                yield typeOfColumn(key,False)

    def columnSearch(self, df: pd.DataFrame, compareFunction: classmethod) -> int:
        """  
        Searches in a column for the number of cells that comply with a certain procedure or characteristic
        :param df: DataFrame
        :paran compareFunction: Function
        :return: int
        """
        return len(compareFunction(list(df)))
