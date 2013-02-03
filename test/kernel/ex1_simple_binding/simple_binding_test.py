from hk2.kernel.file_plugin_loader import FilePluginLoader
from hk2.kernel import Habitat

from test.kernel.ex1_simple_binding.interfaces import ISerializer

import os
import pickle
import unittest

#===========================================================

PROJ_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))

#===========================================================

class SimpleBindingTest(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.dirname(__file__))

    def testSimpleBinding(self):
        pl = FilePluginLoader()
        pl.setImportRoot(PROJ_DIR)
        pl.addAllInDir('serializers')
        pl.addModuleFile('interfaces.py')

        h = Habitat(pl)
        serializers = h.getAllByContract(ISerializer)
        data = map(lambda s: s.serialize(10), serializers)

        self.assertSetEqual(set(data), {'10', pickle.dumps(10)})
