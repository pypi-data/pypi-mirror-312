import jax.numpy as jnp

from scud.pca import _PCA
from scud.logpartitions import poisson_log_partition
from scud.lognormalizers import poisson_log_normalizer
from scud._initialisation import _PoissonReg, _init_components_poisson_model


class PlnPCA(_PCA):
    """
    Poisson Log-Normal Principal Component Analysis. The log
    partitions is the exponential, the link function is the PCA while
    the log normalizer is the log factorial.
    """

    def log_partition(self, x):
        """Exponential log partition."""
        return poisson_log_partition(x)

    def log_normalizer(self, x):
        """Log normalizer of a poisson law: log factorial."""
        return poisson_log_normalizer(x)

    def _get_init_params(self):
        if self.exog is not None and isinstance(self.exog, jnp.ndarray):
            poissreg = _PoissonReg()
            poissreg.fit(self._data, self.exog, self.offsets)
            coef = poissreg.beta
        else:
            coef = jnp.zeros((self.nb_exog, self.dim))
        components = _init_components_poisson_model(self._data, self.latent_dimension)
        return {"coef": coef, "components": components}

    @property
    def _full_model_name(self):
        return "Poisson Log-Normal Principal Component Analysis"
