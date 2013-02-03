from hk2.annotations import Service

from test.kernel.ex1_simple_binding.interfaces import ISerializer

import pickle

#===========================================================

@Service()
class PickleSerializer(ISerializer):
    def serialize(self, obj):
        return pickle.dumps(obj)
