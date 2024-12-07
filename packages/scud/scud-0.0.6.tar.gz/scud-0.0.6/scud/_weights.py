import jax.numpy as jnp


def _get_weights_and_const_from_log_quotient(log_num, log_denom):
    diff_log = log_num - log_denom
    const = jnp.max(diff_log, axis=0)
    diff_log -= const
    weights = jnp.exp(diff_log)
    return weights, const


def _normalize_weights(weights):
    return jnp.divide(weights, jnp.sum(weights, axis=0))


def _get_normalized_weights_const_and_weights(log_num, log_denom):
    weights, const = _get_weights_and_const_from_log_quotient(log_num, log_denom)
    return _normalize_weights(weights), const, weights
