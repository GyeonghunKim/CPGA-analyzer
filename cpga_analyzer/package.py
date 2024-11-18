from typing import List, Dict, Set, Optional

import numpy as np
import matplotlib.pyplot as plt

from .cpga import BaseCPGA
from .units import Units


class Package:
    def __init__(self, cpga: BaseCPGA, wirebonding_map: Dict[str, str]):
        self.cpga = cpga
        self.wirebonding_map = wirebonding_map
        self.electrode_list = list(wirebonding_map.keys())
        self.pad_list = list(wirebonding_map.values())

    def show_capacitance_hist(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        cap_list = []
        for i, electrode_1 in enumerate(self.electrode_list):
            for j, electrode_2 in enumerate(self.electrode_list):
                pad_1 = self.wirebonding_map[electrode_1]
                pad_2 = self.wirebonding_map[electrode_2]
                try:
                    cap = self.cpga.measurement[
                        (
                            self.cpga.measurement["pin_1"]
                            == self.cpga.connection_map[pad_1]
                        )
                        & (
                            self.cpga.measurement["pin_2"]
                            == self.cpga.connection_map[pad_2]
                        )
                    ]["capacitance"].values[0]
                    cap_list.append(cap / Units.pF)
                except IndexError:
                    pass

        ax.hist(cap_list, bins=101)
        ax.set_title("Capacitance Histogram (pF)")
        ax.set_xlabel("Capacitance (pF)")
        ax.set_ylabel("Counts")
        return fig, ax

    def show_capacitance_map(self, cut_off: float = 100 * Units.pF):
        capacitance_map = np.nan * np.zeros(
            (len(self.electrode_list), len(self.electrode_list))
        )
        for i, electrode_1 in enumerate(self.electrode_list):
            for j, electrode_2 in enumerate(self.electrode_list):
                pad_1 = self.wirebonding_map[electrode_1]
                pad_2 = self.wirebonding_map[electrode_2]
                try:
                    cap = self.cpga.measurement[
                        (
                            self.cpga.measurement["pin_1"]
                            == self.cpga.connection_map[pad_1]
                        )
                        & (
                            self.cpga.measurement["pin_2"]
                            == self.cpga.connection_map[pad_2]
                        )
                    ]["capacitance"].values[0]
                    if cap < cut_off:
                        cap = np.nan
                    capacitance_map[min(i, j), max(i, j)] = cap / Units.pF
                except IndexError:
                    capacitance_map[i, j] = np.nan
        fig = plt.figure(figsize=(15, 10))
        ax = fig.add_subplot(111)
        ax.set_aspect("equal")
        ax.grid()
        ax.set_title("Capacitance Map (pF)")
        cax = ax.matshow(capacitance_map, cmap="coolwarm")
        fig.colorbar(cax)
        ax.set_xticks(np.arange(len(self.electrode_list)))
        ax.set_yticks(np.arange(len(self.electrode_list)))
        ax.set_xticklabels(self.electrode_list)
        ax.set_yticklabels(self.electrode_list)
        return fig, ax
