import pandas as pd
from typing import List, Optional

from pydantic import BaseModel
from langchain_core.messages import BaseMessage


class State(BaseModel):
    df: Optional[pd.DataFrame] = None
    label: Optional[str] = None 
    history: List[BaseMessage]