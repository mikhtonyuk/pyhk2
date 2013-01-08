
#===========================================================

def create_all_extensions(ep):
    """ Returns generator of (extension, instance) tuples for specified extension points """
    inst = ((ext, ep.InstantiateExtension(ext)) for ext in ep.Extensions())
    return (i for i in inst if i[1] is not None)

#===========================================================

def dump_plugin_graph(mgr):
    """ Dumps plugin graph to string """
    
    res = ''
    for _, pl in mgr.Plugins().iteritems():
        res += '[%s]\n' % (pl.Name())
        for ep in pl.ExtensionPoints():
            res += '  * %s\n' % (ep.Name())
            for ex in ep.Extensions():
                res += '     + %s (%s)\n' % (ex.Extender().Name(), ex.Class())
    return res

#===========================================================
