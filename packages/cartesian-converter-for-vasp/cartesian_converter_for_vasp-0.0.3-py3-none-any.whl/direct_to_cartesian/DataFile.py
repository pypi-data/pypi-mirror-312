import numpy as np

from util.const_util.CONTCAR_AND_POSCAR_CONFIG import *
from util.dictionary_index_util.COORDINATE_INDEX import CoordinateIndex
from util.dictionary_index_util.BASIC_DATA_INDEX import BasicDataIndex

class DataFile:
    def __init__(self, file_pathname: str):
        self.__filename = file_pathname
        self.__origin_data: str = ""
        self.__name: str = ""
        self.__scaling_factor:float = 0.0
        self.__lattice_vectors: np.array = None
        self.__atom_stat: dict = {}
        self.__coordinates_type: str = ""
        self.__coordinates: np.array = None
        self.__coordinates_end_line: int = 0
        self.__initialize_origin_info()
        self.__initialize()

    def __initialize_origin_info(self):
        try:
            print()
            print("--------------------------------Read File--------------------------------")
            with open(self.__filename, "r") as file:
                self.__origin_data = file.read().splitlines()
            print("-------------------------------------------------------------------------")
            print()
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.__filename} not found.")
        except (ValueError, IndexError) as e:
            raise ValueError(f"Error while parsing file content: {e}")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {e}")

    def __initialize(self) -> None:
        print("----------------------------Initialize Basic Data----------------------------")
        info = self.__origin_data
        self.__name = info[NAME_LINE - 1]
        self.__scaling_factor = float(info[SCALING_FACTOR_LINE - 1])
        self.__lattice_vectors = np.array([
            list(map(float, vector.split()))
            for vector in info[(LATTICE_VECTORS_START_LINE - 1):LATTICE_VECTORS_END_LINE]
        ])
        atom_types: list = info[ATOM_TYPE_LINE - 1].split()
        atom_numbers: list = list(
            map(int, info[ATOM_NUMBER_LINE - 1].split())
        )
        for atom_type, atom_number in zip(atom_types, atom_numbers):
            self.__atom_stat[atom_type] = atom_number
        self.__atom_stat['ALL'] = sum(atom_numbers)
        print("-----------------------------------------------------------------------------")
        print()

        print("--------------------------Initialize Coordinate Data-------------------------")
        self.__coordinates_end_line = self.__atom_stat['ALL'] + COORDINATE_START_LINE - 1
        self.__coordinates_type = info[COORDINATE_TYPE_LINE - 1]
        self.__coordinates = np.array([
            list(map(float, coor.split()))
            for coor in info[(COORDINATE_START_LINE - 1):self.__coordinates_end_line]
        ])
        print("-----------------------------------------------------------------------------")
        print()

    def get_basic_data(self) -> dict:
        return {
            BasicDataIndex.NAME             : self.__name,
            BasicDataIndex.SCALING_FACTOR   : self.__scaling_factor,
            BasicDataIndex.LATTICE_VECTORS  : self.__lattice_vectors,
            BasicDataIndex.ATOM_STAT        : self.__atom_stat,
        }

    def get_coordinates(self) -> dict:
        return {
            CoordinateIndex.TYPE        : self.__coordinates_type,
            CoordinateIndex.COORDINATE  : self.__coordinates,
            CoordinateIndex.END         : self.__coordinates_end_line,
        }

    @property
    def origin_data(self):
        return self.__origin_data