import jax.numpy as np
import jax


def poisson_mapping(x):
    """Mapping to simulate from a poisson law. See Wikipédia 'Exponential Families'.
    Parameters
    ----------
    x: jax.numpy.ndarray

    Returns
    -------
    jax.numpy.ndarray

    """
    return np.exp(x)


def binomial_mapping(x):
    """Mapping to simulate from a binomial law. See Wikipédia 'Exponential Families'.
    Parameters
    ----------
    x: jax.numpy.ndarray

    Returns
    -------
    jax.numpy.ndarray
    """
    return jax.nn.sigmoid(x)
