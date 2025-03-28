import numpy as np
import pytest
from numpy.typing import NDArray

from dvpio.read.shapes.geometry import (
    apply_affine_transformation,
    compute_affine_transformation,
)

test_cases = [
    # Scale
    (
        np.array([[0, 0], [1, 0], [0, 1]]),
        np.array([[0, 0], [2, 0], [0, 2]]),
        np.array([[2, 0, 0], [0, 2, 0], [0, 0, 1]]),
    ),
    # Translation
    (
        np.array([[0, 0], [1, 0], [0, 1]]),
        np.array([[1, 1], [2, 1], [1, 2]]),
        np.array([[1, 0, 0], [0, 1, 0], [1, 1, 1]]),
    ),
    # Rotation
    (
        np.array([[0, 0], [1, 0], [0, 1]]),
        np.array([[0, 0], [0, -1], [1, 0]]),
        np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]),
    ),
    # Rotate (-90degrees), scale (x2), translate (1,1)
    (
        np.array([[0, 0], [1, 0], [0, 1]]),
        np.array([[1, 1], [1, 3], [-1, 1]]),
        np.array([[0, 2, 0], [-2, 0, 0], [1, 1, 1]]),
    ),
]


@pytest.mark.parametrize(["query", "reference", "affine_transformation"], test_cases)
def test_compute_affine_transformation(
    query: NDArray[np.float64],
    reference: NDArray[np.int64],
    affine_transformation: NDArray[np.int64],
) -> None:
    inferred_transformation = compute_affine_transformation(query, reference, precision=3)
    assert np.isclose(inferred_transformation, affine_transformation, rtol=0.001).all()


@pytest.mark.parametrize(["query", "reference", "affine_transformation"], test_cases)
def test_apply_affine_transformation(
    query: NDArray[np.float64],
    reference: NDArray[np.float64],
    affine_transformation: NDArray[np.float64],
) -> None:
    target = apply_affine_transformation(query, affine_transformation)
    assert np.isclose(target, reference, rtol=0.001).all()
