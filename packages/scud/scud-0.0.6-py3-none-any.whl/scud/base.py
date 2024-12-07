from abc import ABC, abstractmethod
from typing import Optional, Dict, Union

import math
import numpy as np
import optax
import pandas as pd
import torch
import jax.numpy as jnp
from sklearn.decomposition import PCA
from jax import grad, hessian, vmap
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt

from scud._utils import (
    _format_data,
    _format_dict_of_array,
    _log_unit_gaussian_density,
    _sample_gaussians,
    _vmap_all_but_params,
    _vmap_only_x,
    _vvmap_log_gaussian_density,
)
from scud._weights import _get_normalized_weights_const_and_weights

DELTA = 0.1


class BaseModel(ABC):
    """Implements all the features that can be shared across models."""

    def __init__(
        self,
        data: Union[torch.Tensor, np.ndarray, pd.DataFrame, jnp.ndarray],
        *,
        latent_dimension: int,
        additional_data: Optional[
            Dict[str, Union[torch.Tensor, np.ndarray, pd.DataFrame, jnp.ndarray]]
        ] = None,
        alpha: float = 0.001,
    ):
        """
        Init the model.
        Parameters
        ----------
        data: torch.Tensor or np.ndarray or pd.DataFrame or jnp.ndarray
            The input array on which doing dimension reduction.
        latent_dimension: int (keyword-only)
            The reduced dimension.
        additional_data:dict[str,Union[torch.Tensor,np.ndarray,pd.DataFrame,jnp.ndarray]](kw-only)
            Optional dictionnary with additional data such as covariates or offsets. Each item
            should be either a torch.Tensor or np.ndarray or pd.DataFrame or jnp.ndarray.
            Default to None.
        alpha : float
            The parameter of the mixture between the best proposal and the
            defensive proposal. Should be between 0 and 1. Default to 0.001
        Returns
        -------
        An instance of the BaseModel class. Cannot be instantiated.
        """
        self._data = _format_data(data)
        self._aux_var = {
            "latent_dimension": latent_dimension,
            "nb_particles": None,
            "loglike_list": [],
            "selected_indices": None,
            "batch_size": None,
            "alpha": None,
        }
        self._additional_data = (
            _format_dict_of_array(additional_data)
            if additional_data is not None
            else {}
        )
        self._init_arguments()
        self._params = self._get_init_params()
        self._gaussian_params = {
            "mean_prop": None,
            "var_prop": None,
            "sqrt_var_prop": None,
        }
        self._particles = None
        self._aux_var["alpha"] = alpha

    @property
    def exog(self):
        """The exogenous variable in the model."""
        return (
            self._additional_data.get("exog", 0)
            if self._additional_data is not None
            else jnp.zeros((self.n_samples, 1))
        )

    @property
    def offsets(self):
        """The offsets in the model."""
        return (
            self._additional_data.get("offsets", 0)
            if self._additional_data is not None
            else jnp.zeros_like(self._data)
        )

    @property
    def n_samples(self):
        """the number of samples in the dataset (number of lines of the given data)"""
        return self._aux_var["n_samples"]

    @property
    def dim(self):
        """Number of variables of data."""
        return self._aux_var["dim"]

    @property
    def _selected_indices(self):
        return self._aux_var["selected_indices"]

    @property
    def _alpha(self):
        return self._aux_var["alpha"]

    @property
    def _batch_size(self):
        return self._aux_var["batch_size"]

    @property
    def _current_batch_size(self):
        return len(self._selected_indices)

    @property
    def _nb_batch(self):
        return self._aux_var["nb_batch"]

    @property
    def latent_dimension(self):
        """The latent dimension of the model"""
        return self._aux_var["latent_dimension"]

    @property
    def nb_particles(self):
        """Number of particles used for the Monte Carlo approximation."""
        return self._aux_var["nb_particles"]

    @property
    def particles(self):
        """The particles used for Monte Carlo approximation."""
        return self._particles

    @property
    def _batch_particles(self):
        return self._particles[:, self._selected_indices]

    @property
    def _batch_data(self):
        return self._data[self._selected_indices]

    @property
    def _batch_additional_data(self):
        batch_dict = {}
        for key, items in self._additional_data.items():
            batch_dict[key] = items[self._selected_indices]
        return batch_dict

    @property
    def mean_prop(self):
        """The mean of the proposal."""
        return self._gaussian_params["mean_prop"]

    @property
    def _batch_mean_prop(self):
        return self.mean_prop[self._selected_indices]

    @property
    def var_prop(self):
        """The variance of the proposal."""
        return self._gaussian_params["var_prop"]

    @property
    def _sqrt_var_prop(self):
        """The variance of the proposal."""
        return self._gaussian_params["sqrt_var_prop"]

    @property
    def _batch_var_prop(self):
        return self.var_prop[self._selected_indices]

    @property
    def _batch_sqrt_var_prop(self):
        return self._sqrt_var_prop[self._selected_indices]

    def _vmap_link_function(
        self, x: jnp.ndarray, params: dict, additional_data: dict
    ) -> jnp.ndarray:
        """
        Vectorized map of the link function.

        Parameters
        ----------
        x : jax.numpy.ndarray
            Input values.
        params : dict
            Model parameters.
        additional_data : dict
            Additional data such as covariates or offsets.

        Returns
        -------
        jax.numpy.ndarray
            Vectorized output values from the link function.
        """
        return _vmap_all_but_params(self.link_function, x, params, additional_data)

    def _vvmap_link_function(
        self, x: jnp.ndarray, *, params: dict, additional_data: dict
    ) -> jnp.ndarray:
        """
        Doubly Vectorized vectorized map of the link function.

        Parameters
        ----------
        x : jax.numpy.ndarray
            Input values.
        params : dict (keyword-only)
            Model parameters.
        additional_data : dict (keyword-only)
            Additional data.

        Returns
        -------
        jax.numpy.ndarray
            Doubly vectorized output values from the link function.
        """
        return _vmap_only_x(self._vmap_link_function, x, params, additional_data)

    def _hessian_w_complete_loglike(self, data, x, params, additional_data):
        return hessian(self._complete_loglike, argnums=1)(
            data, x, params, additional_data
        )

    def _vmap_hessian_w_complete_loglike(self, data, x, params, additional_data):
        return vmap(
            self._hessian_w_complete_loglike,
            in_axes=(
                0,
                0,
                {key: None for key in params.keys()},
                {key: 0 for key in additional_data.keys()},
            ),
        )(data, x, params, additional_data)

    def _complete_loglike(self, data, x, params, additional_data):
        """Computes the complete log likelihood of the model."""
        return self._log_conditional_y_w(
            data, x, params, additional_data
        ) + _log_unit_gaussian_density(x)

    def _vmap_complete_loglike(self, data, x, params, additional_data):
        """
        Computes the complete log likelihood of the model vectorized
        one time.
        """
        parameter = self._vmap_link_function(
            x, params=params, additional_data=additional_data
        )
        log_unit_gauss = _log_unit_gaussian_density(x)
        return self._log_nef(data, parameter) + log_unit_gauss

    def _log_nef(self, data, parameter):
        """log density of the Natural Exponential Family."""
        log_partition_parameter = self.log_partition(parameter)
        return jnp.sum(
            data * parameter - log_partition_parameter - self.log_normalizer(data),
            axis=-1,
        )

    def _log_conditional_y_w(self, data, x, params, additional_data):
        """Log conditional of Y given W"""
        parameter = self.link_function(
            x, params=params, additional_data=additional_data
        )
        return jnp.sum(self._log_nef(data, parameter))

    def _grad_theta_log_conditional_y_w(self, data, x, params, additional_data):
        """Derivative with respect to theta of the conditional."""
        return grad(self._log_conditional_y_w, argnums=2)(
            data, x, params, additional_data
        )

    def _vmap_grad_theta_log_conditional_y_w(self, data, x, params, additional_data):
        """Derivative with respect to theta of the log conditional Y given W vectorized."""
        return vmap(
            self._grad_theta_log_conditional_y_w,
            in_axes=(
                0,
                0,
                {key: None for key in params.keys()},
                {key: 0 for key in additional_data.keys()},
            ),
        )(data, x, params, additional_data)

    def _vvmap_grad_theta_log_conditional_y_w(self, data, x, params, additional_data):
        """Doubly vectorized derivate with respect to theta of the log conditional Y given W"""
        return vmap(
            self._vmap_grad_theta_log_conditional_y_w,
            in_axes=(
                None,
                0,
                {key: None for key in params.keys()},
                {key: None for key in additional_data.keys()},
            ),
        )(data, x, params, additional_data)

    def _grad_w_complete_loglike(self, data, x, params, additional_data):
        return grad(self._complete_loglike, argnums=1)(data, x, params, additional_data)

    def _vvmap_conditional(self, data, x, params, additional_data):
        parameter = self._vvmap_link_function(
            x, params=params, additional_data=additional_data
        )
        return self._log_nef(data, parameter)

    def _vvmap_complete_loglike(self, data, x, params, additional_data):
        """Computes the doubly vectorized complete log likelihood of the model."""
        return self._vvmap_conditional(
            data, x, params, additional_data
        ) + _log_unit_gaussian_density(x)

    def transform(self):
        """Transforms data."""
        return self._vmap_link_function(
            self.mean_prop, params=self._params, additional_data=self._additional_data
        )

    def _get_loglike(self, weights, const):
        per_sample_loglike = jnp.log(jnp.mean(weights, axis=0)) + const
        return jnp.mean(per_sample_loglike, axis=0)

    def _snis_estimator(self, grad_params, normalized_weights):
        normalized_weights = jnp.expand_dims(normalized_weights, (2, 3))
        for key in grad_params.keys():
            grad_params[key] *= normalized_weights
            grad_params[key] = -jnp.sum(grad_params[key], axis=(0, 1))
        return grad_params

    def fit(
        self,
        *,
        nb_particles: int = 30,
        nb_max_gradients: int = -1,
        batch_size: int = None,
        nb_epoch: int = 100,
    ):
        """
        Fits the data with gradient ascent via self-normalized estimated gradients.

        Parameters
        ----------
        nb_particles : int (optional, keyword-only)
            The number of particles used for Monte Carlo
            approximation. default to 30.

        nb_max_gradients: int (optional, keyword-only)
            The maximum number of gradients to compute.
            One epoch computes n_samples gradients. If -1,
            will do only nb_epoch and not look at the number of gradients computed.
            Default to -1.

        batch_size: int (optional, keyword-only)
            The batch size used. If None, will take the number of samples.
            Default to None.

        nb_epoch: int (optional, keyword-only)
            The number of epoch to perform. If nb_max_gradients is lower
            than n_samples * nb_epoch, it will stop before the nb_epoch epoch is done.
            Default to 100.
        """
        optim = self._handle_batch_size_and_get_optim(batch_size)
        self._aux_var["nb_particles"] = nb_particles
        self._init_proposal_and_particles()
        self._print_fit_info()
        opt_state = optim.init(self._params)
        nb_epoch_done = 0
        nb_gradients_computed = 0
        nb_max_gradients = np.inf if nb_max_gradients == -1 else nb_max_gradients
        pbar = tqdm(desc="while loop", total=nb_epoch)
        while nb_epoch_done < nb_epoch and nb_gradients_computed < nb_max_gradients:
            loglike = 0
            for selected_indices in self._get_indices_per_batch():
                self._aux_var["selected_indices"] = selected_indices
                self._estimate_proposal()
                self._sample_particles()
                current_loglike, opt_state = self._step(optim, opt_state)
                loglike += current_loglike
                nb_gradients_computed += self._current_batch_size
            self._aux_var["loglike_list"].append(float(loglike / self._nb_batch))
            nb_epoch_done += 1
            pbar.update(1)

    def _print_fit_info(self):
        print(
            f"Start fitting the {self._full_model_name} model with {self.latent_dimension} PCs, "
            f"{self.nb_particles} particles and a batch size of {self._batch_size} out of "
            f"{self.n_samples} samples."
        )

    def _handle_batch_size_and_get_optim(self, batch_size):
        self._aux_var["batch_size"] = (
            batch_size if batch_size is not None else self.n_samples
        )
        if self._batch_size < self.n_samples:
            optim = optax.adam(learning_rate=0.01)
        else:
            optim = optax.rprop(learning_rate=0.01)
        nb_full_batch = self.n_samples // self._batch_size
        last_batch_size = self.n_samples % self._batch_size
        self._aux_var["nb_batch"] = nb_full_batch + (last_batch_size > 0)
        return optim

    def _get_indices_per_batch(self, shuffle=False):
        indices = np.arange(self.n_samples)
        if shuffle is True:
            np.random.shuffle(indices)

        for i in range(self._nb_batch):
            yield indices[i * self._batch_size : (i + 1) * self._batch_size]

    def _step(self, optim, opt_state):
        (
            normalized_weights,
            const,
            weights,
        ) = self._get_updated_normalized_weights_const_and_weights()
        loglike = self._get_loglike(weights, const)

        grad_params = self._vvmap_grad_theta_log_conditional_y_w(
            self._batch_data,
            self._batch_particles,
            self._params,
            self._batch_additional_data,
        )
        grad_params = self._snis_estimator(grad_params, normalized_weights)
        updates, opt_state = optim.update(grad_params, opt_state)
        self._params = optax.apply_updates(self._params, updates)
        return loglike, opt_state

    def _find_mode(self):
        optim = optax.rprop(0.01)

        def loss(optax_param):
            return -jnp.sum(
                self._vmap_complete_loglike(
                    self._batch_data,
                    optax_param["gaussian"],
                    self._params,
                    self._batch_additional_data,
                )
            )

        optax_params = {
            "gaussian": jnp.zeros((self._current_batch_size, self.latent_dimension))
        }
        opt_state = optim.init(optax_params)
        for _ in range(45):
            grads = grad(loss)(optax_params)
            updates, opt_state = optim.update(grads, opt_state)
            optax_params = optax.apply_updates(optax_params, updates)
        return optax_params["gaussian"]

    def _estimate_proposal(self):
        (
            normalized_weights,
            _,
            _,
        ) = self._get_updated_normalized_weights_const_and_weights()
        expectation_mean = jnp.sum(
            jnp.expand_dims(normalized_weights, 2) * self._batch_particles, axis=0
        )
        self._gaussian_params["mean_prop"] = (
            self._gaussian_params["mean_prop"]
            .at[self._selected_indices]
            .set(expectation_mean)
        )
        best_var = self._get_hessian()
        sqrt_best_var = jnp.linalg.cholesky(best_var)
        self._gaussian_params["var_prop"] = (
            self._gaussian_params["var_prop"].at[self._selected_indices].set(best_var)
        )
        self._gaussian_params["sqrt_var_prop"] = (
            self._gaussian_params["sqrt_var_prop"]
            .at[self._selected_indices]
            .set(sqrt_best_var)
        )

    def _get_hessian(self):
        _hessian = self._vmap_hessian_w_complete_loglike(
            self._batch_data,
            self._batch_mean_prop,
            self._params,
            self._batch_additional_data,
        )
        return jnp.linalg.inv(-_hessian)

    def _get_updated_normalized_weights_const_and_weights(self):
        log_num = self._get_log_numerator()
        log_denom = self._get_log_denominator()
        return _get_normalized_weights_const_and_weights(log_num, log_denom)

    def _get_log_numerator(self):
        return self._vvmap_complete_loglike(
            self._batch_data,
            self._batch_particles,
            self._params,
            self._batch_additional_data,
        )

    def _get_log_denominator(self):
        best_log_density = _vvmap_log_gaussian_density(
            self._batch_particles, self._batch_mean_prop, self._batch_var_prop
        )
        if self._alpha == 0:
            return best_log_density
        batch_identity = jnp.repeat(
            jnp.eye(self.latent_dimension)[None, :, :], self._current_batch_size, axis=0
        ) * (1 + DELTA)
        defensive_log_density = _vvmap_log_gaussian_density(
            self._batch_particles, self._batch_mean_prop, batch_identity
        )
        log_rapport_density = defensive_log_density - best_log_density
        log_rapport_alpha = math.log(self._alpha) + jnp.logaddexp(
            log_rapport_density,
            jnp.array([math.log(1 - self._alpha) - math.log(self._alpha)]),
        )
        return best_log_density + log_rapport_alpha

    def viz(self, colors=None, ax=None):
        """Visualize the latent variables."""
        transformed_data = self.transform()
        pca = PCA(n_components=2)
        proj_variables = pca.fit_transform(transformed_data)
        x = proj_variables[:, 0]
        y = proj_variables[:, 1]
        if ax is None:
            ax = plt.gca()
            to_show = True
        else:
            to_show = False
        sns.scatterplot(x=x, y=y, hue=colors, ax=ax, s=80)
        if to_show is True:
            plt.show()
        return ax

    def _init_proposal_and_particles(self):
        self._init_proposal()
        self._init_particles()

    def _init_proposal(self):
        self._gaussian_params["mean_prop"] = jnp.zeros(
            (self.n_samples, self.latent_dimension)
        )
        self._gaussian_params["var_prop"] = jnp.repeat(
            jnp.eye(self.latent_dimension)[None, :, :], self.n_samples, axis=0
        )
        self._gaussian_params["sqrt_var_prop"] = jnp.repeat(
            jnp.eye(self.latent_dimension)[None, :, :], self.n_samples, axis=0
        )

    def _sample_particles(self):
        best_one = _sample_gaussians(
            self.nb_particles,
            self._batch_mean_prop,
            self._batch_sqrt_var_prop,
        )
        batch_identity = jnp.repeat(
            jnp.eye(self.latent_dimension)[None, :, :], self._current_batch_size, axis=0
        ) * math.sqrt(1 + DELTA)
        defensive = _sample_gaussians(
            self.nb_particles, self._batch_mean_prop, batch_identity
        )
        prob = jnp.ones((self.nb_particles, self._current_batch_size)) * self._alpha
        bern = np.random.binomial(1, prob)[:, :, None] * 0
        self._particles = self._particles.at[:, self._selected_indices].set(
            (1 - bern) * best_one + bern * defensive
        )

    def _init_particles(self):
        self._particles = _sample_gaussians(
            self.nb_particles,
            self.mean_prop,
            self._sqrt_var_prop,
        )

    def _init_arguments(self):
        self._aux_var["n_samples"], self._aux_var["dim"] = self._data.shape

    @property
    @abstractmethod
    def _full_model_name(self):
        """The name that will be displayed at the beginning of the fit."""

    @abstractmethod
    def log_partition(self, x):
        """The log partition of the model."""

    @abstractmethod
    def link_function(self, x, params, additional_data):
        """The link function of the model."""

    @abstractmethod
    def log_normalizer(self, x):
        """Log normalizer that allows the density to integrate to 1."""

    @abstractmethod
    def _get_init_params(self):
        pass
