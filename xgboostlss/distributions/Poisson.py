from torch.distributions import Poisson as Poisson_Torch
from xgboostlss.utils import *
from .distribution_utils import DistributionClass


class Poisson(DistributionClass):
    """
    Poisson distribution class.

    Distributional Parameters
    -------------------------
    rate: torch.Tensor
        Rate parameter of the distribution (often referred to as lambda).

    Source
    -------------------------
    https://pytorch.org/docs/stable/distributions.html#poisson

    Parameters
    -------------------------
    stabilization: str
        Stabilization method for the Gradient and Hessian. Options are "None", "MAD", "L2".
    response_fn: str
        When a custom objective and metric are provided, XGBoost doesn't know its response and link function. Hence,
        the user is responsible for specifying the transformations. Options are "exp", "softplus" or "relu".
    loss_fn: str
        Loss function. Options are "nll" (negative log-likelihood) or "crps" (continuous ranked probability score).
        Note that if "crps" is used, the Hessian is set to 1, as the current CRPS version is not twice differentiable.
        Hence, using the CRPS disregards any variation in the curvature of the loss function.
    """
    def __init__(self,
                 stabilization: str = "None",
                 response_fn: str = "relu",
                 loss_fn: str = "nll"
                 ):
        #  # Specify Response Functions
        if response_fn == "exp":
            response_fn = exp_fn
        elif response_fn == "softplus":
            response_fn = softplus_fn
        elif response_fn == "relu":
            response_fn = relu_fn
        else:
            raise ValueError("Invalid response function for total_count. Please choose from 'exp', 'softplus' or relu.")

        # Set the parameters specific to the distribution
        distribution = Poisson_Torch
        param_dict = {"rate": response_fn}

        # Specify Distribution Class
        super().__init__(distribution=distribution,
                         univariate=True,
                         discrete=False,
                         n_dist_param=len(param_dict),
                         stabilization=stabilization,
                         param_dict=param_dict,
                         distribution_arg_names=list(param_dict.keys()),
                         loss_fn=loss_fn
                         )
