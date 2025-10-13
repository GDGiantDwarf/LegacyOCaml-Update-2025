from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from geneweb.core.models.alchemyBase import Base

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    event_type = Column(String, nullable=False)
    date = Column(Date, nullable=True)
    place = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=True)
    family_id = Column(Integer, ForeignKey('families.id'), nullable=True)
    source_id = Column(Integer, ForeignKey('sources.id'), nullable=True)

    person = relationship("Person")
    family = relationship("Family")
    source = relationship("Source")

