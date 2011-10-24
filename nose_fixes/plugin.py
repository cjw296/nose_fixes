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

    name = 'nose_collect'

    enabled = True
    
    def options(self, parser, env):
        pass
    
    def prepareTestLoader(self, loader):
        return BetterLoader()
