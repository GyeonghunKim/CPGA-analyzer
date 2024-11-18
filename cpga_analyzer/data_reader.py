from typing import List

import pandas as pd

from .units import Units


class DataReader:
    @classmethod
    def read(cls, file_name: str):
        df = pd.read_csv(
            file_name, names=["pin_1", "pin_2", "_", "capacitance", "resistance"]
        )
        df["capacitance"] = abs(df["capacitance"])
        df["resistance"] = abs(df["resistance"])
        return df
