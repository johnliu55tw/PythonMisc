import unittest
try:
    import unittest.mock as mock
except ImportError:
    import mock

import the_module


class TestModuleA(unittest.TestCase):

    def testModuleA(self):
        a = the_module.ModuleA('John')
        self.assertEqual('John', a.value)
