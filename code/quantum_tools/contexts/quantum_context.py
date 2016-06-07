"""
Methods used to take a set of states and measurements and determine a probability distribution from it.
"""
from __future__ import print_function, division
import numpy as np
from ..statistics.probability import ProbDist
from ..utilities import utils
from .measurement import Measurement
from ..statistics.variable import RandomVariableCollection
from .state import State
from .. import config

class QuantumContext():

    def __init__(self, random_variables, measurements, states, permutation=None):
        self.random_variables = random_variables
        self.measurements = measurements
        self.states = states
        self.permutation = permutation
        self.permutationT = permutation.T if permutation is not None else None
        self.num_measurements = len(measurements)
        self.num_states = len(states)

def QuantumProbDist(qc):
    def pdf(*args):
        measurement_operators = [qc.measurements[posn][val] for posn, val in enumerate(args)]
        joint_measurement = utils.tensor(*measurement_operators)
        joint_state = utils.tensor(*tuple(s.data for s in qc.states))
        # if args == (0,0,0):
        #     for i in measurement_operators:
        #         print(i)
        #     for s in qc.states:
        #         print(s.data)
        #     print(joint_measurement)
        #     print(joint_state)
        if qc.permutation is not None:
            joint_state = utils.multidot(qc.permutationT, joint_state, qc.permutation)

        p = np.trace(utils.multidot(joint_state, joint_measurement))
        assert(utils.is_small(p.imag)), "Probability is not real. It is {0}.".format(p)
        return p.real

    pd = ProbDist.from_callable_support(qc.random_variables, pdf)
    return pd
