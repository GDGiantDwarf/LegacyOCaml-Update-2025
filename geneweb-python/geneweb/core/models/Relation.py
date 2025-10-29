from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from geneweb.core.models.alchemyBase import Base


class Relation(Base):
    __tablename__ = "relations"

    id = Column(Integer, primary_key=True)
    person1_id = Column(Integer, ForeignKey("persons.id"))
    person2_id = Column(Integer, ForeignKey("persons.id"))
    relation_type = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=True)

    person1 = relationship("Person", foreign_keys=[person1_id])
    person2 = relationship("Person", foreign_keys=[person2_id])
    event = relationship("Event", foreign_keys=[event_id])
