# This code is part of Qiskit.
#
# (C) Copyright IBM 2021, 2022.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Test the UCCSD Ansatz."""

from test import QiskitNatureTestCase
from test.second_q.circuit.library.ansatzes.test_ucc import assert_ucc_like_ansatz

import unittest

from ddt import ddt, data, unpack

from qiskit_nature.second_q.circuit.library import UCCSD
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_nature.second_q.operators import FermionicOp
from qiskit_nature.second_q.mappers import QubitConverter


@ddt
class TestUCCSD(QiskitNatureTestCase):
    """Tests for the UCCSD Ansatz."""

    @unpack
    @data(
        (
            4,
            (1, 1),
            [
                FermionicOp({"+_0 -_1": 1j, "+_1 -_0": -1j}, register_length=4),
                FermionicOp({"+_2 -_3": 1j, "+_3 -_2": -1j}, register_length=4),
                FermionicOp({"+_0 +_2 -_1 -_3": 1j, "+_3 +_1 -_2 -_0": -1j}, register_length=4),
            ],
        ),
        (
            8,
            (2, 2),
            [
                FermionicOp({"+_0 -_2": 1j, "+_2 -_0": -1j}, register_length=8),
                FermionicOp({"+_0 -_3": 1j, "+_3 -_0": -1j}, register_length=8),
                FermionicOp({"+_1 -_2": 1j, "+_2 -_1": -1j}, register_length=8),
                FermionicOp({"+_1 -_3": 1j, "+_3 -_1": -1j}, register_length=8),
                FermionicOp({"+_4 -_6": 1j, "+_6 -_4": -1j}, register_length=8),
                FermionicOp({"+_4 -_7": 1j, "+_7 -_4": -1j}, register_length=8),
                FermionicOp({"+_5 -_6": 1j, "+_6 -_5": -1j}, register_length=8),
                FermionicOp({"+_5 -_7": 1j, "+_7 -_5": -1j}, register_length=8),
                FermionicOp({"+_0 +_1 -_2 -_3": 1j, "+_3 +_2 -_1 -_0": -1j}, register_length=8),
                FermionicOp({"+_0 +_4 -_2 -_6": 1j, "+_6 +_2 -_4 -_0": -1j}, register_length=8),
                FermionicOp({"+_0 +_4 -_2 -_7": 1j, "+_7 +_2 -_4 -_0": -1j}, register_length=8),
                FermionicOp({"+_0 +_5 -_2 -_6": 1j, "+_6 +_2 -_5 -_0": -1j}, register_length=8),
                FermionicOp({"+_0 +_5 -_2 -_7": 1j, "+_7 +_2 -_5 -_0": -1j}, register_length=8),
                FermionicOp({"+_0 +_4 -_3 -_6": 1j, "+_6 +_3 -_4 -_0": -1j}, register_length=8),
                FermionicOp({"+_0 +_4 -_3 -_7": 1j, "+_7 +_3 -_4 -_0": -1j}, register_length=8),
                FermionicOp({"+_0 +_5 -_3 -_6": 1j, "+_6 +_3 -_5 -_0": -1j}, register_length=8),
                FermionicOp({"+_0 +_5 -_3 -_7": 1j, "+_7 +_3 -_5 -_0": -1j}, register_length=8),
                FermionicOp({"+_1 +_4 -_2 -_6": 1j, "+_6 +_2 -_4 -_1": -1j}, register_length=8),
                FermionicOp({"+_1 +_4 -_2 -_7": 1j, "+_7 +_2 -_4 -_1": -1j}, register_length=8),
                FermionicOp({"+_1 +_5 -_2 -_6": 1j, "+_6 +_2 -_5 -_1": -1j}, register_length=8),
                FermionicOp({"+_1 +_5 -_2 -_7": 1j, "+_7 +_2 -_5 -_1": -1j}, register_length=8),
                FermionicOp({"+_1 +_4 -_3 -_6": 1j, "+_6 +_3 -_4 -_1": -1j}, register_length=8),
                FermionicOp({"+_1 +_4 -_3 -_7": 1j, "+_7 +_3 -_4 -_1": -1j}, register_length=8),
                FermionicOp({"+_1 +_5 -_3 -_6": 1j, "+_6 +_3 -_5 -_1": -1j}, register_length=8),
                FermionicOp({"+_1 +_5 -_3 -_7": 1j, "+_7 +_3 -_5 -_1": -1j}, register_length=8),
                FermionicOp({"+_4 +_5 -_6 -_7": 1j, "+_7 +_6 -_5 -_4": -1j}, register_length=8),
            ],
        ),
        (
            8,
            (2, 1),
            [
                FermionicOp({"+_0 -_2": 1j, "+_2 -_0": -1j}, register_length=8),
                FermionicOp({"+_0 -_3": 1j, "+_3 -_0": -1j}, register_length=8),
                FermionicOp({"+_1 -_2": 1j, "+_2 -_1": -1j}, register_length=8),
                FermionicOp({"+_1 -_3": 1j, "+_3 -_1": -1j}, register_length=8),
                FermionicOp({"+_4 -_5": 1j, "+_5 -_4": -1j}, register_length=8),
                FermionicOp({"+_4 -_6": 1j, "+_6 -_4": -1j}, register_length=8),
                FermionicOp({"+_4 -_7": 1j, "+_7 -_4": -1j}, register_length=8),
                FermionicOp({"+_0 +_1 -_2 -_3": 1j, "+_3 +_2 -_1 -_0": -1j}, register_length=8),
                FermionicOp({"+_0 +_4 -_2 -_5": 1j, "+_5 +_2 -_4 -_0": -1j}, register_length=8),
                FermionicOp({"+_0 +_4 -_2 -_6": 1j, "+_6 +_2 -_4 -_0": -1j}, register_length=8),
                FermionicOp({"+_0 +_4 -_2 -_7": 1j, "+_7 +_2 -_4 -_0": -1j}, register_length=8),
                FermionicOp({"+_0 +_4 -_3 -_5": 1j, "+_5 +_3 -_4 -_0": -1j}, register_length=8),
                FermionicOp({"+_0 +_4 -_3 -_6": 1j, "+_6 +_3 -_4 -_0": -1j}, register_length=8),
                FermionicOp({"+_0 +_4 -_3 -_7": 1j, "+_7 +_3 -_4 -_0": -1j}, register_length=8),
                FermionicOp({"+_1 +_4 -_2 -_5": 1j, "+_5 +_2 -_4 -_1": -1j}, register_length=8),
                FermionicOp({"+_1 +_4 -_2 -_6": 1j, "+_6 +_2 -_4 -_1": -1j}, register_length=8),
                FermionicOp({"+_1 +_4 -_2 -_7": 1j, "+_7 +_2 -_4 -_1": -1j}, register_length=8),
                FermionicOp({"+_1 +_4 -_3 -_5": 1j, "+_5 +_3 -_4 -_1": -1j}, register_length=8),
                FermionicOp({"+_1 +_4 -_3 -_6": 1j, "+_6 +_3 -_4 -_1": -1j}, register_length=8),
                FermionicOp({"+_1 +_4 -_3 -_7": 1j, "+_7 +_3 -_4 -_1": -1j}, register_length=8),
            ],
        ),
    )
    def test_uccsd_ansatz(self, num_spin_orbitals, num_particles, expect):
        """Tests the UCCSD Ansatz."""
        converter = QubitConverter(JordanWignerMapper())

        ansatz = UCCSD(
            qubit_converter=converter,
            num_particles=num_particles,
            num_spin_orbitals=num_spin_orbitals,
        )

        assert_ucc_like_ansatz(self, ansatz, num_spin_orbitals, expect)

    @unpack
    @data(
        (
            6,
            (1, 1),
            [
                FermionicOp({"+_0 -_1": 1j, "+_1 -_0": -1j}, register_length=6),
                FermionicOp({"+_0 -_2": 1j, "+_2 -_0": -1j}, register_length=6),
                FermionicOp({"+_1 -_2": 1j, "+_2 -_1": -1j}, register_length=6),
                FermionicOp({"+_3 -_4": 1j, "+_4 -_3": -1j}, register_length=6),
                FermionicOp({"+_3 -_5": 1j, "+_5 -_3": -1j}, register_length=6),
                FermionicOp({"+_4 -_5": 1j, "+_5 -_4": -1j}, register_length=6),
                FermionicOp({"+_0 +_3 -_1 -_4": 1j, "+_4 +_1 -_3 -_0": -1j}, register_length=6),
                FermionicOp({"+_0 +_3 -_1 -_5": 1j, "+_5 +_1 -_3 -_0": -1j}, register_length=6),
                FermionicOp({"+_0 +_4 -_1 -_5": 1j, "+_5 +_1 -_4 -_0": -1j}, register_length=6),
                FermionicOp({"+_0 +_3 -_2 -_4": 1j, "+_4 +_2 -_3 -_0": -1j}, register_length=6),
                FermionicOp({"+_0 +_3 -_2 -_5": 1j, "+_5 +_2 -_3 -_0": -1j}, register_length=6),
                FermionicOp({"+_0 +_4 -_2 -_5": 1j, "+_5 +_2 -_4 -_0": -1j}, register_length=6),
                FermionicOp({"+_1 +_3 -_2 -_4": 1j, "+_4 +_2 -_3 -_1": -1j}, register_length=6),
                FermionicOp({"+_1 +_3 -_2 -_5": 1j, "+_5 +_2 -_3 -_1": -1j}, register_length=6),
                FermionicOp({"+_1 +_4 -_2 -_5": 1j, "+_5 +_2 -_4 -_1": -1j}, register_length=6),
            ],
        ),
    )
    def test_uccsd_ansatz_generalized(self, num_spin_orbitals, num_particles, expect):
        """Tests the generalized UCCSD Ansatz."""
        converter = QubitConverter(JordanWignerMapper())

        ansatz = UCCSD(
            qubit_converter=converter,
            num_particles=num_particles,
            num_spin_orbitals=num_spin_orbitals,
            generalized=True,
        )

        assert_ucc_like_ansatz(self, ansatz, num_spin_orbitals, expect)

    @unpack
    @data(
        (
            4,
            (1, 1),
            [
                FermionicOp({"+_0 -_1": 1j, "+_1 -_0": -1j}, register_length=4),
                FermionicOp({"+_0 -_3": 1j, "+_3 -_0": -1j}, register_length=4),
                FermionicOp({"+_2 -_1": 1j, "+_1 -_2": -1j}, register_length=4),
                FermionicOp({"+_2 -_3": 1j, "+_3 -_2": -1j}, register_length=4),
                FermionicOp({"+_0 +_2 -_1 -_3": 1j, "+_3 +_1 -_2 -_0": -1j}, register_length=4),
            ],
        ),
        (
            6,
            (1, 1),
            [
                FermionicOp({"+_0 -_1": 1j, "+_1 -_0": -1j}, register_length=6),
                FermionicOp({"+_0 -_2": 1j, "+_2 -_0": -1j}, register_length=6),
                FermionicOp({"+_0 -_4": 1j, "+_4 -_0": -1j}, register_length=6),
                FermionicOp({"+_0 -_5": 1j, "+_5 -_0": -1j}, register_length=6),
                FermionicOp({"+_3 -_1": 1j, "+_1 -_3": -1j}, register_length=6),
                FermionicOp({"+_3 -_2": 1j, "+_2 -_3": -1j}, register_length=6),
                FermionicOp({"+_3 -_4": 1j, "+_4 -_3": -1j}, register_length=6),
                FermionicOp({"+_3 -_5": 1j, "+_5 -_3": -1j}, register_length=6),
                FermionicOp({"+_0 +_3 -_1 -_2": 1j, "+_2 +_1 -_3 -_0": -1j}, register_length=6),
                FermionicOp({"+_0 +_3 -_1 -_4": 1j, "+_4 +_1 -_3 -_0": -1j}, register_length=6),
                FermionicOp({"+_0 +_3 -_1 -_5": 1j, "+_5 +_1 -_3 -_0": -1j}, register_length=6),
                FermionicOp({"+_0 +_3 -_2 -_4": 1j, "+_4 +_2 -_3 -_0": -1j}, register_length=6),
                FermionicOp({"+_0 +_3 -_2 -_5": 1j, "+_5 +_2 -_3 -_0": -1j}, register_length=6),
                FermionicOp({"+_0 +_3 -_4 -_5": 1j, "+_5 +_4 -_3 -_0": -1j}, register_length=6),
            ],
        ),
    )
    def test_uccsd_ansatz_preserve_spin(self, num_spin_orbitals, num_particles, expect):
        """Tests UCCSD Ansatz with spin flips."""
        converter = QubitConverter(JordanWignerMapper())

        ansatz = UCCSD(
            qubit_converter=converter,
            num_particles=num_particles,
            num_spin_orbitals=num_spin_orbitals,
            preserve_spin=False,
        )

        assert_ucc_like_ansatz(self, ansatz, num_spin_orbitals, expect)


if __name__ == "__main__":
    unittest.main()
