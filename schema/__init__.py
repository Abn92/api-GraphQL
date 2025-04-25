import strawberry
from schema.query import Query

schema = strawberry.Schema(query=Query)
