from typing import Hashable

class ConnectionRule:
    def __init__(self, *fields: Hashable):
        self._fields = frozenset(fields)
        self.hash_value = hash(self._fields)
    
    def __repr__(self):
        return str(self._fields)

    def __hash__(self):
        return self.hash_value
        
    def __eq__(self, other):
        return self.hash_value == other.hash_value