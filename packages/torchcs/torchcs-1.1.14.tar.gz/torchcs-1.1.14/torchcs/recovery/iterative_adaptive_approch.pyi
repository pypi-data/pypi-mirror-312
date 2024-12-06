def iaa(Y, Phi, x0=None, niter=15, tol=1e-6, gamma=None, islog=False):
    r"""Iterative Adaptive Approch

    Parameters
    ----------
    Y : Tensor
        Observation :math:`{\bf Y} \in {\mathbb C}^{M\times L}`
    Phi : Tensor
        Observation matrix :math:`{\bf \Phi} \in {\mathbb C}^{M\times N}`
    x : Tensor or None
        Initial :math:`{\bf Y} \in {\mathbb C}^{N\times 1}`
    niter : int, optional
        The number of iteration (the default is 15)
    tol : float, optional
        The tolerance of error (the default is 1e-6)
    gamma : float or None, optional
        the regularization factor, by default None
    islog : str, optional
        show progress bar and other log information.
    """

def iaaadl(Y, Phi, x0=None, niter=15, tol=1e-6, islog=False):
    r"""Iterative Adaptive Approch with Adaptive Diagonal Loading

    Parameters
    ----------
    Y : Tensor
        Observation :math:`{\bf Y} \in {\mathbb C}^{M\times L}`
    Phi : Tensor
        Observation matrix :math:`{\bf \Phi} \in {\mathbb C}^{M\times N}`
    x : Tensor or None
        Initial :math:`{\bf Y} \in {\mathbb C}^{N\times 1}`
    niter : int, optional
        The number of iteration (the default is 15)
    tol : float, optional
        The tolerance of error (the default is 1e-6)
    islog : str, optional
        show progress bar and other log information.
    """


