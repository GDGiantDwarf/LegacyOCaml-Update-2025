from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Person(Base):
    __tablename__ = 'persons'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    gender = Column(String(1), nullable=True)
    birth_date = Column(Date, nullable=True)
    death_date = Column(Date, nullable=True)
    birth_place = Column(String, nullable=True)
    death_place = Column(String, nullable=True)
    occupation = Column(String, nullable=True)
    notes = Column(Text, nullable=True)



