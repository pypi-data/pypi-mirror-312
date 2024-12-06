import logging
from collections import defaultdict
from typing import Sequence

from sqlalchemy import Table, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

import libqcanvas.database.types as db
from libqcanvas.net.resources.scanning.extracted_resources import (
    ContentItemReference,
    ExtractedResources,
)
from libqcanvas.net.sync.canvas_sync_observer import CanvasSyncObservable

_logger = logging.getLogger(__name__)


class ResourceLinker(CanvasSyncObservable):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self._session = session

    async def link_resources(self, extracted_resource_links: list[ExtractedResources]):
        if len(extracted_resource_links) == 0:
            return

        await self._mark_content_links_as_dead(extracted_resource_links)
        await self._link_new_resources_and_restore_active_links(
            extracted_resource_links
        )

    async def _mark_content_links_as_dead(
        self, extracted_resource_links: list[ExtractedResources]
    ):
        table_groups: dict[Table, set] = defaultdict(set)

        for link in extracted_resource_links:
            table_groups[link.content.resource_link_table].add(link.content.id)

        for link_table, page_ids in table_groups.items():
            _logger.debug(
                "Deactivating resource links for %i content items (table=%s)",
                len(page_ids),
                link_table.name,
            )
            stmt = (
                update(link_table)
                .where(link_table.c.content_item_id.in_(page_ids))
                .values(link_state=db.ResourceLinkState.RESIDUAL.name)
            )
            await self._session.execute(stmt)

    async def _link_new_resources_and_restore_active_links(
        self, extracted_resource_links: list[ExtractedResources]
    ):
        for link in extracted_resource_links:
            existing_resource_links = await self._get_existing_content_resource_links(
                link.content
            )
            newly_linked_resources: list[str] = []

            await self._create_links_for_resources(
                existing_resource_links=existing_resource_links,
                extracted_resource_links=link,
                newly_linked_resources=newly_linked_resources,
            )

            await self._create_links_for_invisible_resources(
                existing_resource_links=existing_resource_links,
                extracted_resource_links=link,
                newly_linked_resources=newly_linked_resources,
            )

    async def _create_links_for_resources(
        self,
        existing_resource_links: Sequence[str],
        extracted_resource_links: ExtractedResources,
        newly_linked_resources: list[str],
    ):
        for extracted_resource in extracted_resource_links.resources:
            if extracted_resource.id in existing_resource_links:
                # If a resource is still linked on this page, reactivate the link
                await self._reactivate_existing_resource_link(
                    content_ref=extracted_resource_links.content,
                    resource=extracted_resource,
                )
            # Prevent adding duplicate links (duplicate links have been observed on some pages)
            elif extracted_resource.id not in newly_linked_resources:
                await self._create_resource_link(
                    content_ref=extracted_resource_links.content,
                    resource=extracted_resource,
                )
                newly_linked_resources.append(extracted_resource.id)

                await self._add_resource_to_db_if_new(extracted_resource)

    async def _create_links_for_invisible_resources(
        self,
        existing_resource_links: Sequence[str],
        extracted_resource_links: ExtractedResources,
        newly_linked_resources: list[str],
    ):
        for resource in extracted_resource_links.invisible_resources:
            if (
                resource.id in existing_resource_links
                or resource.id in newly_linked_resources
            ):
                # If the resource was already on the page, or it has just been added, don't add it again
                continue

            await self._create_dead_resource_link(
                content_ref=extracted_resource_links.content, resource=resource
            )
            newly_linked_resources.append(resource.id)
            await self._add_resource_to_db_if_new(resource)

    async def _create_resource_link(
        self, content_ref: ContentItemReference, resource: db.Resource
    ):
        _logger.debug(
            "Linking resource %s (id=%s) to id=%s (table=%s)",
            resource.file_name,
            resource.id,
            content_ref.id,
            content_ref.resource_link_table.name,
        )

        stmt = insert(content_ref.resource_link_table).values(
            content_item_id=content_ref.id, resource_id=resource.id
        )
        await self._session.execute(stmt)

    async def _create_dead_resource_link(
        self, content_ref: ContentItemReference, resource: db.Resource
    ):
        _logger.debug(
            "Linking resource as RESIDUAL for %s (id=%s) to id=%s (table=%s)",
            resource.file_name,
            resource.id,
            content_ref.id,
            content_ref.resource_link_table.name,
        )

        stmt = insert(content_ref.resource_link_table).values(
            content_item_id=content_ref.id,
            resource_id=resource.id,
            link_state=db.ResourceLinkState.RESIDUAL.name,
        )
        await self._session.execute(stmt)

    async def _get_existing_content_resource_links(
        self, content_ref: ContentItemReference
    ) -> Sequence[str]:
        columns = content_ref.resource_link_table.c
        stmt = select(columns.resource_id).where(
            columns.content_item_id == content_ref.id
        )
        return (await self._session.scalars(stmt)).all()

    async def _reactivate_existing_resource_link(
        self, content_ref: ContentItemReference, resource: db.Resource
    ):
        link_table = content_ref.resource_link_table

        _logger.debug(
            "Reactivating resource link for %s (id=%s) to id=%s (table=%s)",
            resource.file_name,
            resource.id,
            content_ref.id,
            content_ref.resource_link_table.name,
        )

        stmt = (
            update(link_table)
            .where(link_table.c.resource_id == resource.id)
            .values(link_state=db.ResourceLinkState.ACTIVE.name)
        )
        await self._session.execute(stmt)

    async def _add_resource_to_db_if_new(self, resource: db.Resource):
        does_not_exist = (await self._session.get(db.Resource, resource.id)) is None

        if does_not_exist:
            _logger.debug("New resource %s (id=%s)", resource.file_name, resource.id)
            self._session.add(resource)
            self.notify_observers_for_updated_item(resource)
