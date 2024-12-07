from typing import Dict

import jax
import jax.numpy as np


def linear_with_offsets(
    x: jax.numpy.ndarray,
    *,
    params: Dict[str, jax.numpy.ndarray],
    additional_data: Dict[str, jax.numpy.ndarray],
) -> jax.numpy.ndarray:
    """
    Linear link function with offsets. Performs Principal
    Component Analysis (PCA) and add offsets.

    Parameters
    ----------
    x : jax.numpy.ndarray
        Input values.
    params : dict
        Model parameters including components and coef.
    additional_data : dict
        Additional data including offsets and exog.

    Returns
    -------
    jax.numpy.ndarray
        Output values from the linear link function with offsets.
    """
    linear_result = linear(x, params=params, additional_data=additional_data)
    return linear_result + (
        additional_data.get("offsets") if "offsets" in additional_data else 0
    )


def linear(
    x: jax.numpy.ndarray,
    *,
    params: Dict[str, jax.numpy.ndarray],
    additional_data: Dict[str, jax.numpy.ndarray],
) -> jax.numpy.ndarray:
    """
    Linear link function. Performs Principal Component Analysis (PCA).

    Parameters
    ----------
    x : jax.numpy.ndarray
        Input values.
    params : dict
        Model parameters including components and coef.
    additional_data : dict
        Additional data including exog and coef.

    Returns
    -------
    jax.numpy.ndarray
        Output values from the linear link function.
    """
    components_x = np.matmul(params["components"], x)
    mean = (
        np.matmul(additional_data.get("exog"), params["coef"])
        if "exog" in additional_data
        else 0
    )
    return components_x + mean
