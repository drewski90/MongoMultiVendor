from bson import ObjectId as oid
import graphene as gp
from datetime import datetime
from graphql.language.ast import IntValue

class MediaList(gp.List):
    
    @staticmethod
    def serialize(value):
        if value:
            return [i.url for i in value]

class Media(gp.Scalar):
    '''converts media reference to url'''

    @staticmethod
    def serialize(value):
        if value:
            return value.url

class ObjectId(gp.Scalar):
    '''Object Id Scalar'''

    @staticmethod
    def serialize(value):
        return str(value)

    @staticmethod
    def parse_literal(node, _variables=None):
        if isinstance(node.value, str):
            return oid(node.value)

    @staticmethod
    def parse_value(value):
        return oid(value)

class Date(gp.Scalar):
    '''DateTime Scalar Description'''

    @staticmethod
    def serialize(value):
        return int(value.timestamp())

    @staticmethod
    def parse_literal(node, _variables=None):
        if isinstance(node.value, str):
            return datetime.fromtimestamp(node.value)

    @staticmethod
    def parse_value(value):
        return datetime.fromtimestamp(value)

class BigInt(gp.Scalar):


    @staticmethod
    def coerce_int(value):
        try:
            num = int(value)
        except ValueError:
            try:
                num = int(float(value))
            except ValueError:
                return None
        return num

    serialize = coerce_int
    parse_value = coerce_int

    @staticmethod
    def parse_literal(ast):
        if isinstance(ast, IntValue):
            return int(ast.value)