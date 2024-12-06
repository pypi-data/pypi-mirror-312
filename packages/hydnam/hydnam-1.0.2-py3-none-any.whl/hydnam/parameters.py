import dataclasses
import json

import numpy as np


@dataclasses.dataclass
class Parameters:
    umax: float = 0.01
    lmax: float = 0.01
    cqof: float = 0.01
    ckif: float = 200.0
    ck12: float = 10.0
    tof: float = 0.0
    tif: float = 0.0
    tg: float = 0.0
    ckbf: float = 500.0
    csnow: float = 0.0
    snowtemp: float = 0.0

    @staticmethod
    def get_bounds():
        bounds = (
            (0.01, 50),  # umax
            (0.01, 1000),  # lmax
            (0.01, 1),  # cqof
            (200, 1000),  # ckif
            (10, 50),  # ck12
            (0, 1),  # tof
            (0, 1),  # tif
            (0, 1),  # tg
            (500, 5000),  # ckbf
            (0, 4),  # csnow
            (-2, 4),  # snowtemp
        )
        return bounds

    def to_initial_params(self):
        return np.array(
            [
                self.umax,
                self.lmax,
                self.cqof,
                self.ckif,
                self.ck12,
                self.tof,
                self.tif,
                self.tg,
                self.ckbf,
                self.csnow,
                self.snowtemp,
            ]
        )

    def from_params(self, params):
        field_names = [field.name for field in dataclasses.fields(self)]
        bounds = self.get_bounds()

        for i, (name, bound) in enumerate(zip(field_names, bounds)):
            value = params[i]
            if not (bound[0] <= value <= bound[1]):
                raise ValueError(f"Value {value} for '{name}' is out of bounds {bound}")
            setattr(self, name, value)

        self._validate()

    def _validate(self):
        params = self.to_initial_params()
        field_names = [field.name for field in dataclasses.fields(self)]

        for i, (param, bound) in enumerate(zip(params, self.get_bounds())):
            if not (bound[0] <= param <= bound[1]):
                raise ValueError(
                    f"Attribute '{field_names[i]}' with value {param} is out of bounds {bound}"
                )

    def __post_init__(self):
        self._validate()

    def __str__(self):
        return json.dumps(self.__dict__, indent=4)
