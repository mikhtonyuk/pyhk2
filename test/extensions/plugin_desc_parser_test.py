from hk2.extensions.impl.plugin_desc_parser import PluginDescParser

from hk2.extensions import EPParam
from hk2.utils.version import Version

import unittest
from StringIO import StringIO

#===========================================================

sample_config = '''
plugin = {
    'name' : 'Sample plugin',
    'version' : '0.0.1',
    'author' : 'sergeym',
    'provides' : [
        {
            'point' : 'residents',
            'interface' : 'my_plugin.IResident',
            'params': {
                'priority' : EPParam.Optional
            }
        }
    ],
    'extends' : [
        {
            'point' : 'hk2.extensions::start_listeners',
            'class' : 'my_plugin.MyStarter',
            'params' : {
                'priority' : 20
            }
        }
    ]
}'''

#===========================================================

class TestEnum(unittest.TestCase):
    def testDescription(self):
        config = "plugin = { 'name' : 'Sample plugin', 'version' : '0.0.1', 'author' : 'sergeym' }"
        desc = PluginDescParser.parse(StringIO(config))
        self.assertEqual('Sample plugin', desc.name)
        self.assertEqual(desc.version, Version('0.0.1'))
        self.assertEqual('sergeym', desc.author)
    
    def testRaisesOnUnknownParams(self):
        config = "plugin = { 'name' : 'Sample plugin', 'asdf' : 'asdf' }"
        self.assertRaises(Exception, lambda: PluginDescParser.parse(StringIO(config)) )
    
    def testProvides(self):
        desc = PluginDescParser.parse(StringIO(sample_config))
        self.assertEqual(len(desc.provides), 1)
        
        p = desc.provides[0]
        self.assertEqual(p.name, 'residents')
        self.assertEqual(p.interface, 'my_plugin.IResident')
        self.assertDictEqual(p.params, { 'priority' : EPParam.Optional })
    
    def testExtends(self):
        desc = PluginDescParser.parse(StringIO(sample_config))
        self.assertEqual(len(desc.extends), 1)
        
        p = desc.extends[0]
        self.assertEqual(p.name, 'hk2.extensions::start_listeners')
        self.assertEqual(p.clazz, 'my_plugin.MyStarter')
        self.assertDictEqual(p.params, { 'priority' : 20 })
