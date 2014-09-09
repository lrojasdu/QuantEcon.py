"""
Solow growth model with Cobb-Douglas aggregate production.

@author : David R. Pugh
@date : 2014-09-01

"""
import numpy as np
import sympy as sym

from . import model

# declare key variables for the model
t, X = sym.var('t'), sym.DeferredVector('X')
A, k, K, L = sym.var('A, k, K, L')

# declare required model parameters
g, n, s, alpha, delta = sym.var('g, n, s, alpha, delta')


class CobbDouglasModel(model.Model):

    def __init__(self, params):
        """
        Create an instance of the Solow growth model with Cobb-Douglas
        aggregate production.

        Parameters
        ----------
        params : dict
            Dictionary of model parameters.

        """
        cobb_douglas_output = K**alpha * (A * L)**(1 - alpha)
        super(CobbDouglasModel, self).__init__(cobb_douglas_output, params)


def analytic_solution(cls, t, k0):
    """
    Compute the analytic solution for the Solow model with Cobb-Douglas
    production technology.

    Parameters
    ----------
    cls : object
        Instance of the `solow.CobbDouglasModel` class.
    t : ndarray (shape=(T,))
        Array of points at which the solution is desired.
    k0 : (float)
        Initial condition for capital stock (per unit of effective labor)

    Returns
    -------
    analytic_traj : ndarray (shape=t.size, 2)
        Array representing the analytic solution trajectory.

    """
    s = cls.params['s']
    alpha = cls.params['alpha']

    # lambda governs the speed of convergence
    lmbda = cls.effective_depreciation_rate * (1 - alpha)

    # analytic solution for Solow model at time t
    k_t = (((s / (cls.effective_depreciation_rate)) * (1 - np.exp(-lmbda * t)) +
            k0**(1 - alpha) * np.exp(-lmbda * t))**(1 / (1 - alpha)))

    # combine into a (T, 2) array
    analytic_traj = np.hstack((t[:, np.newaxis], k_t[:, np.newaxis]))

    return analytic_traj


def analytic_steady_state(cls):
    """
    Steady-state level of capital stock (per unit effective labor).

    Parameters
    ----------
    cls : object
        Instance of the `solow.CobbDouglasModel` class.

    Returns
    -------
    kstar : float
        Steady state value of capital stock (per unit effective labor).

    """
    s = cls.params['s']
    alpha = cls.params['alpha']

    k_star = (s / cls.effective_depreciation_rate)**(1 / (1 - alpha))

    return k_star
