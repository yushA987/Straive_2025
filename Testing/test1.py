import unittest

from numpy.ma.testutils import assert_equal

from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(5,10), 15)
        self.assertEqual(self.calc.add(0, 5), 10)
    
    def test_subtract(self):
        self.assertEqual(self.calc.subtract(10, 5), 5)
        self.assertEqual(self.calc.subtract(100,90), 100)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(10, 9), 90)
        self.assertEqual(self.calc.multiply(0, 10), 1)

    def test_divide(self):
        self.assertEqual(self.calc.divide(100, 10), 10)
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

if __name__ == '__main__':
    unittest.main()