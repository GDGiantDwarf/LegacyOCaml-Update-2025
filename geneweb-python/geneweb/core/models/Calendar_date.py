from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class CalendarDate(Base):
    __tablename__ = "calendar_dates"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=True)
    event_type = Column(String, nullable=False)  # "birth", "death", "marriage", etc.
    
    # Date grégorienne (référence)
    gregorian_year = Column(Integer, nullable=False)
    gregorian_month = Column(Integer, nullable=False)
    gregorian_day = Column(Integer, nullable=False)
    gregorian_date = Column(Date, nullable=False)
    
    # Date julienne
    julian_year = Column(Integer, nullable=True)
    julian_month = Column(Integer, nullable=True)
    julian_day = Column(Integer, nullable=True)
    julian_day_number = Column(Integer, nullable=True)  # Jour julien astronomique
    
    # Date républicaine française
    french_year = Column(Integer, nullable=True)
    french_month = Column(String, nullable=True)
    french_day = Column(Integer, nullable=True)
    
    # Date hébraïque
    hebrew_year = Column(Integer, nullable=True)
    hebrew_month = Column(String, nullable=True)
    hebrew_day = Column(Integer, nullable=True)
    
    # Relation
    person = relationship("Person", back_populates="calendar_dates")

    def __repr__(self):
        return f"<CalendarDate(event={self.event_type}, gregorian={self.gregorian_year}-{self.gregorian_month}-{self.gregorian_day})>"