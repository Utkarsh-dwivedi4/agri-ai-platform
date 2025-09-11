from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func
from .db import Base


class Farmer(Base):
__tablename__ = "farmers"
id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
name = Column(String, nullable=True)
phone = Column(String, unique=True, nullable=False)
language = Column(String, default="en")
created_at = Column(DateTime(timezone=True), server_default=func.now())


class Farm(Base):
__tablename__ = "farms"
id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
farmer_id = Column(UUID(as_uuid=True), ForeignKey('farmers.id'))
name = Column(String)
polygon_json = Column(JSON)
area_ha = Column(Numeric)
created_at = Column(DateTime(timezone=True), server_default=func.now())