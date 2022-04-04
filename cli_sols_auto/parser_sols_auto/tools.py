from enum import Enum


def dummyparser():
    raise NotImplementedError("This parser does not exist.")


class FileType(str, Enum):
    TRF = "TRF"
    TRS = "TRS"
    VAL = "VAL"
    VEN = "VEN"
