from scud._utils import _log_stirling


def poisson_log_normalizer(x):
    """The log normalize constant in the poisson case.

    Parameters
    ----------
    x: jax.numpy.ndarray

    Returns
    -------
    jax.numpy.ndarray
    """
    return _log_stirling(x)


def binomial_log_normalizer(x, n):
    """Log normalize constant in the binomial case.
    Parameters
    ----------
    x: jax.numpy.ndarray
    n: int

    Returns
    -------
    jax.numpy.ndarray
    """
    num = _log_stirling(n)
    denom_left = _log_stirling(x)
    denom_right = _log_stirling(n - x)
    return num - denom_left - denom_right
