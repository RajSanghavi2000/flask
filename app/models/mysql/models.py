from sqlalchemy import Column, MetaData, DateTime, VARCHAR, UniqueConstraint
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

__all__ = ['Person']

meta = MetaData()
Base = declarative_base(metadata=meta)


class Person(Base):
    """Sample table for micro service template"""

    __tablename__ = "person"
    id = Column(BIGINT(display_width=20, unsigned=True), primary_key=True, nullable=False, autoincrement=True)
    first_name = Column(VARCHAR(50), nullable=False)
    last_name = Column(VARCHAR(50), nullable=False)
    email = Column(VARCHAR(50), nullable=False)
    phone = Column(VARCHAR(10), nullable=False)
    created_at = Column(DateTime(3), nullable=False)
    created_by = Column(BIGINT(display_width=20, unsigned=True))
    modified_at = Column(DateTime(3), nullable=True, default=None)
    modified_by = Column(BIGINT(display_width=20, unsigned=True), nullable=True, default=None)
    UniqueConstraint(email, name="idx_person_email")
