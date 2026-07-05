from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime
import random

from app.database.database import get_db
from app.models.observation_sessions import ObservationSession
from app.models.photo_detections import Detection

router = APIRouter(prefix="/api/sessions", tags=["Sessions"])


@router.post("")
def create_session(db: Session = Depends(get_db)):
    today_str = datetime.now().strftime("%Y-%m-%d")
    session_name = f"Sesi Pengamatan - {today_str}"
    
    new_session = ObservationSession(
        session_name=session_name,
        status="IN_PROGRESS"
    )
    
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    return new_session


@router.post("/{session_id}/detect")
def upload_and_detect_photo(
    session_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    # Mock data generasi
    semi_ripe = random.randint(1, 5)
    nearly_ripe = random.randint(1, 5)
    ripe = random.randint(1, 5)
    confidence = round(random.uniform(0.75, 0.95), 2)
    
    # Path mock
    original_path = f"uploads/{file.filename}"
    processed_path = f"uploads/processed_{file.filename}"
    
    # Simpan ke tabel detections
    new_detection = Detection(
        session_id=session_id,
        original_image=original_path,
        processed_image=processed_path,
        semi_ripe_count=semi_ripe,
        nearly_ripe_count=nearly_ripe,
        ripe_count=ripe,
        average_confidence=confidence
    )
    
    db.add(new_detection)
    db.commit()
    db.refresh(new_detection)
    
    return {
        "status": "success",
        "session_id": session_id,
        "semi_ripe": semi_ripe,
        "nearly_ripe": nearly_ripe,
        "ripe": ripe,
        "confidence": confidence,
        "boxes": [
            {"box": [50, 50, 150, 200], "label": "ripe"}
        ]
    }
