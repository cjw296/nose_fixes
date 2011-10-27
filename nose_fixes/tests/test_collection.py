from imp import new_module
from nose.case import Test
from unittest import TestCase

class Tests(TestCase):

    def setUp(self):
        from nose_fixes.plugin import Plugin
        plugin = Plugin()
        plugin.test_suite_func = 'test_suite'
        self.l = plugin.prepareTestLoader(None)
        
    def test_suite(self):

        suite = object()
        def test_suite():
            # return a suite
            return suite
        
        mod = new_module('with_test_suite')
        mod.test_suite = test_suite

        self.assertTrue(self.l.loadTestsFromModule(mod) is suite)

    def test_no_suite(self):
        def test_sweet():
            # a tester of sweets ;-)
            assert True!=False
        
        mod = new_module('without_test_suite')
        mod.test_sweet = test_sweet

        suite = self.l.loadTestsFromModule(mod)

        tests = [t for t in suite]
        self.assertEqual(len(tests), 1)
        test = tests[0]
        self.assertTrue(isinstance(test, Test))
        self.assertEqual(repr(test), 'Test(without_test_suite.test_sweet)')
