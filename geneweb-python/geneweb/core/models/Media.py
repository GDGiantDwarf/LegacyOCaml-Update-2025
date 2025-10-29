from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from geneweb.core.models.alchemyBase import Base


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True)
    file_path = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    linked_person_id = Column(Integer, ForeignKey("persons.id"), nullable=True)
    linked_event_id = Column(Integer, ForeignKey("events.id"), nullable=True)

    person = relationship("Person")
    event = relationship("Event")
