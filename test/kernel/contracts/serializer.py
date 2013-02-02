from hk2.types import interface
from hk2.annotations import Contract

#===========================================================

@Contract()
@interface
class ISerializer(object):
    def serialize(self, obj):
        """Returns obj serialized to string"""
