from math import log, pi

import torch


def gaussian_log_likelihood(
    x: torch.tensor, mean: torch.tensor, logvar: torch.tensor, clip: bool = True
) -> torch.tensor:
    """Calculates the log likelihood of a Gaussian distribution.

    Parameters
    ----------
    x : torch.tensor
        the sampled value
    mean : torch.tensor
        the mean of the Gaussian distribution
    logvar : torch.tensor
        the log variance of the Gaussian distribution
    clip : bool, optional
        whether to clip the variance to range [-4,3], by default True

    Returns
    -------
    torch.tensor
        the log likelihood of the Gaussian distribution
    """
    if clip:
        logvar = torch.clamp(logvar, min=-4, max=3)
    a = log(2 * pi)
    b = logvar
    c = (x - mean) ** 2 / torch.exp(logvar)
    return -0.5 * torch.sum(a + b + c)


def bernoulli_log_likelihood(x: torch.tensor, p: torch.tensor, clip: bool = True, eps: float = 1e-6) -> torch.tensor:
    """
    Computes the log-likelihood of a Bernoulli distribution.

    Parameters
    ----------
    x: torch.tensor
        The observed data, a tensor of binary values (0 or 1).
    p: torch.tensor
        The probabilities of success for the Bernoulli distribution.
    clip: bool, optional
        Whether to clip the probabilities to avoid log(0). Default is True.
    eps: float, optional
        A small value to use for clipping probabilities. Default is 1e-6.

    Returns
    -------
    torch.tensor
        The log-likelihood of the observed data given the probabilities.
    """

    if clip:
        p = torch.clamp(p, min=eps, max=1 - eps)
    return torch.sum((x * torch.log(p)) + ((1 - x) * torch.log(1 - p)))


def kl_diagnormal_stdnormal(mean: torch.tensor, logvar: torch.tensor) -> torch.tensor:
    """Calculates the KL divergence between a diagonal normal distribution and a standard normal distribution.

    Parameters
    ----------
    mean : torch.tensor
        the mean of the diagonal normal distribution
    logvar : torch.tensor
        the log variance of the diagonal normal distribution

    Returns
    -------
    torch.tensor
        the KL divergence between the diagonal normal and standard normal distributions
    """
    logvar = torch.clamp(logvar, min=-5, max=5)
    a = mean**2
    b = torch.exp(logvar)
    c = -1
    d = -logvar
    return 0.5 * torch.sum(a + b + c + d)


def kl_diagnormal_diagnormal(
    q_mean: torch.tensor,
    q_logvar: torch.tensor,
    p_mean: torch.tensor,
    p_logvar: torch.tensor,
    clamp: bool = True,
    sum: bool = True,
) -> torch.tensor:
    """Calculates the KL divergence between two diagonal normal distributions and.

    Parameters
    ----------
    q_mean : torch.tensor
        the mean of the first diagonal normal distribution
    q_logvar : torch.tensor
        the log variance of the first diagonal normal distribution
    p_mean : torch.tensor
        the mean of the second diagonal normal distribution
    p_logvar : torch.tensor
        the log variance of the second diagonal normal distribution
    clamp : bool, optional
        whether to clamp the log variances to range [-5,5], by default True
    sum : bool, optional
        whether to sum the KL divergence over the last dimension, by default True

    Returns
    -------
    torch.tensor
        the KL divergence between the two diagonal normal distributions
    """
    # Ensure correct shapes since no numpy broadcasting yet
    if len(q_mean.shape) > len(p_mean.shape):
        p_mean = p_mean.expand_as(q_mean)
        p_logvar = p_logvar.expand_as(q_logvar)
    elif len(q_mean.shape) < len(p_mean.shape):
        q_mean = q_mean.expand_as(p_mean)
        q_logvar = q_logvar.expand_as(p_logvar)
    if clamp:
        q_logvar = torch.clamp(q_logvar, min=-5, max=5)
        p_logvar = torch.clamp(p_logvar, min=-5, max=5)

    a = p_logvar
    b = -1
    c = -q_logvar
    d = ((q_mean - p_mean) ** 2 + torch.exp(q_logvar)) / torch.exp(p_logvar)
    if sum:
        return 0.5 * torch.sum(a + b + c + d)
    return 0.5 * torch.sum(a + b + c + d, dim=-1)
