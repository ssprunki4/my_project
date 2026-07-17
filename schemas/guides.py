from pydantic import BaseModel, ConfigDict
from schemas.categories import CategoryCreate


class GuideCreate(BaseModel):
    name: str
    category_id: str
    url: str | None = None
class GuideUpdate(GuideCreate):
    name: str | None = None
    category_id: str | None = None
    url: str | None = None

class GuideResponse(BaseModel):
    name:str
    category_id: str
    url: str | None
    id: str
    category: CategoryCreate
    model_config = ConfigDict(from_attributes=True)
