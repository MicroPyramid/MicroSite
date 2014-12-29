from django.test import TestCase

# Create your tests here.
import unittest

class TestBasic(unittest.TestCase):
    "Basic tests"

    def test_basic(self):
        a = 1
        self.assertEqual(1, a)