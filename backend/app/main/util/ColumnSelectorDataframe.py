from app.main.util.semanticWordLists import listOfVectorWords
from app.main.service.languageBuilder import LanguageBuilder
from app.main.util.heuristicMeasures import MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES
import pandas as pd


class ColumnSelectorDataFrame:

    def getPossibleColumnsNames(self, df: pd.DataFrame) -> str:
        for key, typeColumn in zip(df.keys(), df.dtypes):
            if typeColumn == object:
                listOfWordSemantics = list(
                        filter(
                                lambda x: LanguageBuilder().semanticSimilarity(key, x) > MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES,
                                listOfVectorWords
                            )
                    )
                if listOfWordSemantics:
                    yield key

    def getPossibleColumnsIdCards(self, df: pd.DataFrame):
        for key, typeColumn in zip(df.keys(), df.dtypes):
            if typeColumn == object:
                yield key

    def columnSearch(self, df: pd.DataFrame, comparateFuntion: classmethod) -> int:
        return sum(list(map(lambda x: comparateFuntion(str(x)), df)))

    
