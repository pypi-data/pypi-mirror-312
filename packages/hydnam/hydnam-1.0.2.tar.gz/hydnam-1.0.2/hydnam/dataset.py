from datetime import datetime
from typing import List

from hydutils.hyd_constants import (
    TIMESERIES,
    TEMPERATURE,
    PRECIPITATION,
    EVAPOTRANSPIRATION,
    DISCHARGE,
)
import pandas as pd


class Dataset:
    def __init__(
        self,
        timeseries: List[datetime],
        temperature: List[float],
        precipitation: List[float],
        evapotranspiration: List[float],
        discharge: List[float],
    ):
        self._timeseries = timeseries
        self._temperature = temperature
        self._precipitation = precipitation
        self._evapotranspiration = evapotranspiration
        self._discharge = discharge

    def to_dataframe(self):
        dataset_dict = {
            TIMESERIES: self._timeseries,
            TEMPERATURE: self._temperature,
            PRECIPITATION: self._precipitation,
            EVAPOTRANSPIRATION: self._evapotranspiration,
            DISCHARGE: self._discharge
        }

        df = pd.DataFrame(dataset_dict)
        df[TIMESERIES] = pd.to_datetime(df[TIMESERIES])
        return df
