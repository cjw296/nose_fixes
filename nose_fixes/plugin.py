from nose.plugins import Plugin as NosePlugin
from nose.loader import TestLoader

class BetterLoader(TestLoader):

    def __init__(self, test_suite_func):
        super(BetterLoader, self).__init__()
        self.test_suite_func = test_suite_func
        
    def loadTestsFromModule(self, module, path=None, discovered=False):
        suite_func = getattr(module, self.test_suite_func, None)
        if suite_func is not None:
            return suite_func()
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
        return BetterLoader(self.test_suite_func)

    def prepareTestResult(self, result):
        result.descriptions = self.show_docstrings
