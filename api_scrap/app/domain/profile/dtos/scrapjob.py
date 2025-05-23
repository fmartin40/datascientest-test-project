from pydantic import BaseModel, Field

class ScrapJobSummaryInputDto(BaseModel):
    source: str
    query: str
    location: str
    loop: int = Field(default=1)

class ScrapJobDetailInputDto(BaseModel):
    url: str
    source: str
