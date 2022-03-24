from typing import Union

import numpy as np


class LinearTransformation:
    """Basic linear transformation object. 
    Handles multiplication of tuples and multiplication of other linear transformations."""
    # DUNDER METHODS -------------------------------------------------------------------------------------------------
    def __init__(self, std_matrix_repr: Union[np.ndarray, list[list], tuple[tuple]]
            ) -> None:
        """@param list/tuple of 1 dim, list/tuple of 2 dim, or numpy ndarray"""
        self.std_matrix_repr = np.array(std_matrix_repr)
        self.m_dim = self._get_size(0)
        self.n_dim = self._get_size(1)

    def __repr__(self) -> str:
        string = self.__class__.__name__ + f"(std_matrix_repr={self.std_matrix_repr}, m_dim={self.m_dim}, n_dim={self.n_dim})"
        return string

    def _get_size(self, axis):
        """Get row or column dimensions of matrix.
            @param int: 0 (column size), 1 (row size)
            @return int: row or column size"""
        if axis != 0 and axis != 1:
            raise ValueError("axis = 0 or 1")
        return np.size(self.std_matrix_repr, axis)

    @staticmethod
    def _correct_type(instance) -> bool:
        if isinstance(instance, tuple) or isinstance(instance, np.ndarray) or isinstance(instance, list):
            return True
        else: return False

    def transform(self, point: tuple) -> np.ndarray:
        # check if tuple, not necessary, but forces consistent type use
        if not self._correct_type(point): raise ValueError(f"Type {type(point)} is not tuple.")
        # m x n * n x 1, tuple must be of n size
        if len(point) != self.n_dim: raise ValueError(f"Point must be of {self.n_dim} size." +
            "Given point={point} is of {len(point)} size."
        )
        # tuple is of m size
        return np.dot(self.std_matrix_repr, point)
