from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    QueryableAttribute,
    joinedload,
    selectin_polymorphic,
    selectinload,
)

import libqcanvas.database.types as db


class DataMonolith:
    def __init__(
        self,
        courses: Sequence[db.Course],
        resources: Sequence[db.Resource],
        terms: Sequence[db.Term],
    ):
        self.courses = sorted(courses, key=lambda x: x.name)
        self.resources = self._create_resource_map(resources)
        self.terms = terms

    @staticmethod
    def _create_resource_map(resources):
        return {resource.id: resource for resource in resources}

    @staticmethod
    async def create(session: AsyncSession) -> "DataMonolith":
        def _load_course_content_type(
            attribute: QueryableAttribute, content_type: type[db.AnyContentItem]
        ):
            return selectinload(attribute).options(
                selectinload(content_type.resources),
                selectinload(content_type.dead_resources),
                joinedload(content_type.course),
            )

        eager_load_resources = [
            joinedload(db.Resource.course),
            selectin_polymorphic(db.Resource, [db.PanoptoResource]),
        ]
        eager_load_terms = joinedload(db.Term.courses)
        eager_load_courses = [
            selectinload(db.Course.modules).options(
                joinedload(db.Module.course),
                selectinload(db.Module.pages).joinedload(db.Page.module),
            ),
            selectinload(db.Course.resources).options(*eager_load_resources),
            _load_course_content_type(db.Course.assignments, db.Assignment),
            _load_course_content_type(db.Course.messages, db.Message),
            _load_course_content_type(db.Course.pages, db.Page),
            selectinload(db.Course.term).joinedload(db.Term.courses),
            selectinload(db.Course.assignment_groups).options(
                joinedload(db.AssignmentGroup.course),
                selectinload(db.AssignmentGroup.assignments).joinedload(
                    db.Assignment.group
                ),
            ),
        ]

        query = select(db.Course).options(*eager_load_courses)
        courses = (await session.scalars(query)).all()
        query = select(db.Resource).options(*eager_load_resources)
        resources = (await session.scalars(query)).all()
        query = select(db.Term).options(eager_load_terms)
        terms = (await session.scalars(query)).unique().all()

        return DataMonolith(courses=courses, resources=resources, terms=terms)
