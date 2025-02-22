# This code is part of Qiskit.
#
# (C) Copyright IBM 2022.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Test for SparseLabelOp"""

from __future__ import annotations

from typing import Collection, Iterator

import unittest
from test import QiskitNatureTestCase

from qiskit_nature.second_q.operators import PolynomialTensor, SparseLabelOp

op1 = {
    "+_0 -_1": 0.0,
    "+_0 -_2": 1.0,
}

op2 = {
    "+_0 -_1": 0.5,
    "+_0 -_2": 1.0,
}

op3 = {
    "+_0 -_1": 0.5,
    "+_0 -_3": 3.0,
}

opComplex = {
    "+_0 -_1": 0.5 + 1j,
    "+_0 -_2": 1.0,
}


class DummySparseLabelOp(SparseLabelOp):
    """Dummy SparseLabelOp for testing purposes"""

    @classmethod
    def _validate_keys(cls, keys: Collection[str], register_length: int | None) -> int:
        return register_length

    @classmethod
    def _validate_polynomial_tensor_key(cls, keys: Collection[str]) -> None:
        pass

    @classmethod
    def from_polynomial_tensor(cls, tensor: PolynomialTensor) -> SparseLabelOp:
        pass

    def terms(self) -> Iterator[tuple[list[tuple[str, int]], complex]]:
        pass

    def transpose(self) -> SparseLabelOp:
        return self

    def compose(self, other, qargs=None, front=False) -> SparseLabelOp:
        return self

    def tensor(self, other) -> SparseLabelOp:
        return self

    def expand(self, other) -> SparseLabelOp:
        return self

    # pylint: disable=unused-argument
    def simplify(self, *, atol: float | None = None) -> SparseLabelOp:
        return self


class TestSparseLabelOp(QiskitNatureTestCase):
    """SparseLabelOp tests."""

    def test_add(self):
        """Test add method"""
        with self.subTest("real + real"):
            test_op = DummySparseLabelOp(op1, 2) + DummySparseLabelOp(op2, 2)
            target_op = DummySparseLabelOp(
                {
                    "+_0 -_1": 0.5,
                    "+_0 -_2": 2.0,
                },
                2,
            )

            self.assertEqual(test_op, target_op)

        with self.subTest("complex + real"):
            test_op = DummySparseLabelOp(op2, 2) + DummySparseLabelOp(opComplex, 2)
            target_op = DummySparseLabelOp(
                {
                    "+_0 -_1": 1.0 + 1j,
                    "+_0 -_2": 2.0,
                },
                2,
            )

            self.assertEqual(test_op, target_op)

        with self.subTest("complex + complex"):
            test_op = DummySparseLabelOp(opComplex, 2) + DummySparseLabelOp(opComplex, 2)
            target_op = DummySparseLabelOp(
                {
                    "+_0 -_1": 1.0 + 2j,
                    "+_0 -_2": 2.0,
                },
                2,
            )

            self.assertEqual(test_op, target_op)

        with self.subTest("new key"):
            test_op = DummySparseLabelOp(op1, 2) + DummySparseLabelOp(op3, 2)
            target_op = DummySparseLabelOp(
                {
                    "+_0 -_1": 0.5,
                    "+_0 -_2": 1.0,
                    "+_0 -_3": 3.0,
                },
                2,
            )

            self.assertEqual(test_op, target_op)

    def test_mul(self):
        """Test scalar multiplication method"""
        with self.subTest("real * real"):
            test_op = DummySparseLabelOp(op1, 2) * 2
            target_op = DummySparseLabelOp(
                {
                    "+_0 -_1": 0.0,
                    "+_0 -_2": 2.0,
                },
                2,
            )

            self.assertEqual(test_op, target_op)

        with self.subTest("complex * real"):
            test_op = DummySparseLabelOp(opComplex, 2) * 2
            target_op = DummySparseLabelOp(
                {
                    "+_0 -_1": 1.0 + 2j,
                    "+_0 -_2": 2.0,
                },
                2,
            )

            self.assertEqual(test_op, target_op)

        with self.subTest("real * complex"):
            test_op = DummySparseLabelOp(op2, 2) * (0.5 + 1j)
            target_op = DummySparseLabelOp(
                {
                    "+_0 -_1": 0.25 + 0.5j,
                    "+_0 -_2": 0.5 + 1j,
                },
                2,
            )

            self.assertEqual(test_op, target_op)

        with self.subTest("complex * complex"):
            test_op = DummySparseLabelOp(opComplex, 2) * (0.5 + 1j)
            target_op = DummySparseLabelOp(
                {
                    "+_0 -_1": -0.75 + 1j,
                    "+_0 -_2": 0.5 + 1j,
                },
                2,
            )

            self.assertEqual(test_op, target_op)

        with self.subTest("raises TypeError"):
            with self.assertRaises(TypeError):
                _ = DummySparseLabelOp(op1, 2) * "something"

    def test_adjoint(self):
        """Test adjoint method"""
        test_op = DummySparseLabelOp(opComplex, 2).adjoint()
        target_op = DummySparseLabelOp(
            {
                "+_0 -_1": 0.5 - 1j,
                "+_0 -_2": 1.0,
            },
            2,
        )
        self.assertEqual(test_op, target_op)

    def test_conjugate(self):
        """Test conjugate method"""
        test_op = DummySparseLabelOp(opComplex, 2).conjugate()
        target_op = DummySparseLabelOp(
            {
                "+_0 -_1": 0.5 - 1j,
                "+_0 -_2": 1.0,
            },
            2,
        )
        self.assertEqual(test_op, target_op)

    def test_eq(self):
        """test __eq__ method"""
        with self.subTest("equal"):
            test_op = DummySparseLabelOp(op1, 2) == DummySparseLabelOp(op1, 2)
            self.assertTrue(test_op)

        with self.subTest("not equal - keys"):
            test_op = DummySparseLabelOp(op1, 2) == DummySparseLabelOp(
                {
                    "+_0 -_1": 0.0,
                    "+_0 -_3": 1.0,
                },
                2,
            )
            self.assertFalse(test_op)

        with self.subTest("not equal - values"):
            test_op = DummySparseLabelOp(op1, 2) == DummySparseLabelOp(op2, 2)
            self.assertFalse(test_op)

        with self.subTest("not equal - tolerance"):
            test_op = DummySparseLabelOp(op1, 2) == DummySparseLabelOp(
                {
                    "+_0 -_1": 0.000000001,
                    "+_0 -_2": 1.0,
                },
                2,
            )

            self.assertFalse(test_op)

    def test_equiv(self):
        """test equiv method"""
        with self.subTest("not equivalent - tolerances"):
            test_op = DummySparseLabelOp(op1, 2).equiv(
                DummySparseLabelOp(
                    {
                        "+_0 -_1": 0.000001,
                        "+_0 -_2": 1.0,
                    },
                    2,
                )
            )

            self.assertFalse(test_op)

        with self.subTest("not equivalent - keys"):
            test_op = DummySparseLabelOp(op1, 2).equiv(
                DummySparseLabelOp(
                    {
                        "+_0 -_1": 0.0,
                        "+_0 -_3": 1.0,
                    },
                    2,
                )
            )

            self.assertFalse(test_op)

        with self.subTest("equivalent"):
            test_op = DummySparseLabelOp(op1, 2).equiv(
                DummySparseLabelOp(
                    {
                        "+_0 -_1": 0.000000001,
                        "+_0 -_2": 1.0,
                    },
                    2,
                )
            )

            self.assertTrue(test_op)

    def test_iter(self):
        """test __iter__ method"""
        test_op = iter(DummySparseLabelOp(op1, 2))

        self.assertEqual(next(test_op), "+_0 -_1")
        self.assertEqual(next(test_op), "+_0 -_2")

    def test_get_item(self):
        """test __getitem__ method"""
        test_op = DummySparseLabelOp(op1, 2)
        self.assertEqual(test_op["+_0 -_1"], 0.0)

    def test_len(self):
        """test __len__ method"""
        test_op = DummySparseLabelOp(op1, 2)
        self.assertEqual(len(test_op), 2)

    def test_get_register_length(self):
        """test register length property"""
        test_val = DummySparseLabelOp(op1, 2).register_length
        self.assertEqual(test_val, 2)

    def test_copy(self):
        """test copy bool"""
        data = {
            "+_0 -_1": 0.0,
            "+_0 -_3": 1.0,
        }
        test_op = DummySparseLabelOp(data, 2, copy=True)
        data["+_0 -_1"] = 0.2
        self.assertEqual(test_op._data["+_0 -_1"], 0.0)

    def test_zero(self):
        """test zero class initializer"""
        test_op = DummySparseLabelOp.zero(1)
        self.assertEqual(test_op._data, {})
        self.assertEqual(test_op.register_length, 1)

    def test_one(self):
        """test one class initializer"""
        test_op = DummySparseLabelOp.one(1)
        self.assertEqual(test_op._data, {"": 1.0})
        self.assertEqual(test_op.register_length, 1)


if __name__ == "__main__":
    unittest.main()
