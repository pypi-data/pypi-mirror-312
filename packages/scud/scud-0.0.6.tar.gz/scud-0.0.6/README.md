Package for Statistical Components for Underlying Dimensions.

# Installing
```
pip install scud
```

# Documentation
The documentation can be found [here](https://scud-422a9c.gitlab.io/).

# Getting Started

The getting started can be found [here](Getting_started.ipynb).


# Quick start

### Import package and load data

```
from scud import PlnPCA, BinPCA
from scud.data import load_scrna

data_and_labels = load_scrna(return_labels = True)
counts = data_and_labels['endog']
labels = data_and_labels['labels']
```

### Instantiate, fit the model and visualize the results for the Binomial PCA model

```
binpca = BinPCA(data = counts, latent_dimension = 5)
binpca.fit()
binpca.viz(colors = labels)
```

### Instantiate, fit the model and visualize the results for the Poisson-log Normal PCA model

```
plnpca = PlnPCA(data = counts, latent_dimension = 5)
plnpca.fit()
plnpca.viz(colors = labels)
```


## Supervised learning using labels

### One hot encode the labels

```
from sklearn.preprocessing import OneHotEncoder
import numpy as np

labels = np.array(labels).reshape(-1, 1)
encoder = OneHotEncoder()
exog = encoder.fit_transform(labels).toarray()
additional_data = {"exog": exog}
```


### Instantiate and fit the PlnPCA model
```
plnpca = PlnPCA(data = counts, latent_dimension = 5, additional_data = additional_data)
plnpca.fit()
plnpca.viz(colors = labels.reshape(-1))
```

### Instantiate and fit the BinPCA model

```
binpca = PlnPCA(data = counts, latent_dimension = 5, additional_data = additional_data)
binpca.fit()
binpca.viz(colors = labels.reshape(-1))
```


# CONTRIBUTING
You should run ``` pre-commit install ``` in the repo directory before commiting (if ```pre-commit``` is not installed,
you can pip install it). This will make sure each python file is well
formated and pylint will check the code before any python file is committed. You can check the ```.pre-commit-config.yaml``` file for more details on pylint configuration.


## 🛠 Installation


## ⚡️ Citations

Please cite our work:

Batardière, Bastien, Joon Kwon, Julien Chiquet, and Julien Stoehr (2024).
“Importance sampling based gradient method for dimension reduction in Poisson
Log-Normal model.” In: arXiv. url: https://arxiv.org/abs/2410.00476.
