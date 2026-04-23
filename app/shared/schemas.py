from pydantic import BaseModel, Field

class CreateLeads(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    contact: str = Field(max_length=32, description="Номер телефона или Telegram username")
    text: str | None = None