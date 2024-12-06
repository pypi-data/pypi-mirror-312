from dataclasses import dataclass

import libqcanvas.database.types as db


# @dataclass
class ContentItemReference:
    def __init__(self, content: db.AnyContentItem):
        self.id = content.id
        self.resource_link_table = db.RESOURCE_LINK_TABLES[content.__tablename__]


@dataclass
class ExtractedResources:
    content: ContentItemReference
    resources: list[db.Resource]
    invisible_resources: list[db.Resource]
