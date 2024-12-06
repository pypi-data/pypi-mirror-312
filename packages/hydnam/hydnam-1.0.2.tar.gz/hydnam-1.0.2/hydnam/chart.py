import io

import matplotlib.pyplot as plt
from PIL import Image

from hydnam.simulation_result import SimulationResult


def plot_q(
    simulation_result: SimulationResult, only_obs_and_sim: bool = False, figsize=(10, 6)
):
    sr = simulation_result

    plt.figure(figsize=figsize)
    plt.plot(
        sr.timeseries, sr.Q_obs, label="Q_obs", color="blue", linestyle="--", marker="o"
    )
    plt.plot(
        sr.timeseries, sr.Q_sim, label="Q_sim", color="red", linestyle="--", marker="o"
    )

    if not only_obs_and_sim:
        plt.plot(sr.timeseries, sr.Q_snow, label="Q_snow")
        plt.plot(sr.timeseries, sr.Q_inter, label="Q_inter")
        plt.plot(sr.timeseries, sr.Q_of, label="Q_of")
        plt.plot(sr.timeseries, sr.Q_g, label="Q_g")
        plt.plot(sr.timeseries, sr.Q_bf, label="Q_bf")

    plt.xlabel("Timeseries")
    plt.ylabel("Q")
    plt.legend()
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format="PNG")
    buf.seek(0)

    image = Image.open(buf)
    plt.close()

    return image
