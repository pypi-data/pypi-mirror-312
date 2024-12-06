from dataclasses import dataclass
import numpy as np

from nema.data.data_properties import DataProperties


@dataclass
class FloatVector(DataProperties):
    vector: np.ndarray

    def __post_init__(self):

        # convert to numpy array if needed
        if not isinstance(self.vector, np.ndarray):
            self.vector = np.array(self.vector)

        if len(self.vector.shape) > 1:
            raise ValueError("Vector must be 1D")

    @property
    def data_type(self):
        return "FLOAT_VECTOR.V0"

    def __nema_marshall__(self):
        return {"vector": self.vector.tolist()}

    @classmethod
    def __nema_unmarshall__(cls, data: dict):
        return cls(vector=np.array(data["vector"]))


@dataclass
class FloatMatrix(DataProperties):
    matrix: np.ndarray

    def __post_init__(self):

        # convert to numpy array if needed
        if not isinstance(self.matrix, np.ndarray):
            self.matrix = np.array(self.matrix)

        if len(self.matrix.shape) != 2:
            raise ValueError("Matrix must be 2D")

    @property
    def data_type(self):
        return "FLOAT_MATRIX.V0"

    def __nema_marshall__(self):
        return {"matrix": self.matrix.tolist()}

    @classmethod
    def __nema_unmarshall__(cls, data: dict):
        return cls(matrix=np.array(data["matrix"]))
