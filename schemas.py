from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class ActionItem(BaseModel):
    task: str
    assignee: Optional[str] = "Unassigned"
    priority: Optional[str] = "Medium"

class MeetingAnalysis(BaseModel):
    category: Literal["meeting", "tutorial", "news", "presentation"] = Field(
        default="meeting",
        description="Classification of the audio or video content."
    )
    summary: str = Field(
        description="Concise overview of the content, highlighting key points."
    )
    key_takeaways: List[str] = Field(
        default_factory=list,
        description="Key tips, lessons, or educational highlights."
    )
    key_decisions: List[str] = Field(
        default_factory=list,
        description="Concrete decisions made during discussions."
    )
    action_items: List[ActionItem] = Field(
        default_factory=list,
        description="Assigned tasks or follow-up actions."
    )