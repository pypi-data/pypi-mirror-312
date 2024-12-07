import numpy as np

from scud.base import BaseModel
from scud.linkfunctions import linear_with_offsets


class _PCA(BaseModel):
    _nb_exog = None

    def _init_arguments(self):
        super()._init_arguments()
        if not self._additional_data:
            self._nb_exog = 1
        else:
            self._nb_exog = self._additional_data["exog"].shape[1]

    @property
    def nb_exog(self):
        """Number of exogenous variable in the model."""
        return self._nb_exog

    @property
    def coef(self):
        """The coefficient in the regression."""
        return self._params["coef"]

    @property
    def components(self):
        """The components in the PCA."""
        return self._params["components"]

    @property
    def covariance(self):
        """The covariance of the model."""
        return self.components @ (self.components.T)

    def _get_init_params(self):
        coef = np.random.rand(self.nb_exog, self.dim)
        components = np.random.randn(self.dim, self.latent_dimension)
        return {"coef": coef, "components": components}

    def link_function(self, x, params, additional_data):
        """
        Linear link function with offsets.
        """
        return linear_with_offsets(x, params=params, additional_data=additional_data)
