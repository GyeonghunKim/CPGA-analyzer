from .base_cpga import BaseCPGA


class CPG10039(BaseCPGA):
    def __init__(self):
        pin_list = [
            "B2",
            "B1",
            "C2",
            "C1",
            "D2",
            "D1",
            "E2",
            "E1",
            "F3",
            "F2",
            "F1",
            "G2",
            "G3",
            "G1",
            "H1",
            "H2",
            "H3",
            "J1",
            "J2",
            "K1",
            "K2",
            "L1",
            "M1",
            "L2",
            "N1",
            "M2",
            "N2",
            "M3",
            "N3",
            "M4",
            "N4",
            "M5",
            "N5",
            "L6",
            "M6",
            "N6",
            "M7",
            "L7",
            "N7",
            "N8",
            "M8",
            "L8",
            "N9",
            "M9",
            "N10",
            "M10",
            "N11",
            "N12",
            "M11",
            "N13",
            "M12",
            "M13",
            "L12",
            "L13",
            "K12",
            "K13",
            "J12",
            "J13",
            "H11",
            "H12",
            "H13",
            "G12",
            "G11",
            "G13",
            "F13",
            "F12",
            "F11",
            "E13",
            "E12",
            "D13",
            "D12",
            "C13",
            "B13",
            "C12",
            "A13",
            "B12",
            "A12",
            "B11",
            "A11",
            "B10",
            "A10",
            "B9",
            "A9",
            "C8",
            "B8",
            "A8",
            "B7",
            "C7",
            "A7",
            "A6",
            "B6",
            "C6",
            "A5",
            "B5",
            "A4",
            "B4",
            "A3",
            "A2",
            "B3",
            "A1",
        ]
        connection_map = {k: v for k, v in zip(range(1, 101), pin_list)}
        super().__init__("CPG10039", pin_list, connection_map)
