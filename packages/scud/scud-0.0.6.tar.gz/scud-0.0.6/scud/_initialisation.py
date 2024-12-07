from typing import Optional
import math

import numpy as np
import jax.numpy as jnp
from jax.scipy.stats.binom import logpmf
from jax.scipy.special import logit
from jax.nn import sigmoid
from jax import grad
from sklearn.decomposition import PCA
import optax


def _compute_poissreg_loglike(
    endog: jnp.ndarray, offsets: jnp.ndarray, exog: jnp.ndarray, coef: jnp.ndarray
) -> jnp.ndarray:
    """
    Compute the log likelihood of a Poisson regression model.

    Parameters
    ----------
    endog : jnp.ndarray
        The dependent variable of shape (n_samples, n_features).
    offsets : jnp.ndarray
        The offset term of shape (n_samples, n_features).
    exog : jnp.ndarray
        The exog of shape (n_samples, n_exog).
    coef : jnp.ndarray
        The regression coefficients of shape (n_exog, n_features).

    Returns
    -------
    jnp.ndarray
        The log likelihood of the Poisson regression model.
    """
    exog_coef = jnp.matmul(exog, coef)
    return jnp.sum(-jnp.exp(offsets + exog_coef) + endog * (offsets + exog_coef))


class _PoissonReg:
    """
    Poisson regression model.

    Attributes
    ----------
    coef : jnp.ndarray
        The learned regression coefficients.

    Methods
    -------
    fit(endog, exog, offsets, n_iter_max=300, tol=0.001)
        Fit the Poisson regression model to the given data.
    """

    def __init__(self) -> None:
        """
        Class to infer the maximum likelihood of the coef for the Poisson Regression.
        """
        self._beta: Optional[jnp.ndarray] = None

    def fit(
        self,
        endog: jnp.ndarray,
        exog: jnp.ndarray,
        offsets: jnp.ndarray,
    ) -> None:
        """
        Fit the Poisson regression model to the given data.

        Parameters
        ----------
        endog : jnp.ndarray
            The dependent variable of shape (n_samples, n_features).
        exog : jnp.ndarray
            The exog of shape (n_samples, n_exog).
        offsets : jnp.ndarray
            The offset term of shape (n_samples, n_features).
        """
        n_iter_max = 300
        tol = 0.001
        lr = 0.005
        beta = jnp.array(np.random.rand(exog.shape[1], endog.shape[1]))
        optimizer = optax.rprop(learning_rate=lr)
        opt_state = optimizer.init(beta)
        i = 0
        grad_norm = 2 * tol  # Criterion

        def loss(beta):
            return -_compute_poissreg_loglike(endog, offsets, exog, beta)

        while i < n_iter_max and grad_norm > tol:
            grads = grad(loss)(beta)
            updates, opt_state = optimizer.update(grads, opt_state)
            beta = optax.apply_updates(beta, updates)
            grad_norm = jnp.linalg.norm(grads)
            i += 1

        self._beta = beta

    @property
    def beta(self):
        """Coef of the Poisson regression."""
        return self._beta


def _init_components_poisson_model(endog: jnp.ndarray, rank: int) -> jnp.ndarray:
    """
    Initialization for components for the PlnPCA model. Get a first guess for covariance
    that is easier to estimate and then takes the rank largest eigenvectors to get components.

    Parameters
    ----------
    endog : jnp.ndarray
        Samples with size (n,p)
    rank : int
        The dimension of the latent space, i.e. the reduced dimension.

    Returns
    -------
    jnp.ndarray
        Initialization of components of size (p,rank)
    """
    log_y = jnp.log(endog + (endog == 0) * math.exp(-2))
    max_dim = min(rank, endog.shape[0])
    pca = PCA(n_components=max_dim)
    pca.fit(np.array(log_y))
    pca_comp = pca.components_.T * np.sqrt(pca.explained_variance_)
    if rank > max_dim:
        nb_missing = rank - max_dim
        adding = np.random.randn(endog.shape[1], nb_missing) / rank
        pca_comp = np.concatenate((pca_comp, adding), axis=1)
    return jnp.array(pca_comp)


def _init_components_binomial_model(
    endog: jnp.ndarray, rank: int, n_trials: int
) -> jnp.ndarray:
    """
    Initialization for components for the Binomial PCA model. Get a first guess for covariance
    that is easier to estimate and then takes the rank largest eigenvectors to get components.

    Parameters
    ----------
    endog : jnp.ndarray
        Samples with size (n,p)
    rank : int
        The dimension of the latent space, i.e. the reduced dimension.
    n_trials : int
        The number of trials assumed in the Binomial model.

    Returns
    -------
    jnp.ndarray
        Initialization of components of size (p,rank)
    """
    _endog = endog + (endog == 0) * math.exp(-2) - (endog == n_trials) * math.exp(-2)
    normalized_y = _endog / n_trials
    logit_y = logit(normalized_y)
    max_dim = min(rank, endog.shape[0])
    pca = PCA(n_components=max_dim)
    pca.fit(np.array(logit_y))
    pca_comp = pca.components_.T * np.sqrt(pca.explained_variance_)
    if rank > max_dim:
        nb_missing = rank - max_dim
        adding = np.random.randn(endog.shape[1], nb_missing) / rank
        pca_comp = np.concatenate((pca_comp, adding), axis=1)
    return jnp.array(pca_comp)


def _compute_binreg_loglike(
    endog: jnp.ndarray,
    offsets: jnp.ndarray,
    exog: jnp.ndarray,
    coef: jnp.ndarray,
    n_trials: int,
) -> jnp.ndarray:
    """
    Compute the log likelihood of a Binomial regression model.

    Parameters
    ----------
    endog : jnp.ndarray
        The dependent variable of shape (n_samples, n_features).
    offsets : jnp.ndarray
        The offset term of shape (n_samples, n_features).
    exog : jnp.ndarray
        The exog of shape (n_samples, n_exog).
    coef : jnp.ndarray
        The regression coefficients of shape (n_exog, n_features).

    Returns
    -------
    jnp.ndarray
        The log likelihood of the Binomial regression model.
    """
    offsets_exog_coef = offsets + jnp.matmul(exog, coef)
    jax_lpmf = logpmf(endog, n_trials, sigmoid(offsets_exog_coef))
    return jnp.sum(jax_lpmf)


class _MBinomialRegression:
    """Multivariate Binomial Regression."""

    def __init__(self, n_trials) -> None:
        self._coef: Optional[jnp.ndarray] = None
        self._n_trials = n_trials

    def fit(
        self,
        endog: jnp.ndarray,
        exog: jnp.ndarray,
        offsets: jnp.ndarray,
    ) -> None:
        """
        Fit the Binomial regression model to the given data.

        Parameters
        ----------
        endog : jnp.ndarray
            The dependent variable of shape (n_samples, n_features).
        exog : jnp.ndarray
            The exog of shape (n_samples, n_exog).
        offsets : jnp.ndarray
            The offset term of shape (n_samples, n_features).
        """
        n_iter_max = 300
        tol = 0.001
        coef = jnp.array(np.random.rand(exog.shape[1], endog.shape[1]))
        optimizer = optax.rprop(learning_rate=0.005)
        opt_state = optimizer.init(coef)
        i = 0
        grad_norm = 2 * tol  # Criterion

        def loss(coef):
            return -_compute_binreg_loglike(endog, offsets, exog, coef, self._n_trials)

        while i < n_iter_max and grad_norm > tol:
            grads = grad(loss)(coef)
            updates, opt_state = optimizer.update(grads, opt_state)
            coef = optax.apply_updates(coef, updates)
            grad_norm = jnp.mean(grads**2)
            i += 1

        self._coef = coef

    @property
    def coef(self):
        """Coefficient of the Multivariate Binomial regression."""
        return self._coef
