import unittest

from deprecated import deprecated
import numpy as np
#
# from direct_to_cartesian.FileHandler import FileHandler
from direct_to_cartesian.DataFile import DataFile
from direct_to_cartesian.DataFileHandler import DataFileHandler


class FileHandlerTest(unittest.TestCase):
    # def test_file_handler_class(self):
    #     handler = FileHandler("./CONTCAR", "./CONTCAR_C")
    #     handler.convert_to_cartesian()

    def test1(self):
        lattice_vectors = np.array([
            [20.0, 0.0, 0.0],  # a1
            [0.0, 20.0, 0.0],  # a2
            [0.0, 0.0, 20.0]   # a3
        ])

        # 直角坐标 (相对坐标)
        direct_coords = np.array([
            [0.0716021408501959, 0.9734334250018648, 0.0000000000000000],
            [0.9997448392206820, 0.9740060709304666, 0.0000000000000000],
            [0.9750339954236580, 0.0446316904570310, 0.0000000000000000],
            [0.9808632880536692, 0.9465397983940065, 0.0446756894737703],
            [0.9808632880536692, 0.9465397983940065, 0.9553243105262297],
            [0.9200415587354911, 0.0451480971649687, 0.0000000000000000],
            [0.9924062585533804, 0.0717124248566350, 0.9554417829533932],
            [0.9924062585533804, 0.0717124248566350, 0.0445582170466068],
            [0.0870383725558810, 0.9272762699443859, 0.0000000000000000]
        ])

        # 将直角坐标转换为笛卡尔坐标
        cartesian_coords = np.dot(direct_coords, lattice_vectors)
        print(cartesian_coords)

    def test2(self):
        list1 = [1, 2, 3]
        print(str(list1))

    def test_data_file(self):
        data_file = DataFile("./POSCAR")
        print(data_file.get_basic_data())
        print(data_file.get_coordinates())
        handler = DataFileHandler(data_file, "./POSCAR_C")
        print(handler.get_cartesian_str())

if __name__ == '__main__':
    unittest.main()
