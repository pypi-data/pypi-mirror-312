# HydNAM

![PyPI - Version](https://img.shields.io/pypi/v/hydnam)

**HydNAM** is a Python implementation of the NedborAfstromnings Model (NAM), a lumped rainfall–runoff model.

This project is based on the [NAM_Model](https://github.com/hckaraman/NAM_Model) created by [hckaraman](https://github.com/hckaraman). 

## Installation

```bash
pip install hydnam
```

## Getting Started

### 1. Prepare the Dataset

The dataset must contain the following properties: Date, Temperature, Precipitation, Evapotranspiration, and Discharge.

| Date       | Temperature | Discharge | Precipitation | Evapotranspiration |
|------------|-------------|-----------|---------------|--------------------|
| 10/9/2016  | 15.4        | 0.25694   | 0             | 2.79               |
| 10/10/2016 | 14.4        | 0.25812   | 0             | 3.46               |
| 10/11/2016 | 14.9        | 0.30983   | 0             | 3.65               |
| 10/12/2016 | 16.1        | 0.31422   | 0             | 3.46               |
| 10/13/2016 | 20.1        | 0.30866   | 0             | 5.64               |
| 10/14/2016 | 13.9        | 0.30868   | 0             | 3.24               |
| 10/15/2016 | 11.1        | 0.31299   | 0             | 3.41               |
| ...        | ...         | ...       | ...           | ...                |

Ensure that the time intervals between dates are consistent (e.g., 24 hours) for accurate model performance.

### 2. Initialize the NAM Model

```python
from datetime import datetime
from hydnam.chart import plot_q
from hydnam.dataset import Dataset
from hydnam.hydnam import HydNAM
from hydnam.parameters import Parameters

dataset = Dataset(
    timeseries=[
        datetime(2016, 10, 9),
        datetime(2016, 10, 10),
        datetime(2016, 10, 11),
    ],
    temperature=[15.4, 14.4, 14.9],
    precipitation=[0.0, 0.0, 0.0],
    evapotranspiration=[2.79, 3.46, 3.65],
    discharge=[0.25694, 0.25812, 0.30983]
)

params = Parameters(
    umax=0.01,
    lmax=0.01,
    cqof=0.01,
    ckif=200.0,
    ck12=10.0,
    tof=0.0,
    tif=0.0,
    tg=0.0,
    ckbf=500.0,
    csnow=0.0,
    snowtemp=0.0
)

nam = HydNAM(
    dataset=dataset,
    parameters=params,
    area=58.8,
    interval=24.0,
    start=None,
    end=None,
    spin_off=0.0
)
print(f'Parameters: {nam.parameters}')
print(f'Statistics: {nam.statistics}')
df = nam.simulation_result.to_dataframe()
```

### 3. Optimize the Model

```
NAM.optimize()
```

The model will calculate and check which `Parameters` are optimal for the model and use it as the main `Parameters` for
the model.

### 4. Customize Parameters

```
nam.set_parameters(Parameters())
```

### 5. Show Discharge

```
from hydnam.chart import plot_q
...
plot_q(nam.simulation_result, only_obs_and_sim=False).show()
```

## License

This library is released under the MIT License.

## Contact

If you have any questions or issues, please open an issue on [GitHub](https://github.com/duynguyen02/hydnam/issues) or
email us at [duynguyen02.dev@gmail.com](mailto:duynguyen02.dev@gmail.com).
