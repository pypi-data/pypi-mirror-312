import jax.numpy as jnp
import jax


def poisson_log_partition(x):
    """
    Poisson link from the exponential family.
    See Wikipedia 'Exponential families'.

    Parameters
    ----------
    x: jax.numpy.ndarray

    Returns
    -------
    jax.numpy.ndarray
    """
    return jnp.exp(x)


def binomial_log_partition(x, n):
    """
    Binomial link from the exponential family.
    See Wikipedia 'Exponential families'.
    Parameters
    ----------
    x: jax.numpy.ndarray
    n:int

    Returns
    -------
    jax.numpy.ndarray
    """
    return n * jax.numpy.logaddexp(jnp.array([0]), x)
