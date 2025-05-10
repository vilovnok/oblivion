import pandas as pd
from typing import List, Optional

from pydantic import BaseModel
from langchain_core.messages import BaseMessage


class State(BaseModel):
    df: Optional[object] = None
    label: Optional[str] = None 
    partition: Optional[bool] = None
    history: List[BaseMessage]