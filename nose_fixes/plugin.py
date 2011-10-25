from nose.plugins import Plugin as NosePlugin
from nose.loader import TestLoader

class BetterLoader(TestLoader):

    def loadTestsFromModule(self, module, path=None, discovered=False):
        suite_func = getattr(module, 'test_suite', None)
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
    
    def configure(self, options, config):
        self.test_suite_func = options.test_suite_func
        
    def prepareTestLoader(self, loader):
        return BetterLoader()
