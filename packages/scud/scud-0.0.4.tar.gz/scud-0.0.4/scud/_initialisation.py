from typing import Optional
import math

import numpy as np
import jax.numpy as jnp
from jax.scipy.stats.binom import logpmf
from jax.scipy.special import logit
from jax.nn import sigmoid
from jax import grad
import torch
from sklearn.decomposition import PCA
import optax


if torch.cuda.is_available():
    DEVICE = "cuda:0"
else:
    DEVICE = "cpu"


def _compute_poissreg_loglike(
    endog: torch.Tensor, offsets: torch.Tensor, exog: torch.Tensor, coef: torch.Tensor
) -> torch.Tensor:
    """
    Compute the log likelihood of a Poisson regression model.

    Parameters
    ----------
    endog : torch.Tensor
        The dependent variable of shape (n_samples, n_features).
    offsets : torch.Tensor
        The offset term of shape (n_samples, n_features).
    exog : torch.Tensor
        The exog of shape (n_samples, n_exog).
    coef : torch.Tensor
        The regression coefficients of shape (n_exog, n_features).

    Returns
    -------
    torch.Tensor
        The log likelihood of the Poisson regression model.

    """
    exog_coef = torch.matmul(exog.unsqueeze(1), coef.unsqueeze(0)).squeeze()
    return torch.sum(
        -torch.exp(offsets + exog_coef) + torch.multiply(endog, offsets + exog_coef)
    )


class _PoissonReg:
    """
    Poisson regression model.

    Attributes
    ----------
    coef : torch.Tensor
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
        self._beta: Optional[torch.Tensor] = None

    def fit(
        self,
        endog: torch.Tensor,
        exog: torch.Tensor,
        offsets: torch.Tensor,
    ) -> None:
        """
        Fit the Poisson regression model to the given data.

        Parameters
        ----------
        endog : torch.Tensor
            The dependent variable of shape (n_samples, n_features).
        exog : torch.Tensor
            The exog of shape (n_samples, n_exog).
        offsets : torch.Tensor
            The offset term of shape (n_samples, n_features).
        """
        n_iter_max = 300
        tol = 0.001
        lr = 0.005
        beta = torch.rand(
            (exog.shape[1], endog.shape[1]), requires_grad=True, device=DEVICE
        )
        endog = endog.to(DEVICE)
        exog = exog.to(DEVICE)
        offsets = offsets.to(DEVICE)
        optimizer = torch.optim.Rprop([beta], lr=lr)
        i = 0
        grad_norm = 2 * tol  # Criterion
        while i < n_iter_max and grad_norm > tol:
            loss = -_compute_poissreg_loglike(endog, offsets, exog, beta)
            loss.backward()
            optimizer.step()
            grad_norm = torch.norm(beta.grad)
            beta.grad.zero_()
            i += 1
        self._beta = beta

    @property
    def beta(self):
        """Coef of the Poisson regression."""
        return self._beta


def _init_components_poisson_model(endog: torch.Tensor, rank: int) -> torch.Tensor:
    """
    Initialization for components for the PlnPCA model. Get a first guess for covariance
    that is easier to estimate and then takes the rank largest eigenvectors to get components.

    Parameters
    ----------
    endog : torch.Tensor
        Samples with size (n,p)
    rank : int
        The dimension of the latent space, i.e. the reduced dimension.

    Returns
    -------
    torch.Tensor
        Initialization of components of size (p,rank)
    """
    log_y = torch.log(endog + (endog == 0) * math.exp(-2))
    max_dim = min(rank, endog.shape[0])
    pca = PCA(n_components=max_dim)
    pca.fit(log_y.cpu().detach())
    pca_comp = pca.components_.T * np.sqrt(pca.explained_variance_)
    if rank > max_dim:
        nb_missing = rank - max_dim
        adding = np.random.randn(endog.shape[1], nb_missing) / rank
        pca_comp = np.concatenate((pca_comp, adding), axis=1)
    return pca_comp


def _init_components_binomial_model(
    endog: torch.Tensor, rank: int, n_trials: int
) -> torch.Tensor:
    """
    Initialization for components for the Binomial PCA model. Get a first guess for covariance
    that is easier to estimate and then takes the rank largest eigenvectors to get components.

    Parameters
    ----------
    endog : torch.Tensor
        Samples with size (n,p)
    rank : int
        The dimension of the latent space, i.e. the reduced dimension.
    n_trials : int
        The number of trials assumed in the Binomial model.

    Returns
    -------
    torch.Tensor
        Initialization of components of size (p,rank)
    """
    _endog = endog + (endog == 0) * math.exp(-2) - (endog == n_trials) * math.exp(-2)
    normalized_y = _endog / n_trials
    logit_y = logit(normalized_y)
    max_dim = min(rank, endog.shape[0])
    pca = PCA(n_components=max_dim)
    pca.fit(logit_y)
    pca_comp = pca.components_.T * np.sqrt(pca.explained_variance_)
    if rank > max_dim:
        nb_missing = rank - max_dim
        adding = np.random.randn(endog.shape[1], nb_missing) / rank
        pca_comp = np.concatenate((pca_comp, adding), axis=1)
    return pca_comp


def _compute_binreg_loglike(
    endog: torch.Tensor,
    offsets: torch.Tensor,
    exog: torch.Tensor,
    coef: torch.Tensor,
    n_trials: int,
) -> jnp.ndarray:
    """
    Compute the log likelihood of a Poisson regression model.

    Parameters
    ----------
    endog : torch.Tensor
        The dependent variable of shape (n_samples, n_features).
    offsets : torch.Tensor
        The offset term of shape (n_samples, n_features).
    exog : torch.Tensor
        The exog of shape (n_samples, n_exog).
    coef : torch.Tensor
        The regression coefficients of shape (n_exog, n_features).

    Returns
    -------
    torch.Tensor
        The log likelihood of the Poisson regression model.

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
        coef = np.random.rand(exog.shape[1], endog.shape[1])
        optim = optax.rprop(learning_rate=0.005)
        dict_coef = {"coef": coef}
        opt_state = optim.init(dict_coef)
        i = 0
        grad_norm = 2 * tol  # Criterion

        def loss(dict_x):
            return -_compute_binreg_loglike(
                endog, offsets, exog, dict_x["coef"], self._n_trials
            )

        while i < n_iter_max and grad_norm > tol:
            grads = grad(loss)(dict_coef)
            updates, opt_state = optim.update(grads, opt_state)
            dict_coef = optax.apply_updates(dict_coef, updates)
            grad_norm = jnp.mean(grads["coef"] ** 2)
            i += 1

        self._coef = coef

    @property
    def coef(self):
        """Coefficient of the Multivariate Binomial regression."""
        return self.coef
