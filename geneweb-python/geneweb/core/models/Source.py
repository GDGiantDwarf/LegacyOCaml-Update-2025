from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from geneweb.core.models.alchemyBase import Base


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    reference = Column(String, nullable=False)
    type = Column(String, nullable=False)
    repository = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
