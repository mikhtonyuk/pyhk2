from hk2.annotations import Service
from test.kernel.contracts.serializer import ISerializer

#===========================================================

@Service()
class StrSerializer(ISerializer):
    def serialize(self, obj):
        return str(obj)
