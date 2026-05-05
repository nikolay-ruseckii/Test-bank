from pydantic import BaseModel as BM


from pydantic import BaseModel as PydanticBaseModel, ConfigDict

class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(populate_by_name=True)