import numpy as np

from mushroom.algorithms.value import LSPI
from mushroom.core import Core
from mushroom.environments import *
from mushroom.features import Features
from mushroom.features.basis import PolynomialBasis
from mushroom.policy import EpsGreedy
from mushroom.utils.parameters import Parameter


def test_lspi():
    np.random.seed(1)

    # MDP
    mdp = CartPole()

    # Policy
    epsilon = Parameter(value=1.)
    pi = EpsGreedy(epsilon=epsilon)

    # Agent
    basis = [PolynomialBasis()]
    features = Features(basis_list=basis)

    fit_params = dict()
    approximator_params = dict(input_shape=(features.size,),
                               output_shape=(mdp.info.action_space.n,),
                               n_actions=mdp.info.action_space.n)
    agent = LSPI(mdp.info, pi, approximator_params=approximator_params,
                 fit_params=fit_params, features=features)

    # Algorithm
    core = Core(agent, mdp)

    # Train
    core.learn(n_episodes=10, n_episodes_per_fit=10)

    w = agent.approximator.get_weights()
    w_test = np.array([-1.00749128, -1.13444655, -0.96620322])

    assert np.allclose(w, w_test)
