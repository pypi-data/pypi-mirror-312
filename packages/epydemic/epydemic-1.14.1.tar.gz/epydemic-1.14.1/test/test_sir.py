# Test SIR under different dynamics
#
# Copyright (C) 2017--2021 Simon Dobson
#
# This file is part of epydemic, epidemic network simulations in Python.
#
# epydemic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# epydemic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with epydemic. If not, see <http://www.gnu.org/licenses/gpl.html>.

import unittest
import networkx             # type: ignore
import epyc
from epydemic import *
from test.compartmenteddynamics import CompartmentedDynamicsTest

class SIRTest(unittest.TestCase, CompartmentedDynamicsTest):

    def setUp( self ):
        '''Set up the experimental parameters and experiment.'''

        # single epidemic-causing experiment
        self._params = dict()
        self._params[SIR.P_INFECT] = 0.3
        self._params[SIR.P_INFECTED] = 0.01
        self._params[SIR.P_REMOVE] = 0.05
        self._network = networkx.erdos_renyi_graph(1000, 0.005)

        # lab run
        self._lab = epyc.Lab()
        self._lab[SIR.P_INFECT] = [ 0.1,  0.3 ]
        self._lab[SIR.P_INFECTED] = 0.01
        self._lab[SIR.P_REMOVE] = [ 0.05, 1 ]

        # model
        self._model = SIR()

    def assertEpidemic(self, rc):
        self.assertCountEqual(rc, [SIR.SUSCEPTIBLE, SIR.INFECTED, SIR.REMOVED])
        self.assertTrue(rc[SIR.SUSCEPTIBLE] > 0)
        self.assertTrue(rc[SIR.INFECTED] == 0)
        self.assertTrue(rc[SIR.REMOVED] > 0)
        self.assertEqual(rc[SIR.SUSCEPTIBLE] + rc[SIR.REMOVED], self._network.order())


if __name__ == '__main__':
    unittest.main()
