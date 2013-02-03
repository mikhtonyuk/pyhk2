from hk2.annotations import Service

from test.kernel.ex1_simple_binding.interfaces import ISerializer

#===========================================================

@Service()
class StrSerializer(ISerializer):
    def serialize(self, obj):
        return str(obj)
