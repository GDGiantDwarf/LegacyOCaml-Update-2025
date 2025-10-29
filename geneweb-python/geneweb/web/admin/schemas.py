from pydantic import BaseModel, Field, constr

BaseName = constr(pattern=r"^[A-Za-z0-9_-]{1,64}$")


class BaseCreate(BaseModel):
    name: BaseName = Field(..., description="New base name")


class BaseRename(BaseModel):
    new_name: BaseName = Field(..., description="Target base name")
