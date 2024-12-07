from abc import ABC, abstractmethod
from typing import Optional, Dict, Union


import numpy as np
import torch
import pandas as pd
import jax.numpy as jnp
from jax import random
from jax.typing import ArrayLike

from scud.inverse_parameter_mappings import poisson_mapping, binomial_mapping
from scud.linkfunctions import linear_with_offsets
from scud._utils import _format_dict_of_array, _add_doc, _vmap_all_but_params


COMPONENT_KEY = "components"
COV_KEY = "exog"
COEF_KEY = "coef"
OFFSETS_KEY = "offsets"


class BaseSampler(ABC):
    """An abstract class used to simulate data from a model."""

    def __init__(
        self,
        n_samples: int,
        latent_dimension: int,
        params: Dict[str, Union[torch.Tensor, np.ndarray, jnp.ndarray, pd.DataFrame]],
        additional_data: Optional[
            Dict[str, Union[torch.Tensor, np.ndarray, pd.DataFrame, jnp.ndarray]]
        ] = None,
    ):
        """
        Instantiate the model with the data given.

        Parameters
        ----------
        n_samples : int
            Number of samples.
        latent_dimension : int
            Latent dimension.
        params : dict
            Model parameters. Each item should be one of
            [torch.Tensor, np.ndarray, jnp.ndarray, pd.DataFrame]
        additional_data : dict, optional
            Additional data, by default None. Each item should be one of
            [torch.Tensor, np.ndarray, jnp.ndarray, pd.DataFrame]

        """
        self._n_samples: int = n_samples
        self._latent_dimension: int = latent_dimension
        self._additional_data: Dict[str, np.ndarray] = _format_dict_of_array(
            additional_data
        )
        self._params: Dict[str, np.ndarray] = _format_dict_of_array(params)

    def sample(self, seed: int = 0) -> jnp.ndarray:
        """
        Generate samples from the model.

        Parameters
        ----------
        seed : int, optional
            Seed for random number generation, by default 0.

        Returns
        -------
        np.ndarray
            Generated samples.
        """
        key = random.PRNGKey(seed)
        gaussian = random.normal(key=key, shape=(self.n_samples, self.latent_dimension))

        parameter = self.vmap_link_function(
            gaussian, params=self.params, additional_data=self._additional_data
        )

        return self.sample_from_parameter(parameter=parameter, key=key)

    @property
    def n_samples(self) -> int:
        """Number of samples."""
        return self._n_samples

    @property
    def latent_dimension(self) -> int:
        """Latent dimension."""
        return self._latent_dimension

    @property
    def params(self) -> Dict[str, np.ndarray]:
        """Method for the parameters of the model."""
        return self._params

    @property
    def additional_data(self) -> Dict[str, jnp.ndarray]:
        """Method for the additional data."""
        return self._additional_data

    @abstractmethod
    def inverse_parameter_mapping(self, x: jnp.ndarray) -> jnp.ndarray:
        """The inverse parameter mapping of the model."""

    @abstractmethod
    def link_function(
        self, x: jnp.ndarray, params: dict, additional_data: dict
    ) -> jnp.ndarray:
        """The link function of the model."""

    @abstractmethod
    def sample_from_parameter(
        self, parameter: jnp.ndarray, key: ArrayLike
    ) -> jnp.ndarray:
        """
        Sample from the distribution of the model given the parameter.

        Parameters
        ----------
        parameter : jax.numpy.ndarray
            Parameter values.
        key : KeyArrayLike
            Random key for sampling.

        Returns
        -------
        jax.numpy.ndarray
            Sampled values.
        """

    def vmap_link_function(
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
            Additional data.

        Returns
        -------
        jax.numpy.ndarray
            Vectorized output values from the link function.
        """
        return _vmap_all_but_params(self.link_function, x, params, additional_data)


class PCAsampler(BaseSampler, ABC):
    """Simulation according to a Principal Component Analysis based model."""

    @classmethod
    def from_dict(cls, dict_params_and_additional_data, **kwargs):
        """
        Create an instance of PCAsampler from a dictionary of parameters and additional data.

        Parameters
        ----------
        dict_params_and_additional_data : dict
            Dictionary containing components, coef, exog, and offsets.
            Each item should be one of
            [torch.Tensor, np.ndarray, jnp.ndarray, pd.DataFrame]
        **kwargs : additional keyword arguments
            Additional arguments for the constructor.

        Raises
        ------
        ValueError
            If the dict does not contain the
            keys "components", "exog", "coef", "offsets".

        Returns
        -------
        PCAsampler
            Instance of PCAsampler created from the provided dictionary.
        """
        for key in [COMPONENT_KEY, COV_KEY, OFFSETS_KEY, COEF_KEY]:
            if key not in dict_params_and_additional_data.keys():
                raise ValueError(f"'{key}' should be in the dictionnary keys.")

        latent_dim = dict_params_and_additional_data[COMPONENT_KEY].shape[1]
        params = {
            COMPONENT_KEY: dict_params_and_additional_data[COMPONENT_KEY],
            COEF_KEY: dict_params_and_additional_data[COEF_KEY],
        }
        additional_data = {
            OFFSETS_KEY: dict_params_and_additional_data[OFFSETS_KEY],
            COV_KEY: dict_params_and_additional_data[COV_KEY],
        }
        n_samples = additional_data[OFFSETS_KEY].shape[0]
        return cls(
            n_samples=n_samples,
            latent_dimension=latent_dim,
            params=params,
            additional_data=additional_data,
            **kwargs,
        )

    @property
    def offsets(self) -> jnp.ndarray:
        """Offsets of the model"""
        return self._additional_data[OFFSETS_KEY]

    @property
    def exog(self) -> jnp.ndarray:
        """Covariates of the model"""
        return self._additional_data[COV_KEY]

    @property
    def components(self) -> jnp.ndarray:
        """Components of the model."""
        return self.params[COMPONENT_KEY]

    @property
    def coef(self) -> jnp.ndarray:
        """Coef of the model."""
        return self.params[COEF_KEY]

    @property
    def covariance(self) -> jnp.ndarray:
        """Covariance matrix of the model."""
        return self.components @ (self.components.T)

    def link_function(
        self,
        x: jnp.ndarray,
        params: Dict[str, Union[torch.Tensor, np.ndarray, jnp.ndarray, pd.DataFrame]],
        additional_data: Dict[
            str, Union[torch.Tensor, np.ndarray, jnp.ndarray, pd.DataFrame]
        ],
    ) -> jnp.ndarray:
        """
        Linear link function.

        Parameters
        ----------
        x : jax.numpy.ndarray
            Input values.
        params : dict
            Model parameters. Each item should be one of
            [torch.Tensor, np.ndarray, jnp.ndarray, pd.DataFrame]
        additional_data : dict
            Additional data. Each item should be one of
            [torch.Tensor, np.ndarray, jnp.ndarray, pd.DataFrame]

        Returns
        -------
        jax.numpy.ndarray
            Output values from the linear link function.
        """
        return linear_with_offsets(x, params=params, additional_data=additional_data)


class PlnPCAsampler(PCAsampler):
    """Simulation according to a Poisson Log-Normal Principal Component Analysis model."""

    def inverse_parameter_mapping(self, x: jnp.ndarray) -> jnp.ndarray:
        """
        Poisson mapping. See wikipédia

        Parameters
        ----------
        x : jax.numpy.ndarray
            Input values.

        Returns
        -------
        jax.numpy.ndarray
            Inverse parameter mapping of the model.
        """
        return poisson_mapping(x)

    @_add_doc(BaseSampler)
    def sample_from_parameter(
        self, parameter: jnp.ndarray, key: ArrayLike
    ) -> jnp.ndarray:
        return random.poisson(key=key, lam=self.inverse_parameter_mapping(parameter))


class BinomialPCAsampler(PCAsampler):
    """Simulation according to a Binomial Principal Component Analysis model."""

    def __init__(
        self,
        n_samples: int,
        latent_dimension: int,
        nb_trials: int,
        params: Dict[str, Union[torch.Tensor, np.ndarray, jnp.ndarray, pd.DataFrame]],
        additional_data: Optional[
            Dict[str, Union[torch.Tensor, np.ndarray, pd.DataFrame, jnp.ndarray]]
        ] = None,
    ):  # pylint: disable=too-many-arguments,too-many-positional-arguments
        super().__init__(
            n_samples=n_samples,
            latent_dimension=latent_dimension,
            params=params,
            additional_data=additional_data,
        )
        self.nb_trials: int = nb_trials

    @classmethod
    def from_dict(
        cls, dict_params_and_additional_data, nb_trials: int
    ):  # pylint: disable=arguments-differ
        """
        Create an instance of BinomialPCAsampler from a dictionary of
        parameters and additional data.

        Parameters
        ----------
        dict_params_and_additional_data : dict
            Dictionary containing components, coef, exog, and offsets.
        nb_trials : int
            Number of trials for binomial sampling.

        Returns
        -------
        BinomialPCAsampler
            Instance of BinomialPCAsampler created from the provided dictionary.
        """
        return super().from_dict(dict_params_and_additional_data, nb_trials=nb_trials)

    def inverse_parameter_mapping(self, x: np.ndarray) -> np.ndarray:
        """
        Inverse parameter mapping for binomial distribution.

        Parameters
        ----------
        x : jax.numpy.ndarray
            Input values.

        Returns
        -------
        jax.numpy.ndarray
            Inverse parameter mapping of the model.
        """
        return binomial_mapping(x)

    @_add_doc(BaseSampler)
    def sample_from_parameter(
        self, parameter: np.ndarray, key: ArrayLike
    ) -> np.ndarray:
        return random.binomial(
            key=key, n=self.nb_trials, p=self.inverse_parameter_mapping(parameter)
        )
