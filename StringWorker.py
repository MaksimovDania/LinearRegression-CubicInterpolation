import numpy as np


class StringWorker:
    @staticmethod
    def two_dimensional_array(data, geography, parameter):
        _, par_ind = np.where(data == parameter)
        _, year_ind = np.where(data == "year")
        array = []
        for string in data:
            if geography in string:
                array.append([float(string[year_ind]), float(string[par_ind])])
        return array
