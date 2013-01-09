
#===========================================================

def create_all_extensions(ep):
    """ Returns generator of (extension, instance) tuples for specified extension points """
    inst = ((ext, ep.InstantiateExtension(ext)) for ext in ep.Extensions())
    return (i for i in inst if i[1] is not None)

#===========================================================

def dump_plugin_graph(mgr):
    """ Dumps plugin graph to string """
    
    res = ''
    for pl in mgr.plugins().itervalues():
        res += '[%s]\n' % (pl.name())
        for ep in pl.extensionPoints():
            res += '  * %s\n' % (ep.name())
            for ex in ep.extensions():
                res += '     + %s (%s)\n' % (ex.plugin().name(), ex.className())
    return res

#===========================================================
