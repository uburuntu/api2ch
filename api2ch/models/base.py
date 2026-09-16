from pydantic import BaseModel, ConfigDict


class Base(BaseModel):
    """Base for the evolving upstream response models."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)
