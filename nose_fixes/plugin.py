from logging import getLogger
from unittest import TestCase, TestSuite
from os.path import exists, splitext

from nose.plugins import Plugin as NosePlugin
from nose.loader import TestLoader

logger = getLogger('nose_fixes')

class BetterLoader(TestLoader):

    def __init__(self, test_suite_func, config):
        super(BetterLoader, self).__init__(config)
        self.test_suite_func = test_suite_func

    def loadTestsFromModule(self, module, path=None, discovered=False):
        module_path = getattr(module, '__file__', None)
        if module_path:
            expected_py_path = splitext(module_path)[0]+'.py'
            if not exists(expected_py_path):
                print (module_path, expected_py_path)
                logger.warn('Ignoring orphaned compiled module: %s', module_path)
                return self.suiteClass([])
        # print (module, module, path)
        suite_func = getattr(module, self.test_suite_func, None)
        if suite_func is not None:
            to_process = list(suite_func())
            suite = self.suiteClass([])
            for entity in to_process:
                if isinstance(entity, TestCase):
                    suite.addTest(entity)
                elif isinstance(entity, TestSuite):
                    to_process.extend(entity)
                else:
                    raise TypeError(
                        "Don't know what to do with %r (%r)" % (
                            entity, type(entity)
                            ))
            return suite
        
        return super(BetterLoader, self).loadTestsFromModule(
            module, path, discovered
            )
    
class Plugin(NosePlugin):

    name = 'nose_fixes'

    enabled = True
    
    def options(self, parser, env):
        parser.add_option("--test-suite-func", action="store",
                          dest="test_suite_func",
                          default='test_suite',
                          help="A function in modules that will return a TestSuite. "
                               "Defaults to 'test_suite'.")
        parser.add_option('--show-docstrings', dest='show_docstrings',
                          action='store_true', default=False,
                          help='Allow docstrings to be displayed as test '
                          'descriptions.')
    
    def configure(self, options, config):
        self.test_suite_func = options.test_suite_func
        self.show_docstrings = options.show_docstrings
        
    def prepareTestLoader(self, loader):
        return BetterLoader(self.test_suite_func, loader.config)

    def prepareTestResult(self, result):
        result.descriptions = self.show_docstrings
