from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from geneweb.core.models.alchemyBase import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=True)

    person = relationship("Person")
    event = relationship("Event")
