from mongoengine import (
    Document, 
    EmbeddedDocument,
    EmbeddedDocumentField,
    GenericEmbeddedDocumentField,
    ReferenceField,
    GenericReferenceField,
    ListField,
    SortedListField,
    ObjectIdField,
    IntField
)
from time import time
from bson import ObjectId

def populate_document(document, data_dict):

    def field_value(field, value):

        embedded_field_classes = (
            EmbeddedDocumentField,
            GenericEmbeddedDocumentField,
            ReferenceField,
            GenericReferenceField,
            ObjectIdField
        )

        reference_field_classes = (
            ReferenceField,
            GenericReferenceField,
            ObjectIdField
        )

        embeded_document_classes = (
            Document, 
            EmbeddedDocument
        )

        array_classes = (
            ListField, 
            SortedListField
        )

        if field.__class__ in array_classes:
            if isinstance(field.field, reference_field_classes):
                return field.field.document_type.objects.filter(id__in=value)
            return [
                field_value(field.field, item)
                for item in value
            ]

        if field.__class__ in embedded_field_classes:

            if isinstance(value, embeded_document_classes):
                return value

            elif isinstance(value, dict):
                return field.document_type(**value)
            
            elif isinstance(field, reference_field_classes):
                if issubclass(field.document_type, Document):
                   return field.document_type.objects.get(id=value)
                else:
                    return ObjectId(value)

            else:
                raise Exception(f'Merging error at {field}')

        else:
            return value


    for key, value in data_dict.items():
        value = field_value(document._fields[key], value)
        setattr(document, key, field_value(document._fields[key], value))


    return document