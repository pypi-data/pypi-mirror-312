import jax.numpy as np
from jax import random

COMPONENT_KEY = "components"
COV_KEY = "exog"
COEF_KEY = "coef"
OFFSETS_KEY = "offsets"


def get_components(
    dim: int = 50, latent_dimension: int = 10, seed: int = 0
) -> np.ndarray:
    """
    Generate components for a linear model.

    Parameters
    ----------
    dim : int, optional
        The total number of features in the data, by default 50.
    latent_dimension : int, optional
        The number of latent dimensions, by default 10.
    seed : int, optional
        Random seed for reproducibility, by default 0.

    Returns
    -------
    components : jax.numpy.ndarray
        The generated components for the linear model.
    """
    key = random.PRNGKey(seed)
    block_size = dim // latent_dimension
    components = np.zeros((dim, latent_dimension))

    for column_number in range(latent_dimension):
        start_idx = column_number * block_size
        end_idx = (column_number + 1) * block_size
        components = components.at[start_idx:end_idx, column_number].set(1)

    components += random.normal(key=key, shape=(dim, latent_dimension)) / 8
    return components


def get_coef(nb_cov: int = 1, dim: int = 50, seed: int = 0) -> np.ndarray:
    """
    Generate coefficients.

    Parameters
    ----------
    nb_cov : int, optional
        The number of exog, by default 1.
    dim : int, optional
        The total number of features in the data, by default 50.
    seed : int, optional
        Random seed for reproducibility, by default 0.

    Returns
    -------
    coefficients : jax.numpy.ndarray
        The generated coefficients for linear regression.
    """
    key = random.PRNGKey(seed)
    coefficients = random.normal(key=key, shape=(nb_cov, dim))
    return coefficients


def get_exog(n_samples: int = 100, nb_cov: int = 1, seed: int = 0) -> np.ndarray:
    """
    Generate binary exog.

    Parameters
    ----------
    n_samples : int, optional
        The number of samples, by default 100.
    nb_cov : int, optional
        The number of exog, by default 1.
    seed : int, optional
        Random seed for reproducibility, by default 0.

    Returns
    -------
    exog : jax.numpy.ndarray
        The generated binary exog.
    """
    key = random.PRNGKey(seed)
    exog = random.bernoulli(key=key, shape=(n_samples, nb_cov))
    return exog


def get_offsets(
    n_samples: int = 100, dim: int = 50, seed: int = 0, only_zero: bool = False
) -> np.ndarray:
    """
    Generate offsets for linear regression.

    Parameters
    ----------
    n_samples : int, optional
        The number of samples, by default 100.
    dim : int, optional
        The total number of features in the data, by default 50.
    seed : int, optional
        Random seed for reproducibility, by default 0.
    only_zero : bool, optional
        If True, only zero offsets are generated, by default False.

    Returns
    -------
    offsets : jax.numpy.ndarray
        The generated offsets for linear regression.
    """
    key = random.PRNGKey(seed)
    offsets = random.normal(key=key, shape=(n_samples, dim))
    return offsets * 0 if only_zero else offsets


# pylint: disable=too-many-positional-arguments,too-many-arguments
def get_linear_params_and_additional_data(
    n_samples: int = 100,
    nb_cov: int = 1,
    dim: int = 50,
    latent_dimension: int = 10,
    no_offsets: bool = False,
    seed: int = 0,
) -> dict:
    """
    Generate linear regression parameters and additional data (offsets and exog).

    Parameters
    ----------
    n_samples : int, optional
        The number of samples, by default 100.
    nb_cov : int, optional
        The number of exog, by default 1.
    dim : int, optional
        The total number of features in the data, by default 50.
    latent_dimension : int, optional
        The number of latent dimensions, by default 10.
    no_offsets : bool, optional
        If True, generate data without offsets, by default False.
    seed : int, optional
        Random seed for reproducibility, by default 0.

    Returns
    -------
    dictionary : dict
        A dictionary containing components, coefficients, exog, and offsets.
    """
    components = get_components(dim, latent_dimension, seed=seed)
    coefficients = get_coef(nb_cov, dim, seed=seed)
    exog = get_exog(n_samples, nb_cov, seed=seed)
    offsets = get_offsets(n_samples, dim, seed=seed, only_zero=no_offsets)

    return {
        COMPONENT_KEY: components,
        COEF_KEY: coefficients,
        COV_KEY: exog,
        OFFSETS_KEY: offsets,
    }
