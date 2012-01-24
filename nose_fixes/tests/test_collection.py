from imp import new_module
from nose.case import Test as NoseTest
from nose.suite import ContextSuite
from nose.loader import TestLoader
from unittest import TestCase, TestSuite, makeSuite

class Tests(TestCase):

    def setUp(self):
        from nose_fixes.plugin import Plugin
        plugin = Plugin()
        plugin.test_suite_func = 'test_suite'
        self.original_loader = TestLoader()
        self.l = plugin.prepareTestLoader(self.original_loader)
        
    def test_suite(self):

        class Tests(TestCase):
            def test_something(self):
                return

        def test_suite():
            return makeSuite(Tests)
        
        mod = new_module('with_test_suite')
        mod.test_suite = test_suite

        result = self.l.loadTestsFromModule(mod)
        self.assertTrue(isinstance(result, ContextSuite))
        tests = tuple(result)
        self.assertEqual(len(tests), 1)
        test = tests[0]
        self.assertTrue(isinstance(test, NoseTest))
        self.assertTrue(isinstance(test.test, Tests))

    def test_suite_returns_nested(self):

        class Tests(TestCase):
            def test_something(self):
                return

        def test_suite():
            return TestSuite([TestSuite([makeSuite(Tests)])])
        
        mod = new_module('with_test_suite')
        mod.test_suite = test_suite

        result = self.l.loadTestsFromModule(mod)
        self.assertTrue(isinstance(result, ContextSuite))
        tests = tuple(result)
        self.assertEqual(len(tests), 1)
        test = tests[0]
        self.assertTrue(isinstance(test, NoseTest))
        self.assertTrue(isinstance(test.test, Tests))

    def test_suite_returns_something_odd(self):
        class dodgy(object):
            def __repr__(self):
                return '<dodgy>'
        
        def test_suite():
            return [dodgy()]
        
        mod = new_module('with_test_suite')
        mod.test_suite = test_suite

        try:
            self.l.loadTestsFromModule(mod)
        except TypeError, e:
            self.assertEqual(
                str(e),
                "Don't know what to do with <dodgy> "
                "(<class 'nose_fixes.tests.test_collection.dodgy'>)"
                )
        else:
            self.fail('No exception raised!')

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
        self.assertTrue(isinstance(test, NoseTest))
        self.assertEqual(repr(test), 'Test(without_test_suite.test_sweet)')

    def test_config_kept(self):
        self.assertTrue(self.l.config is self.original_loader.config)
