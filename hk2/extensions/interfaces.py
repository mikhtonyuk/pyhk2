from hk2.types import interface, enum

#===========================================================

@interface
class IPlugin(object):
    """ Base interface for all plug-ins """
    
    def Shadow(self):
        """ Returns the shadow of this plug-in """
    
    def PluginManager(self):
        """ Returns associated plug-in manager """
    
    def Init(self, plugin_manager, shadow):
        """ Initializes the plug-in """

#===========================================================

@interface
class IExtensionPoint(object):
    """ Extension point all plug-ins can extend """
    
    def Plugin(self):
        """ Returns plug-in shadow of provider """
    
    def Name(self):
        """ Returns name of this extension point """
    
    def FullName(self):
        """ Full name in format plugin_name::ep_name """
    
    def Interface(self):
        """ Returns interface type all extenders should implement """
    
    def Parameters(self):
        """ Returns dictionary of parameters expected by EP """
    
    def Extensions(self):
        """ Returns the list of extensions """
    
    def InstantiateExtension(self, ext):
        """ Creates instance of specified extension
            with all required validation """


#===========================================================

@interface
class IExtension(object):
    """ Extension objects binds extension point
    that is being extended, plug-in that provides an
    extension, and a class that implements point's interface """
    
    def ExtensionPoint(self):
        """ Extension point that is being extended """
    
    def Extender(self):
        """ Plug-in shadow that provides extension """
    
    def Module(self):
        """ Module that defines the implementation class """
    
    def Class(self):
        """ Name of the implementation class """
    
    def FullPath(self):
        """ Full path to the implementation class: "Module::Class" """
    
    def Parameters(self):
        """ Parameter dictionary """

#===========================================================

@interface
class IPluginShadow(object):
    """ Plugin shadow is a proxy object
        it holds all meta-info about plug-in, exported classes,
        extension points it extends and provides """
    
    def Name(self):
        """ Returns name of the plug-in """
    
    def PresentedName(self):
        """ Returns user-friendly name """
    
    def Version(self):
        """ Returns plug-in version """
    
    def GetExtensionPoint(self, shortName):
        """ Searches extension point by short name """
    
    def ExtensionPoints(self):
        """ Returns list of extension points it provides """
    
    def Extensions(self):
        """ List of provided extensions """

#===========================================================

@interface
class IPluginManager(object):
    """ Plugin management system """
    
    def Start(self, args = None):
        """ Starts execution by launching start_listeners """
    
    def Arguments(self):
        """ Returns arguments that were given at startup """
    
    def PluginsDir(self):
        """ Returns plug-in search directory """
    
    def ExtensionPoints(self):
        """ Extension point dict by name """
    
    def Plugins(self):
        """ Plug-in dict by name """
    
    def ServiceRegistry(self):
        """ Returns services registry """

#===========================================================

@interface
class IServiceRegistry(object):
    ''' Simplifies operations on service plugins '''
    
    def GetService(self, interface):
        ''' Returns service instance '''

#===========================================================

class PluginBase(IPlugin):
    """ Basic implementation of IPlugin interface """
    
    def Init(self, plugin_manager, svc_reg, shadow):
        self._shadow = shadow
        self._svc_reg = svc_reg
        self._pluginManager = plugin_manager
    
    def Shadow(self):
        return self._shadow
    
    def PluginManager(self):
        return self._pluginManager
    
    def ServiceRegistry(self):
        return self._svc_reg

#===========================================================
# Plugin description
#===========================================================

class PluginDesc(object):
    """ Implement this interface in plugin.py file so that
        framewor will recognize your plug-in and load its settings
        Required fields:
        - PresentedName - user-friendly name of the plug- in
        - Version - 'maj.min.bld.rev' varsion info
        - Extensions - list of ExtensionDesc
        - ExtensionPoints - list of ExtensionPointDesc """


#===========================================================

@enum
class EPParam:
    (Optional, Mandatory) = range(2)

class ExtensionPointDesc(object):
    """ Describes extension point
        Required fields:
        - Name - short name of the EP
        - Interface - type of the interface
        - Parameters - dict of parameters this EP expects
            { name : EPParam.Optional|EPParam.Mandatory } """

#===========================================================

class ExtensionDesc(object):
    """ Describes provided extension
        Required fields:
        - ExtensionPoint - full name of the target EP
        - Module - name of module that contains implementation
        - Class - name of the class that implements EP's interface
        - Parameters - dict of parameters for EP { name : value } """

#===========================================================
# Extension points
#===========================================================

@interface
class IStartListener(object):
    """ Interface for 'start_listeners' EP """
    
    def Start(self, args = None):
        """ Signals execution start """

#===========================================================

