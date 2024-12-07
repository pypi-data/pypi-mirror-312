import math
from typing import Union
import textwrap


import jax.numpy as jnp
import jax.numpy.linalg as nla
from jax import vmap
import torch
import numpy as np
import pandas as pd


def _log_gaussian_density(x: jnp.ndarray, mean: jnp.ndarray, cov_matrix: jnp.ndarray):
    dim = x.shape[-1]
    sign, logdet = nla.slogdet(cov_matrix)
    log_const = dim / 2 * math.log(2 * math.pi) + 1 / 2 * sign * logdet
    x_moins_mean = x - mean
    inv_sig = jnp.linalg.inv(cov_matrix)
    log_density_unnormalized = (
        -1 / 2 * jnp.matmul(jnp.matmul(inv_sig, x_moins_mean), x_moins_mean)
    )
    return log_density_unnormalized - log_const


def _log_unit_gaussian_density(x):
    dim = x.shape[-1]
    log_const = dim / 2 * math.log(2 * math.pi)
    log_density_unnormalized = -1 / 2 * jnp.sum(x**2, axis=-1)
    return -log_const + log_density_unnormalized


def _vmap_log_gaussian_density(
    x: jnp.ndarray, mean: jnp.ndarray, cov_matrix: jnp.ndarray
):
    return vmap(_log_gaussian_density, in_axes=(0, 0, 0))(x, mean, cov_matrix)


def _vvmap_log_gaussian_density(
    x: jnp.ndarray, mean: jnp.ndarray, cov_matrix: jnp.ndarray
):
    return vmap(_vmap_log_gaussian_density, in_axes=(0, None, None))(
        x, mean, cov_matrix
    )


def _log_binom(n, endog):
    _endog = endog + (endog == 0) - (endog == n)
    return n * jnp.log(n) - _endog * jnp.log(_endog) - (n - _endog) * jnp.log(_endog)


def _log_stirling(integer: jnp.ndarray) -> jnp.ndarray:
    """
    Compute log(n!) using the Stirling formula.

    Parameters
    ----------
    integer : jnp.ndarray
        Input tensor

    Returns
    -------
    jnp.ndarray
        Approximation of log(n!) element-wise.
    """
    integer_ = integer + (integer == 0)  # Replace 0 with 1 since 0! = 1!
    return jnp.log(jnp.sqrt(2 * jnp.pi * integer_)) + integer_ * jnp.log(
        integer_ / math.exp(1)
    )


def _format_data(
    data: Union[torch.Tensor, jnp.ndarray, pd.DataFrame, np.ndarray]
) -> torch.Tensor or None:
    """
    Transforms the data in a jnp.ndarray if the input is an array, and None if the input is None.
    Raises an error if the input is not an array or None.

    Parameters
    ----------
    data : pd.DataFrame, np.ndarray, torch.Tensor, jnp.ndarray
        Input data.

    Returns
    -------
    jnp.ndarray or None
        Formatted data.

    Raises
    ------
    AttributeError
        If the value is not an array or None.
    """
    if data is None:
        return None
    if isinstance(data, pd.DataFrame):
        return jnp.array(data.values)
    if isinstance(data, (np.ndarray, jnp.ndarray)):
        return data
    if isinstance(data, torch.Tensor):
        return data.numpy()
    raise AttributeError(
        "Please insert either a numpy.ndarray, pandas.DataFrame, torch.Tensor or jnp.ndarray."
    )


def _format_dict_of_array(dict_array):
    for array in dict_array.values():
        array = _format_data(array)
    return dict_array


def _add_doc(parent_class, *, params=None, example=None, returns=None, see_also=None):
    def wrapper(fun):
        doc = getattr(parent_class, fun.__name__).__doc__
        if doc is None:
            doc = ""
        doc = textwrap.dedent(doc).rstrip(" \n\r")
        if params is not None:
            doc += textwrap.dedent(params.rstrip(" \n\r"))
        if returns is not None:
            doc += "\n\nReturns"
            doc += "\n-------"
            doc += textwrap.dedent(returns)
        if see_also is not None:
            doc += "\n\nSee also"
            doc += "\n--------"
            doc += textwrap.dedent(see_also)
        if example is not None:
            doc += "\n\nExamples"
            doc += "\n--------"
            doc += textwrap.dedent(example)
        fun.__doc__ = doc
        return fun

    return wrapper


def _sample_gaussians(number_of_samples, mean, sqrt_variance):
    """
    Sample some gaussians with the right mean and variance.
    Careful, we ask for the square root of Sigma, not Sigma.

    Args:
         number_of_samples : int. the number of samples wanted.
         mean : jnp.ndarray of size (batch_size,latent_dim)
         sqrt_variance : jnp.ndarray or size
            (batch_size, latent_dim, latent_dim). The square roots matrices
             of the covariance matrices. (e.g. if you want to sample a
             gaussian with covariance matrix A, you need to give the
            square root of A in argument.)

    Returns:
        gaussians: jnp.ndarray of size
        (number_of_samples, batch_size,latent_dim). It is a vector
        of number_of_samples gaussian of dimension mean.shape. For each
        1< i< NSample, 1<k< nBatch , W[i,k] is a gaussian with mean mean[k,:]
        and variance sqrt_variance[k,:,:]@sqrt_variance[k,:,:].
    """
    latent_dim = mean.shape[1]
    centered_gaussian = np.random.randn(number_of_samples, 1, latent_dim, 1)
    gaussians = jnp.matmul(
        jnp.expand_dims(sqrt_variance, 0), centered_gaussian
    ).squeeze() + jnp.expand_dims(mean, 0)
    return gaussians


def _vmap_all_but_params(func, x, params, additional_data):
    return vmap(
        func,
        in_axes=(
            0,
            {key: None for key in params.keys()},
            {key: 0 for key in additional_data.keys()},
        ),
    )(x, params, additional_data)


def _vmap_only_x(func, x, params, additional_data):
    return vmap(
        func,
        in_axes=(
            0,
            {key: None for key in params.keys()},
            {key: None for key in additional_data.keys()},
        ),
    )(x, params, additional_data)
