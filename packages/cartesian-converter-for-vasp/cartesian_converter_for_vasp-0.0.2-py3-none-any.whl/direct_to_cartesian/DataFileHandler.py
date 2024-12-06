import numpy as np

from direct_to_cartesian.DataFile import DataFile

from util.const_util import *
from util.dictionary_index_util.COORDINATE_INDEX import CoordinateIndex
from util.dictionary_index_util.BASIC_DATA_INDEX import BasicDataIndex

class DataFileHandler:
    def __init__(self, datafile: DataFile, output_file_pathname: str):
        self.__datafile = datafile
        self.__output_file_pathname = output_file_pathname

    def get_cartesian_str(self) -> str:
        cartesian: np.array = np.dot(
            self.__datafile.get_coordinates()[CoordinateIndex.COORDINATE],
            np.multiply(
                self.__datafile.get_basic_data()[BasicDataIndex.LATTICE_VECTORS],
                self.__datafile.get_basic_data()[BasicDataIndex.SCALING_FACTOR]
            )
        )
        output_str = ""
        output_str += "\n".join(st for st in self.__datafile.origin_data[:ATOM_NUMBER_LINE])
        output_str += "\nCartesian\n"
        for row in cartesian:
            output_str += "\t".join(f"{element:.14f}" for element in row) + "\n"
        output_str += "\n".join(
            st for st in
            self.__datafile.origin_data[self.__datafile.get_coordinates()[CoordinateIndex.END]:]
        )
        return output_str

    def save_file_after_converted(self):
        try:
            with open(self.__output_file_pathname, "w") as output_file:
                output_file.writelines(self.get_cartesian_str())
        except Exception as e:
            raise e