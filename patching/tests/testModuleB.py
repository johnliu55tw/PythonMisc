import unittest
try:
    import unittest.mock as mock
except ImportError:
    import mock

import the_module


class TestModuleB(unittest.TestCase):

    @mock.patch("the_module.module_b.ModuleA")
    def testModuleB(self, mockedModuleA):
        b = the_module.ModuleB('Andy')
        mockedModuleA.assert_called_with('Andy')
        self.assertIsInstance(b.a, mock.Mock)
