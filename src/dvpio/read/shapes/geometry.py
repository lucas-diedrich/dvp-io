import numpy as np
from numpy.typing import NDArray


def compute_affine_transformation(
    query_points: NDArray[np.float64], reference_points: NDArray[np.float64], precision: int | None = None
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Computes the affine transformation mapping query_points to reference_points.

    .. math::
        Aq = r

    Parameters
    ----------
    query_points
        An (N, 2) array of points in the query coordinate system.
    reference_points
        An (N, 2) array of corresponding points in the reference coordinate system.
    precision
        Rounding of affine transformation matrix

    Returns
    -------
    tuple[ndarray, ndarray]
        (2, 2) array representing the rotation transformation matrix [A],
        (2, 1) array representing translation vector.
    """
    if query_points.shape != reference_points.shape:
        raise ValueError("Point sets must have the same shape.")
    if query_points.shape[1] != 2:
        raise ValueError("Points must be 2D.")
    if query_points.shape[0] < 3:
        raise ValueError("At least three points are required to compute the transformation.")

    query_points = np.concatenate([query_points, np.ones(shape=(query_points.shape[0], 1))], axis=1)
    reference_points = np.concatenate([reference_points, np.ones(shape=(reference_points.shape[0], 1))], axis=1)
    affine_matrix, _, _, _ = np.linalg.lstsq(query_points, reference_points, rcond=None)

    if precision is not None:
        affine_matrix = np.around(affine_matrix, precision)

    return affine_matrix


def apply_affine_transformation(
    shape: NDArray[np.float64],
    affine_transformation: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Transform shapes between coordinate systems

    Applies affine transformation to a shape,
    in this order.

    Parameters
    ----------
    shape
        (N, 2) array of points representing a polygon, with (x, y) as last dimension
    rotation
        Rotation matrix (2, 2), representing the rotation between the coordinate systems
    translation
        Translation vector (1, 2), representing a translation [=systematic shift] between the coordinate systems

    Returns
    -------
    NDArray[np.float64]
        Shape (N, 2) after affine transformation.
    """
    # Extend shape with ones
    shape_mod = np.hstack([shape, np.ones(shape=(shape.shape[0], 1))])
    # Apply affine transformation
    shape_transformed = shape_mod @ affine_transformation
    # Reuturn shape without padded ones
    return shape_transformed[:, :-1]
