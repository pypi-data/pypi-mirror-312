from datetime import datetime
from typing import List, Optional, Sequence

from sqlalchemy import Column, ForeignKey, String, Table, and_
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    declared_attr,
    mapped_column,
    relationship,
)

from libqcanvas.database.types.module_page_type import ModulePageType
from libqcanvas.database.types.resource_download_state import ResourceDownloadState
from libqcanvas.database.types.resource_life_state import ResourceLinkState


class Base(DeclarativeBase, MappedAsDataclass, init=False):
    pass


RESOURCE_LINK_TABLES: dict[str, Table] = {}
"""
A dictionary for the tables used to link resources to pages/assignments/etc. 
The key is the __tablename__ of the content type.

Columns
-------
content_item_id : str
    The ID of the page, assignment, etc
resource_id : str
    The ID of the resource
link_state : str
    A value from ResourceLinkState. It must be a string, so remember to use .name
"""


def get_resource_link_table_name(content_table_name: str) -> str:
    return f"{content_table_name}_resource_links"


def _create_resource_link_table(content_table_name: str) -> Table:
    # WARNING: When renaming the columns of this table, you must also update them everywhere else! Since type hinting is not
    # available with this older style of declaration, the IDE doesn't know about them.
    result = Table(
        get_resource_link_table_name(content_table_name),
        Base.metadata,
        Column(
            "content_item_id",
            ForeignKey(f"{content_table_name}.id"),
            primary_key=True,
        ),
        Column("resource_id", ForeignKey("resources.id"), primary_key=True),
        Column("link_state", String, default=ResourceLinkState.ACTIVE.name),
    )

    RESOURCE_LINK_TABLES[content_table_name] = result
    return result


class ContentGroup:
    @property
    def items(self) -> "AnyContentItem":
        """
        Retrieve the content items in this content group.
        """
        raise NotImplementedError()


class ModificationDate:
    last_modification_date: Mapped[datetime]


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[str] = mapped_column(primary_key=True)

    course_id: Mapped[str] = mapped_column(ForeignKey("courses.id"))
    course: Mapped["Course"] = relationship(back_populates="resources")

    url: Mapped[str]
    file_name: Mapped[str]
    discovery_date: Mapped[datetime]
    file_size: Mapped[Optional[int]] = mapped_column(default=None)
    download_state: Mapped[ResourceDownloadState] = mapped_column(
        default=ResourceDownloadState.NOT_DOWNLOADED
    )
    download_error_message: Mapped[Optional[str]] = mapped_column(default=None)

    polymorphic_type: Mapped[str]

    __mapper_args__ = {
        "polymorphic_on": "polymorphic_type",
        "polymorphic_identity": "resource",
    }


class CourseContentItem:
    id: Mapped[str] = mapped_column(primary_key=True)

    course_id: Mapped[str] = mapped_column(ForeignKey("courses.id"))

    @declared_attr
    @classmethod
    def course(cls) -> Mapped["Course"]:
        return relationship(back_populates=cls.__tablename__)

    name: Mapped[str]
    body: Mapped[Optional[str]]
    creation_date: Mapped[datetime]

    @declared_attr
    @classmethod
    def resources(cls) -> Mapped[List["Resource"]]:
        if hasattr(cls, "__tablename__"):
            link_table = RESOURCE_LINK_TABLES[cls.__tablename__]
        else:
            raise Exception("Expected class to have __tablename__. Did you forget?")

        return relationship(
            secondary=link_table,
            primaryjoin=and_(
                link_table.c.content_item_id == cls.id,
                link_table.c.link_state == ResourceLinkState.ACTIVE.name,
            ),
            overlaps="dead_resources, course_content",
            order_by=Resource.discovery_date,
        )

    @declared_attr
    @classmethod
    def dead_resources(cls) -> Mapped[List["Resource"]]:
        if hasattr(cls, "__tablename__"):
            link_table = RESOURCE_LINK_TABLES[cls.__tablename__]
        else:
            raise Exception("Expected class to have __tablename__. Did you forget?")

        return relationship(
            secondary=link_table,
            primaryjoin=and_(
                link_table.c.content_item_id == cls.id,
                link_table.c.link_state == ResourceLinkState.RESIDUAL.name,
            ),
            overlaps="resources, course_content",
            order_by=Resource.discovery_date,
        )

    unlock_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    lock_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    can_view: Mapped[bool]


class PanoptoResource(Resource):
    __tablename__ = "panopto_resources"

    id: Mapped[str] = mapped_column(ForeignKey("resources.id"), primary_key=True)

    duration_seconds: Mapped[int]
    recording_date: Mapped[datetime]

    # Panopto/Canvas have this stupid "custom_context_delivery" which is a pain in the ass because it has nothing to do
    # with the actual ID of the video. In this case, this object's id may not be useful in any way (thanks painopto),
    # but delivery_id will always be the true ID of the video.
    # !!!! It has been observed that different "custom_context_delivery"s CAN link to the same video !!!!
    delivery_id: Mapped[str]

    __mapper_args__ = {"polymorphic_identity": "panopto_resource"}


class Assignment(Base, CourseContentItem, ModificationDate):
    __tablename__ = "assignments"
    _create_resource_link_table(__tablename__)

    due_date: Mapped[Optional[datetime]]
    score: Mapped[Optional[float]]
    max_score: Mapped[Optional[float]]
    position: Mapped[int]

    group_id: Mapped[str] = mapped_column(ForeignKey("assignment_groups.id"))
    group: Mapped["AssignmentGroup"] = relationship(back_populates="assignments")


class AssignmentGroup(Base, ContentGroup):
    __tablename__ = "assignment_groups"

    id: Mapped[str] = mapped_column(primary_key=True)

    course_id: Mapped[str] = mapped_column(ForeignKey("courses.id"))
    course: Mapped["Course"] = relationship(back_populates="assignment_groups")

    name: Mapped[str]
    assignments: Mapped[List[Assignment]] = relationship(
        back_populates="group",
        order_by=Assignment.position,
        cascade="save-update, merge, delete",
    )
    group_weight: Mapped[int]
    position: Mapped[int]

    @property
    def items(self) -> Sequence[CourseContentItem]:
        return self.assignments


class Message(Base, CourseContentItem):
    """
    Used for announcements and course mail
    """

    __tablename__ = "messages"
    _create_resource_link_table(__tablename__)

    sender_name: Mapped[str]
    has_been_read: Mapped[bool]


class Page(Base, CourseContentItem, ModificationDate):
    __tablename__ = "pages"
    _create_resource_link_table(__tablename__)

    module_id: Mapped[str] = mapped_column(ForeignKey("modules.id"))
    module: Mapped["Module"] = relationship(back_populates="pages")
    position: Mapped[int]
    page_type: Mapped[ModulePageType]


class Module(Base, ContentGroup):
    __tablename__ = "modules"

    id: Mapped[str] = mapped_column(primary_key=True)

    course_id: Mapped[str] = mapped_column(ForeignKey("courses.id"))
    course: Mapped["Course"] = relationship(back_populates="modules")

    name: Mapped[str]
    pages: Mapped[List["Page"]] = relationship(
        back_populates="module",
        order_by=Page.position,
        cascade="save-update, merge, delete",
    )
    position: Mapped[int]

    @property
    def items(self) -> Sequence[CourseContentItem]:
        return self.pages


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[str] = mapped_column(primary_key=True)

    name: Mapped[str]
    modules: Mapped[List["Module"]] = relationship(
        back_populates="course",
        order_by=Module.position,
        cascade="save-update, merge, delete",
    )
    assignment_groups: Mapped[List[AssignmentGroup]] = relationship(
        back_populates="course",
        order_by=AssignmentGroup.position,
        cascade="save-update, merge, delete",
    )
    resources: Mapped[List[Resource]] = relationship(
        back_populates="course",
        order_by=Resource.discovery_date,
        cascade="save-update, merge, delete",
    )
    panopto_folder_id: Mapped[Optional[str]]
    term_id: Mapped[str] = mapped_column(ForeignKey("terms.id"))
    term: Mapped["Term"] = relationship(back_populates="courses")

    # The names of the following 3 fields MUST match the __tablename__ of the classes they relate to
    messages: Mapped[List[Message]] = relationship(
        viewonly=True,
        primaryjoin=id == Message.course_id,
        order_by=Message.creation_date,
    )
    assignments: Mapped[List[Assignment]] = relationship(
        viewonly=True,
        primaryjoin=id == Assignment.course_id,
        order_by=Assignment.due_date,
    )
    pages: Mapped[List[Page]] = relationship(
        viewonly=True,
        primaryjoin=id == Page.course_id,
        order_by=Page.creation_date,
    )


class Term(Base):
    __tablename__ = "terms"

    id: Mapped[str] = mapped_column(primary_key=True)

    start_date: Mapped[Optional[datetime]]
    end_date: Mapped[Optional[datetime]]
    name: Mapped[str]
    courses: Mapped[List["Course"]] = relationship(
        back_populates="term",
        order_by=Course.name,
        cascade="save-update, merge, delete",
    )

    def __hash__(self):
        return (
            hash(self.id)
            ^ hash(self.start_date)
            ^ hash(self.end_date)
            ^ hash(self.name)
        )


AnyContentGroup = ContentGroup
AnyContentItem = Page | Message | Assignment
