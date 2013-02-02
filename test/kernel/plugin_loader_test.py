from hk2.kernel.plugin_loader import FilePluginLoader

import os
import sys
import unittest

#===========================================================

MODULE_PATH = sys.modules[__name__].__file__
CUR_DIR = os.path.dirname(os.path.relpath(MODULE_PATH))

def cd(dir):
    return os.path.join(CUR_DIR, dir)

#===========================================================

class PluginLoaderTest(unittest.TestCase):
    def testGetPlugins(self):
        plugin_dirs = map(cd, ['contracts', 'test_plugin_1'])

        pl = FilePluginLoader(plugin_dirs)
        plugins = set(pl.getPlugins())
        self.assertSetEqual(plugins, set(plugin_dirs))

    def testScanPlugins(self):
        plugin_dirs = map(cd, ['contracts', 'test_plugin_1'])

        pl = FilePluginLoader(plugin_dirs)
        m, c, s = pl.scanPlugins()
        self.assertEqual(len(m), 2)
        self.assertEqual(len(c), 1)
        self.assertEqual(len(s), 1)

        import contracts.serializer
        import test_plugin_1.str_serializer
        self.assertSetEqual(set(m), {contracts.serializer, test_plugin_1.str_serializer})
        self.assertEqual(c[0], contracts.serializer.ISerializer)
        self.assertEqual(s[0], test_plugin_1.str_serializer.StrSerializer)

        self.assertEqual(s[0]().serialize(10), '10')
