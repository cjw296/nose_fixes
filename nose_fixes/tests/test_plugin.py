from nose.config import Config
from optparse import OptionParser
from unittest import TestCase

class Tests(TestCase):

    def setUp(self):
        from nose_fixes.plugin import Plugin
        self.plugin = Plugin()
        
    def test_enabled(self):
        self.assertTrue(self.plugin.enabled)

    def test_suite_defined(self):
        self.assertEqual(self.plugin.name, 'nose_fixes')

    def _parse_args(self, *args):
        parser = OptionParser()
        self.plugin.addOptions(parser)
        options, args = parser.parse_args(list(args))
        self.plugin.configure(options, Config())
        
    def test_suite_name_default(self):
        self._parse_args()
        self.assertEqual(self.plugin.test_suite_func, 'test_suite')
    
    def test_suite_name_override(self):
        self._parse_args('--test-suite-func=foo')
        self.assertEqual(self.plugin.test_suite_func, 'foo')

    def test_show_docstrings_default(self):
        self._parse_args()
        self.assertFalse(self.plugin.show_docstrings)

    def test_hide_docstrings_override(self):
        self._parse_args('--show-docstrings')
        self.assertTrue(self.plugin.show_docstrings)
