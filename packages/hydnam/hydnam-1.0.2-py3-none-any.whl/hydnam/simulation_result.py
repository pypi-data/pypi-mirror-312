import dataclasses
from typing import Optional

import numpy as np
import pandas as pd


@dataclasses.dataclass
class SimulationResult:
    timeseries: Optional[pd.Series] = None
    T: Optional[np.ndarray] = None
    P: Optional[np.ndarray] = None
    E: Optional[np.ndarray] = None
    Q_obs: Optional[np.ndarray] = None
    Q_sim: Optional[np.ndarray] = None
    U_soil: Optional[np.ndarray] = None
    S_snow: Optional[np.ndarray] = None
    Q_snow: Optional[np.ndarray] = None
    Q_inter: Optional[np.ndarray] = None
    E_eal: Optional[np.ndarray] = None
    Q_of: Optional[np.ndarray] = None
    Q_g: Optional[np.ndarray] = None
    Q_bf: Optional[np.ndarray] = None    
    L_soil: Optional[np.ndarray] = None

    def to_dataframe(self):
        data = {field.name: getattr(self, field.name) for field in dataclasses.fields(self)}
        if any(value is None for value in data.values()):
            return None
        return pd.DataFrame(data)
