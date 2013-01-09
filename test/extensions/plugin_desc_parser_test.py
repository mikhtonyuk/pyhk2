from hk2.extensions.impl.declarative import PluginDescParser

from hk2.extensions import ExtParamConstraint
from hk2.utils.version import Version

import unittest
from StringIO import StringIO

#===========================================================

sample_config = '''
plugin = {
    'name' : 'com.acme.example.plugin',
    'desc' : 'Example plugin',
    'version' : '0.0.1',
    'author' : 'sergeym',
    'provides' : [
        {
            'point' : 'residents',
            'interface' : 'my_plugin.IResident',
            'params': {
                'priority' : ExtParamConstraint.Optional
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
        config = "plugin = { 'name' : 'com.acme.example.plugin', 'desc' : 'test desc', 'version' : '0.0.1', 'author' : 'sergeym' }"
        shadow = PluginDescParser.parse(StringIO(config))
        self.assertEqual('com.acme.example.plugin', shadow.name())
        self.assertEqual('test desc', shadow.description())
        self.assertEqual(Version('0.0.1'), shadow.version())
        self.assertEqual('sergeym', shadow.author())
    
    def testRaisesOnUnknownParams(self):
        config = "plugin = { 'name' : 'com.acme.example.plugin', 'asdf' : 'asdf' }"
        self.assertRaises(Exception, lambda: PluginDescParser.parse(StringIO(config)) )
    
    def testProvides(self):
        shadow = PluginDescParser.parse(StringIO(sample_config))
        self.assertEqual(len(shadow.extensionPoints()), 1)
        
        p = shadow.extensionPoints()[0]
        self.assertEqual(p.name(), 'residents')
        self.assertEqual(p.fullName(), 'com.acme.example.plugin::residents')
        self.assertEqual(p.interfaceName(), 'my_plugin.IResident')
        self.assertDictEqual(p.parameters(), { 'priority' : ExtParamConstraint.Optional })
    
    def testExtends(self):
        shadow = PluginDescParser.parse(StringIO(sample_config))
        self.assertEqual(len(shadow.extensions()), 1)
        
        p = shadow.extensions()[0]
        self.assertEqual(p._pointName, 'hk2.extensions::start_listeners')
        self.assertEqual(p.className(), 'my_plugin.MyStarter')
        self.assertDictEqual(p.params, { 'priority' : 20 })
