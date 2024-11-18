from typing import List, Dict, Set, Optional
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class BaseCPGA:
    def __init__(self, name: str, pin_list: List[str], connection_map: Dict[int, str]):
        self.name = name
        self.pin_list = pin_list
        self.connection_map = connection_map
        self.row_list = sorted(list(set([x[0] for x in self.pin_list])))
        self.col_list = sorted(list(set([int(x[1:]) for x in self.pin_list])))
        self.row_index_dict = {
            k: len(self.row_list) - v for v, k in enumerate(self.row_list)
        }
        self.col_index_dict = {k: v for v, k in enumerate(self.col_list)}
        self.short_crit = 1
        self.measurement_error_pair = [
            ("A13", "D12"),
            ("A13", "C13"),
            ("A13", "C12"),
            ("A13", "B13"),
            ("A13", "B12"),
            ("A6", "C7"),
            ("B6", "C7"),
            ("C6", "C7"),
            ("A5", "C7"),
            ("B5", "C7"),
        ]

    def get_row(self, pin_name):
        return pin_name[0]

    def get_col(self, pin_name):
        return int(pin_name[1:])

    def get_row_index(self, pin_name):
        return self.row_index_dict[self.get_row(pin_name)]

    def get_col_index(self, pin_name):
        return self.col_index_dict[self.get_col(pin_name)]

    def add_measurement(self, data: pd.DataFrame):
        self.measurement = data

    def show_pins(self, top_view: Optional[bool] = True):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect("equal")
        row_list = [self.get_row_index(x) for x in self.pin_list]
        col_list = [self.get_col_index(x) for x in self.pin_list]

        ax.scatter(col_list, row_list, marker="o", color="k", facecolors="none")
        # for i, txt in enumerate(self.pin_list):
        #     ax.annotate(txt, (col_list[i], row_list[i]))
        ax.set_xticks(list(self.col_index_dict.values()))
        ax.set_xticklabels(list(self.col_index_dict.keys()))
        ax.set_yticks(list(self.row_index_dict.values()))
        ax.set_yticklabels(list(self.row_index_dict.keys()))
        return fig, ax

    def show_pads(self):
        n_pad_each_side = len(self.connection_map) // 4
        x_list = (
            [0] * (n_pad_each_side)
            + np.linspace(0, 1, n_pad_each_side + 2)[1:-1].tolist()
            + [1] * (n_pad_each_side)
            + np.linspace(1, 0, n_pad_each_side + 2)[1:-1].tolist()
        )
        y_list = (
            np.linspace(1, 0, n_pad_each_side + 2)[1:-1].tolist()
            + [0] * (n_pad_each_side)
            + np.linspace(0, 1, n_pad_each_side + 2)[1:-1].tolist()
            + [1] * (n_pad_each_side)
        )
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect("equal")
        ax.scatter(x_list, y_list, marker="o", color="k", facecolors="none")
        ax.annotate("1↓", (-0.1, 0.95))
        ax.set_axis_off()
        ax.set_xlim(-0.2, 1.2)
        return fig, ax

    def set_short_crit(self, crit):
        self.short_crit = crit

    def show_short_pins(self, ignore_error: Optional[bool] = False):
        fig, ax = self.show_pins()
        short_pins = self.measurement[self.measurement["resistance"] < self.short_crit][
            ["pin_1", "pin_2"]
        ]
        islands: List[Set[str]] = []
        for x in short_pins.iterrows():
            done = False
            for island in islands:
                if x[1]["pin_1"] in island or x[1]["pin_2"] in island:
                    island.add(x[1]["pin_1"])
                    island.add(x[1]["pin_2"])
                    done = True
                    break
            if not done:
                islands.append({x[1]["pin_1"], x[1]["pin_2"]})

        for island in islands:
            if ignore_error:
                if any(
                    [
                        (x, y) in self.measurement_error_pair
                        or (y, x) in self.measurement_error_pair
                        for x, y in combinations(island, 2)
                    ]
                ):
                    continue
            row_list = [self.get_row_index(x) for x in island]
            col_list = [self.get_col_index(x) for x in island]
            ax.scatter(col_list, row_list, marker="o")

        return fig, ax

    def show_short_pads(self, ignore_error: Optional[bool] = False):
        fig, ax = self.show_pads()
        short_pins = self.measurement[self.measurement["resistance"] < self.short_crit][
            ["pin_1", "pin_2"]
        ]
        islands: List[Set[str]] = []
        for x in short_pins.iterrows():
            done = False
            for island in islands:
                if x[1]["pin_1"] in island or x[1]["pin_2"] in island:
                    island.add(x[1]["pin_1"])
                    island.add(x[1]["pin_2"])
                    done = True
                    break
            if not done:
                islands.append({x[1]["pin_1"], x[1]["pin_2"]})

        n_pad_each_side = len(self.connection_map) // 4
        x_list = (
            [0] * (n_pad_each_side)
            + np.linspace(0, 1, n_pad_each_side + 2)[1:-1].tolist()
            + [1] * (n_pad_each_side)
            + np.linspace(1, 0, n_pad_each_side + 2)[1:-1].tolist()
        )
        y_list = (
            np.linspace(1, 0, n_pad_each_side + 2)[1:-1].tolist()
            + [0] * (n_pad_each_side)
            + np.linspace(0, 1, n_pad_each_side + 2)[1:-1].tolist()
            + [1] * (n_pad_each_side)
        )

        rev_connection_map = dict((v, k) for k, v in self.connection_map.items())
        for island in islands:
            if ignore_error:
                print(island)
                if any(
                    [
                        (x, y) in self.measurement_error_pair
                        or (y, x) in self.measurement_error_pair
                        for x, y in combinations(island, 2)
                    ]
                ):
                    print("error")
                    continue
            row_list = [y_list[rev_connection_map[x] - 1] for x in island]
            col_list = [x_list[rev_connection_map[x] - 1] for x in island]
            ax.scatter(col_list, row_list, marker="o")

        return fig, ax
