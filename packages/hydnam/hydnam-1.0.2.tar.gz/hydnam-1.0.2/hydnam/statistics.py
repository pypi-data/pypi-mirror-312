import dataclasses
import json

from hydutils.stats import nse, rmse, pbias
import numpy as np


@dataclasses.dataclass
class Statistics:
    nse: float = None
    rmse: float = None
    pbias: float = None
    
    def stats(self, q_obs: np.ndarray, q_sim: np.ndarray):
        self.nse = nse(q_sim, q_obs)
        self.rmse = rmse(q_obs, q_sim)
        self.pbias = pbias(q_obs, q_sim)

    def __str__(self):
        return json.dumps(self.__dict__, indent=4)
