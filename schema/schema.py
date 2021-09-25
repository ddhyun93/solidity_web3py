from pydantic import BaseModel


class Account(BaseModel):
    voter: str