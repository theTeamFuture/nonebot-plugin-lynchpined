from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""
    lynchpined_group:list = []
    lynchpined_user:list = []
    class Config:
        extra = "ignore"
