import jax.numpy as jnp

from scud.logpartitions import binomial_log_partition
from scud.lognormalizers import binomial_log_normalizer
from scud.pca import _PCA
from scud._initialisation import (
    _MBinomialRegression,
    _init_components_binomial_model,
)


class BinPCA(_PCA):
    """
    Binomial Principal Component Analysis. The log
    partitions is n*log(1 + exp(x)), the link function is the PCA while
    the log normalizer is log of binomial coefficients.
    """

    _n_max: int

    def log_partition(self, x):
        """Log partition that is n*log(1+ exp(x))."""
        return binomial_log_partition(x, self._n_max)

    def log_normalizer(self, x):
        """Log normalizer of a binomial law: log binomial coefficient."""
        return binomial_log_normalizer(x, self._n_max)

    def _init_arguments(self):
        super()._init_arguments()
        self._n_max = int(jnp.max(self._data))

    def _get_init_params(self):
        """
        Intialisation for the coefficients is done with a binomial regression.
        Intialisation for the components is done by a PCA on the logit of the normalized counts.
        """
        if self.exog is not None and isinstance(self.exog, jnp.ndarray):
            binreg = _MBinomialRegression(self._n_max)
            binreg.fit(
                self._data,
                self.exog,
                self.offsets,
            )
            coef = binreg.coef
        else:
            coef = jnp.zeros((self.nb_exog, self.dim))
        components = _init_components_binomial_model(
            self._data, self.latent_dimension, self._n_max
        )
        return {"coef": coef, "components": components}

    @property
    def _full_model_name(self):
        return f"Binomial(r = {self._n_max}) Component Analysis"
