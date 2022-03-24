from core.math.transformations.linear_transformations import LinearTransformation

class ScalingMatrix3(LinearTransformation):
    "Handles scaling of nx3 matrices"
    def __init__(self, initial_scale: int):
        self._scale = initial_scale
        std_matrix_repr = (
            (initial_scale, 0, 0),
            (0, initial_scale, 0),
            (0, 0, initial_scale)
        )
        super().__init__(std_matrix_repr)

    def scale(self, du: int) -> None:
        new_scale = self._scale + du
        new_scale = max(1, new_scale) # never less than 1, things get weird
        self._scale = new_scale
        self.std_matrix_repr = self.std_matrix_repr * du
