from pynamodb import models, attributes, constants
from uuid import uuid4, UUID
from datetime import datetime, timezone

def current_datetime():
    return datetime.now(timezone.utc)


class UUIDAttribute(attributes.Attribute[UUID]):
    """
    PynamoDB attribute for UUIDs. These are backed by DynamoDB unicode (`S`) types.
    Credits: https://github.com/lyft/pynamodb-attributes
    """

    # This tells PynamoDB that the attribute is stored in DynamoDB as a string
    # attribute
    attr_type = constants.STRING

    def serialize(self, value: UUID) -> str:
        return str(value)

    def deserialize(self, value: str) -> UUID:
        return UUID(value)


class Question(models.Model):
    id = UUIDAttribute(hash_key=True, default_for_new=uuid4)
    question_text = attributes.UnicodeAttribute()
    pub_date = attributes.UTCDateTimeAttribute(attr_name="date_published", default_for_new=current_datetime)

    class Meta:
        table_name = 'questions'
        host = "http://localhost:8000"


class Choice(models.Model):
    id = UUIDAttribute(hash_key=True, default_for_new=uuid4)
    question = UUIDAttribute(range_key=True)
    choice_text = attributes.UnicodeAttribute()
    votes = attributes.NumberAttribute(default=0)

    class Meta:
        table_name = 'choices'
        host = "http://localhost:8000"
