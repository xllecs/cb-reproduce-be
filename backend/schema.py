import graphene

from cole_buxton_be.cb_types import CBQueryType
from cole_buxton_be.cb_mutations import CBMutationType

class Query(CBQueryType, graphene.ObjectType):
  pass

class Mutation(CBMutationType, graphene.ObjectType):
  pass

schema = graphene.Schema(query=Query, mutation=Mutation)
