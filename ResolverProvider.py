"""
File: ResolverProvider.py
Purppose:
Copywrite: Sendwell 2013
"""

import DomainResolver
import AtomicInteger

class ResolverProvider(object):
        
    def getResolver(self):
        self.cnt.increase()
        cntVal = self.cnt.get()
        resolver = DomainResolver.DomainResolver()
        ### resolver = self.resolvers.pop(cntVal % len(self.resolvers))
        return resolver
        
    def __init__(self):
        self.cnt = AtomicInteger.AtomicInteger(0)
        self.resolvers = []