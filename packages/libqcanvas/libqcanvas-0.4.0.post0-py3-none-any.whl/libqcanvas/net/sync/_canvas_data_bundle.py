from dataclasses import dataclass
from typing import List

from libqcanvas_clients.canvas import Announcement

from libqcanvas.gql_queries import Course
from libqcanvas.net.canvas import CourseMailItem, PageWithContent


@dataclass
class CanvasDataBundle:
    """
    A CanvasDataBundle is a collection of various data retrieved from canvas
    """

    courses: List[Course]
    pages: List[PageWithContent]
    messages: List[CourseMailItem | Announcement]
    course_panopto_folders: dict[str, str]
