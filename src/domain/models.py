from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import core_schema
from typing import List, Optional, Any
from bson import ObjectId

# Custom type for ObjectId using Pydantic v2's __get_pydantic_core_schema__
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        """
        Return a Pydantic CoreSchema with validation and serialization logic.
        Handles validation from string/ObjectId and serialization to string.
        """
        # Validator: Accepts ObjectId instance or a valid string representation
        from_input_schema = core_schema.chain_schema(
            [
                core_schema.union_schema(
                    [
                        core_schema.is_instance_schema(ObjectId),
                        core_schema.str_schema(),
                    ],
                    custom_error_type='ObjectIdError',
                    custom_error_message='Input should be a valid ObjectId string or instance',
                ),
                core_schema.no_info_plain_validator_function(cls.validate_object_id),
            ]
        )

        return core_schema.json_or_python_schema(
            # Schema for JSON representation: string
            json_schema=core_schema.str_schema(),
            # Schema for Python representation: uses the validation logic
            python_schema=from_input_schema,
            # Serialization: convert ObjectId to string for JSON
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: str(instance),
                info_arg=False,
                # return_type=str, # Removed invalid argument
                when_used='json-unless-none', # Use str for JSON, ObjectId otherwise
            ),
        )

    @classmethod
    def validate_object_id(cls, v: Any) -> ObjectId:
        """Validate that the input is a valid ObjectId."""
        if isinstance(v, ObjectId):
            return v
        if ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError(f"'{v}' is not a valid ObjectId")

class Pieza(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None, description="MongoDB document ObjectID")
    id_pieza: int = Field(..., alias="id") # Renombrado para evitar conflicto con _id
    nombre: str
    descripcion: str
    foto: str
    modelos_compatibles: List[str]
    estado: str
    precio: float
    informacion_adicional: Optional[str] = None
    id_vendedor: int

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True # Still needed for Pydantic to accept the custom PyObjectId type
        json_encoders = {
            ObjectId: str # Keep this for any direct ObjectId usage if necessary, though PyObjectId handles its own
        }
        json_schema_extra = {
            "example": {
                "id_pieza": 11,
                "nombre": "Kit de Embrague",
                "descripcion": "Este kit de embrague de alto rendimiento es la solución ideal para aplicaciones deportivas o de alto rendimiento. Fabricado con componentes premium, incluye un plato, un disco y un rodamiento de primera calidad, capaces de soportar hasta 400 Nm de par motor. Gracias a su diseño avanzado, este kit de embrague ofrece una mayor durabilidad y un funcionamiento más suave y preciso, brindando una experiencia de conducción deportiva sin renunciar a la fiabilidad.",
                "foto": "https://example.com/kit-embrague.jpg",
                "modelos_compatibles": [
                    "Mazda MX-5 2016-2020",
                    "Hyundai Genesis Coupe 2016-2020"
                ],
                "estado": "Nuevo",
                "precio": 299.99,
                "informacion_adicional": "Plato, disco y rodamiento premium, apto para 400 Nm de par.",
                "id_vendedor": 321
            }
        }