from imp import new_module
from nose.case import Test
from nose.core import TestProgram
from nose.loader import TestLoader
from unittest import TestCase

class Tests(TestCase):

    def setUp(self):
        from nose_fixes.plugin import Plugin
        self.plugin = Plugin()
        
    def test_prepareTestResult_sets_descriptions(self):
        "This test has a docstring"
        # The above is a functional test you can use
        # by running nose with the plugin and making
        # sure the docstring isn't shown by default
        thing = object()
        self.plugin.show_docstrings = thing
        class FakeResult(object):
            def __init__(self):
                self.descriptions = None
        result = FakeResult()
        self.plugin.prepareTestResult(result)
        self.assertEqual(result.descriptions, thing)
