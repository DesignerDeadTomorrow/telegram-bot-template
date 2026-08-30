from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Базовая модель."""

    model_config = ConfigDict(
        populate_by_name=True, use_enum_values=True, from_attributes=True
    )
