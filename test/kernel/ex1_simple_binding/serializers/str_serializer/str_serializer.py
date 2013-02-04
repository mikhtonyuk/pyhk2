from hk2.annotations import Service
from hk2.injection import inject
from hk2.kernel import Habitat

from test.kernel.ex1_simple_binding.interfaces import ISerializer

#===========================================================

@Service()
class StrSerializer(ISerializer):

    @inject(Habitat)
    def __init__(self, habitat):
        pass

    def serialize(self, obj):
        return str(obj)
