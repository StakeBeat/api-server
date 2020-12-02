from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.sql import func


@as_declarative()
class BaseModel:
    """
    Warning: server_default will will create properly for new tables, but will not be modified in
    an automigrate.  We need to set default until all old tables are migrated.
    """

    __abstract__ = True

    created_at = Column(
        DateTime,
        nullable=False,
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        server_default=func.current_timestamp(),
    )
