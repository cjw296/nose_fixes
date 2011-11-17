from imp import new_module
from nose.case import Test
from nose.core import TestProgram
from nose.loader import TestLoader
from nose.plugins import PluginTester 
from nose_fixes.plugin import Plugin
from unittest import TestCase, makeSuite

class Tests(TestCase):

    def setUp(self):
        self.plugin = Plugin()
        
    def test_prepareTestResult_sets_descriptions(self):
        thing = object()
        self.plugin.show_docstrings = thing
        class FakeResult(object):
            def __init__(self):
                self.descriptions = None
        result = FakeResult()
        self.plugin.prepareTestResult(result)
        self.assertEqual(result.descriptions, thing)

class FunctionalMixin(PluginTester):

    plugins = [Plugin()]
    activate = ''
    args = ['-v']

    def makeSuite(self):
        class TC(TestCase):
            def test_name0(self):
                'confusing output!'
                pass
            def test_name1(self):
                'confusing output!'
                self.fail()
        return makeSuite(TC)
    
class TestHideDocStrings(FunctionalMixin, TestCase):

    def test(self):
        self.assertFalse('confusing output!' in self.output)
        self.assertTrue('name0' in self.output)
        self.assertTrue('name1' in self.output)

class TestShowDocStrings(FunctionalMixin, TestCase):

    activate = '--show-docstrings'

    def test(self):
        self.assertTrue('confusing output!' in self.output)
        self.assertFalse('name0' in self.output)
