from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from libqcanvas.gql_queries import Course, Module


@dataclass
class PageWithContent:
    q_id: str
    name: Optional[str]
    updated_at: Optional[datetime]
    created_at: Optional[datetime]
    module: Module
    course: Course
    position: int
    content: Optional[str] = None
    is_locked: bool = False
    unlock_at: Optional[datetime] = None
    lock_at: Optional[datetime] = None
