from typing import Annotated, Any, Callable
from bson import ObjectId
from pydantic_core import core_schema


class _ObjectIdPydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_from_str(input_value: str) -> ObjectId:
            try:
                return ObjectId(input_value)
            except Exception:
                raise ValueError(f"Invalid ObjectId format: {input_value}")

        return core_schema.union_schema(
            [
                core_schema.is_instance_schema(ObjectId),  # Direct instance validation
                core_schema.no_info_plain_validator_function(validate_from_str),  # From string
            ],
            serialization=core_schema.to_string_ser_schema(),  # Serialize as string
        )

PydanticObjectId = Annotated[ObjectId, _ObjectIdPydanticAnnotation]
