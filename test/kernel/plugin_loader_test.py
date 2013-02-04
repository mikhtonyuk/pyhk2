from hk2.kernel import FilePluginLoader

import os
import pickle
import unittest

#===========================================================

PROJ_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

#===========================================================

class PluginLoaderTest(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.dirname(__file__))

    def testGetPlugins(self):
        pl = FilePluginLoader()
        pl.addAllInDir(os.path.normpath('ex1_simple_binding/serializers'))

        plugins = set(pl.getPlugins())
        expected = map(os.path.normpath, ['ex1_simple_binding/serializers/str_serializer', 'ex1_simple_binding/serializers/pickle_serializer'])
        self.assertSetEqual(plugins, set(expected))

    def testScanPlugins(self):
        pl = FilePluginLoader()
        pl.setImportRoot(PROJ_DIR)
        pl.addAllInDir('ex1_simple_binding/serializers')
        pl.addModuleFile('ex1_simple_binding/interfaces.py')

        m, c, s = pl.scanPlugins()
        self.assertEqual(len(m), 3)
        self.assertEqual(len(c), 1)
        self.assertEqual(len(s), 2)

        import test.kernel.ex1_simple_binding.interfaces as ifc
        import test.kernel.ex1_simple_binding.serializers.str_serializer.str_serializer as sstr
        import test.kernel.ex1_simple_binding.serializers.pickle_serializer.pickle_serializer as spik

        self.assertSetEqual(set(m), {ifc, sstr, spik})

        self.assertEqual(c[0], ifc.ISerializer)
        self.assertSetEqual(set(s), {sstr.StrSerializer, spik.PickleSerializer})
