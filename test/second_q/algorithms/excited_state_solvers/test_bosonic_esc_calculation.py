# This code is part of Qiskit.
#
# (C) Copyright IBM 2020, 2022.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

""" Test Numerical qEOM excited states calculation """

import contextlib
import io
import unittest

from test import QiskitNatureTestCase

import numpy as np

from qiskit.algorithms.optimizers import COBYLA
from qiskit.primitives import Estimator
from qiskit.utils import algorithm_globals

from qiskit_nature.second_q.circuit.library import UVCCSD
from qiskit_nature.second_q.drivers import VibrationalStructureDriver
from qiskit_nature.second_q.mappers import DirectMapper
from qiskit_nature.second_q.mappers import QubitConverter
from qiskit_nature.second_q.problems import (
    VibrationalStructureProblem,
)

from qiskit_nature.second_q.algorithms import (
    GroundStateEigensolver,
    NumPyMinimumEigensolverFactory,
    VQEUVCCFactory,
    QEOM,
    ExcitedStatesEigensolver,
    NumPyEigensolverFactory,
)
from qiskit_nature.second_q.hamiltonians import VibrationalEnergy
from qiskit_nature.second_q.properties import OccupiedModals
from qiskit_nature.second_q.properties.integrals import VibrationalIntegrals


class _DummyBosonicDriver(VibrationalStructureDriver):
    def __init__(self):
        super().__init__()
        modes = [
            [605.3643675, 1, 1],
            [-605.3643675, -1, -1],
            [340.5950575, 2, 2],
            [-340.5950575, -2, -2],
            [-89.09086530649508, 2, 1, 1],
            [-15.590557244410897, 2, 2, 2],
            [1.6512647916666667, 1, 1, 1, 1],
            [5.03965375, 2, 2, 1, 1],
            [0.43840625000000005, 2, 2, 2, 2],
        ]
        sorted_integrals: dict[int, list[tuple[float, tuple[int, ...]]]] = {1: [], 2: [], 3: []}
        for coeff, *indices in modes:
            ints = [int(i) for i in indices]
            num_body = len(set(ints))
            sorted_integrals[num_body].append((coeff, tuple(ints)))

        prop = VibrationalEnergy(
            [VibrationalIntegrals(num_body, ints) for num_body, ints in sorted_integrals.items()]
        )
        self._driver_result = VibrationalStructureProblem(
            prop,
            num_modes=2,
            num_modals=2,
        )
        prop = OccupiedModals()
        self._driver_result.properties.occupied_modals = prop

    def run(self):
        """Run dummy driver to return test watson hamiltonian"""
        return self._driver_result


class TestBosonicESCCalculation(QiskitNatureTestCase):
    """Test Numerical QEOM excited states calculation"""

    def setUp(self):
        super().setUp()
        algorithm_globals.random_seed = 8
        self.reference_energies = [
            1889.95738428,
            3294.21806197,
            4287.26821341,
            5819.76975784,
        ]

        self.driver = _DummyBosonicDriver()
        self.qubit_converter = QubitConverter(DirectMapper())
        self.basis_size = 2
        self.truncation_order = 2

        self.vibrational_problem = self.driver.run()
        self.vibrational_problem._num_modals = 2
        self.vibrational_problem.truncation_order = self.truncation_order

    def _assert_energies(self, computed, references, *, places=4):
        with self.subTest("same number of energies"):
            self.assertEqual(len(computed), len(references))

        with self.subTest("ground state"):
            self.assertAlmostEqual(computed[0], references[0], places=places)

        for i in range(1, len(computed)):
            with self.subTest(f"{i}. excited state"):
                self.assertAlmostEqual(computed[i], references[i], places=places)

    def test_numpy_mes(self):
        """Test with NumPyMinimumEigensolver"""
        estimator = Estimator()
        solver = NumPyMinimumEigensolverFactory(use_default_filter_criterion=True)
        gsc = GroundStateEigensolver(self.qubit_converter, solver)
        esc = QEOM(gsc, estimator, "sd")
        results = esc.solve(self.vibrational_problem)
        self._assert_energies(results.computed_vibrational_energies, self.reference_energies)

    def test_numpy_factory(self):
        """Test with NumPyEigensolver"""
        solver = NumPyEigensolverFactory(use_default_filter_criterion=True)
        esc = ExcitedStatesEigensolver(self.qubit_converter, solver)
        results = esc.solve(self.vibrational_problem)
        self._assert_energies(results.computed_vibrational_energies, self.reference_energies)

    def test_vqe_uvccsd_factory(self):
        """Test with VQE plus UVCCSD"""
        optimizer = COBYLA(maxiter=5000)
        estimator = Estimator()
        solver = VQEUVCCFactory(estimator, UVCCSD(), optimizer)
        gsc = GroundStateEigensolver(self.qubit_converter, solver)
        esc = QEOM(gsc, estimator, "sd")
        results = esc.solve(self.vibrational_problem)
        self._assert_energies(
            results.computed_vibrational_energies, self.reference_energies, places=1
        )

    def test_vqe_uvcc_factory_with_user_initial_point(self):
        """Test VQEUVCCFactory when using it with a user defined initial point."""
        initial_point = np.asarray([-7.35250290e-05, -9.73079292e-02, -5.43346282e-05])
        estimator = Estimator()
        optimizer = COBYLA(maxiter=1)
        solver = VQEUVCCFactory(estimator, UVCCSD(), optimizer, initial_point=initial_point)
        gsc = GroundStateEigensolver(self.qubit_converter, solver)
        esc = QEOM(gsc, estimator, "sd")
        results = esc.solve(self.vibrational_problem)
        np.testing.assert_array_almost_equal(
            results.raw_result.ground_state_raw_result.optimal_point, initial_point
        )

    def test_vqe_uvccsd_with_callback(self):
        """Test VQE UVCCSD with callback."""

        def cb_callback(nfev, parameters, energy, stddev):
            print(f"iterations {nfev}: energy: {energy}")

        estimator = Estimator()
        optimizer = COBYLA(maxiter=5000)

        solver = VQEUVCCFactory(estimator, UVCCSD(), optimizer, callback=cb_callback)
        gsc = GroundStateEigensolver(self.qubit_converter, solver)
        esc = QEOM(gsc, estimator, "sd")
        with contextlib.redirect_stdout(io.StringIO()) as out:
            results = esc.solve(self.vibrational_problem)
        self._assert_energies(
            results.computed_vibrational_energies, self.reference_energies, places=1
        )
        for idx, line in enumerate(out.getvalue().split("\n")):
            if line.strip():
                self.assertTrue(line.startswith(f"iterations {idx+1}: energy: "))


if __name__ == "__main__":
    unittest.main()
