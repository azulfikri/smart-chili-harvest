from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.database import Base


class ObservationSession(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)

    session_name = Column(String, nullable=False)

    status = Column(String, default="IN_PROGRESS")

    sample_quality = Column(String, nullable=True)

    hrs = Column(Float, nullable=True)

    harvest_status = Column(String, nullable=True)

    estimated_shelf_life = Column(Integer, nullable=True)

    total_semi_ripe = Column(Integer, nullable=True)

    total_nearly_ripe = Column(Integer, nullable=True)

    total_ripe = Column(Integer, nullable=True)

    recommendation = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    completed_at = Column(DateTime, nullable=True)


    detections = relationship(
        "Detection",
        back_populates="session",
        cascade="all, delete-orphan"
    )