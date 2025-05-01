""" "Custom JSON encoder for Pydantic objects"""

from json import JSONEncoder
from json import dumps

from pydantic import BaseModel


class PydanticJSONEncoder(JSONEncoder):
    """Custom JSON encoder for Pydantic objects"""

    def default(self, o: object):
        """Encode Pydantic objects"""
        if isinstance(o, BaseModel):
            return o.model_dump()
        return None


def custom_serializer(obj):
    """Serialize Pydantic objects"""
    return dumps(obj, cls=PydanticJSONEncoder)
