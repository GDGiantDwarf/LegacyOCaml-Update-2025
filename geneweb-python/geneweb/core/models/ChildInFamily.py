from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from geneweb.core.models.alchemyBase import Base


class ChildInFamily(Base):
    __tablename__ = "children_in_family"

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    family_id = Column(Integer, ForeignKey("families.id"), nullable=False)
    relation_type = Column(String, nullable=True)

    child = relationship("Person", foreign_keys=[person_id])
    family = relationship("Family", foreign_keys=[family_id])
