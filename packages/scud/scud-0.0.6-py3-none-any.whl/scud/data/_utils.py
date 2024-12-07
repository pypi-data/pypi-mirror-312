import warnings


def _threshold_samples_and_dim(max_samples, max_dim, n_samples, dim):
    if n_samples > max_samples:
        warnings.warn(
            message=(
                "\nTaking the whole max_samples samples of the dataset. Requested:"
                f" n_samples={n_samples}, returned:{max_samples}"
            )
        )
        n_samples = max_samples
    if dim > max_dim:
        warnings.warn(
            f"\nTaking the whole max_dim variables. Requested:dim={dim}, returned:{max_dim}"
        )
        dim = max_dim
    return n_samples, dim
