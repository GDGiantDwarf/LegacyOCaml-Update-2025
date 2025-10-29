from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from geneweb.core.models.alchemyBase import Base


class Family(Base):
    __tablename__ = "families"

    id = Column(Integer, primary_key=True)
    spouse1_id = Column(Integer, ForeignKey("persons.id"))
    spouse2_id = Column(Integer, ForeignKey("persons.id"))
    marriage_date = Column(Date, nullable=True)
    marriage_place = Column(String, nullable=True)
    divorce_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)

    spouse1 = relationship("Person", foreign_keys=[spouse1_id])
    spouse2 = relationship("Person", foreign_keys=[spouse2_id])
