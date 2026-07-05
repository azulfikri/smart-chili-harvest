from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.database import Base


class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(Integer, ForeignKey("sessions.id"))

    original_image = Column(String)

    processed_image = Column(String)

    semi_ripe_count = Column(Integer)

    nearly_ripe_count = Column(Integer)

    ripe_count = Column(Integer)

    average_confidence = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship(
        "ObservationSession",
        back_populates="detections"
    )