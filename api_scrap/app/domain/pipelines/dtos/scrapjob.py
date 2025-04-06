from pydantic import BaseModel, Field

class ScrapJobSummaryInputDto(BaseModel):
    website: str
    query: str
    location: str
    loop: int = Field(default=1)

class ScrapJobDetailInputDto(BaseModel):
    url: str
    website: str
