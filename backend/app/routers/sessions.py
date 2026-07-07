from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
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

import shutil
import os
import uuid

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
    
    os.makedirs("uploads", exist_ok=True)
    
    # Path mock - gunakan UUID agar nama file unik (mencegah overwriting/caching)
    unique_id = str(uuid.uuid4())[:8]
    ext = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
    safe_filename = f"{unique_id}.{ext}"
    
    original_path = f"uploads/{safe_filename}"
    processed_path = f"uploads/processed_{safe_filename}"
    
    # Simpan file yang diupload ke disk
    with open(original_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Copy file original sebagai mock untuk "processed_image"
    shutil.copy(original_path, processed_path)
    
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
    
    total_buah = semi_ripe + nearly_ripe + ripe
    persen_semi_ripe = (semi_ripe / total_buah) * 100 if total_buah > 0 else 0
    persen_nearly_ripe = (nearly_ripe / total_buah) * 100 if total_buah > 0 else 0
    persen_ripe = (ripe / total_buah) * 100 if total_buah > 0 else 0
    
    return {
        "status": "success",
        "session_id": session_id,
        "semi_ripe": semi_ripe,
        "nearly_ripe": nearly_ripe,
        "ripe": ripe,
        "persen_semi_ripe": persen_semi_ripe,
        "persen_nearly_ripe": persen_nearly_ripe,
        "persen_ripe": persen_ripe,
        "confidence": confidence,
        "boxes": [
            {"box": [50, 50, 150, 200], "label": "ripe"}
        ]
    }


@router.post("/{session_id}/finalize")
def finalize_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(ObservationSession).filter(ObservationSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Sesi tidak ditemukan")
        
    detections = db.query(Detection).filter(Detection.session_id == session_id).all()
    if not detections:
        raise HTTPException(status_code=400, detail="Belum ada data deteksi pada sesi ini")
        
    n_semi = sum(d.semi_ripe_count for d in detections if d.semi_ripe_count)
    n_nearly = sum(d.nearly_ripe_count for d in detections if d.nearly_ripe_count)
    n_ripe = sum(d.ripe_count for d in detections if d.ripe_count)
    n_total = n_semi + n_nearly + n_ripe
    
    if n_total == 0:
        raise HTTPException(status_code=400, detail="Total objek cabai terdeteksi adalah 0, tidak bisa dikalkulasi")
        
    p_semi = (n_semi / n_total) * 100
    p_nearly = (n_nearly / n_total) * 100
    p_ripe = (n_ripe / n_total) * 100
    
    hrs = (p_semi * 0.2) + (p_nearly * 0.6) + (p_ripe * 1.0)
    
    if hrs >= 80:
        harvest_status = "Siap Panen"
        recommendation = "Pemetikan disarankan segera dilakukan untuk menjaga kualitas optimal buah cabai di lahan."
        shelf_life = 3
    elif hrs >= 60:
        harvest_status = "Hampir Siap Panen"
        recommendation = "Lakukan monitoring lanjutan dalam 2-3 hari ke depan sebelum melakukan pemanenan massal."
        shelf_life = 5
    else:
        harvest_status = "Belum Siap Panen"
        recommendation = "Buah cabai didominasi fase awal pematangan. Pemanenan belum disarankan."
        shelf_life = 7
        
    session.hrs = hrs
    session.harvest_status = harvest_status
    session.recommendation = recommendation
    session.estimated_shelf_life = shelf_life
    session.total_semi_ripe = n_semi
    session.total_nearly_ripe = n_nearly
    session.total_ripe = n_ripe
    session.status = "COMPLETED"
    session.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(session)
    
    return session


@router.get("")
def get_sessions(db: Session = Depends(get_db)):
    sessions = db.query(ObservationSession)\
                 .filter(ObservationSession.status == "COMPLETED")\
                 .order_by(desc(ObservationSession.created_at))\
                 .all()
                 
    result = []
    for session in sessions:
        thumbnail = None
        if session.detections and len(session.detections) > 0:
            thumbnail = f"http://127.0.0.1:8000/{session.detections[0].processed_image}"
            
        session_dict = {
            "id": session.id,
            "session_name": session.session_name,
            "status": session.status,
            "sample_quality": session.sample_quality,
            "hrs": session.hrs,
            "harvest_status": session.harvest_status,
            "estimated_shelf_life": session.estimated_shelf_life,
            "total_semi_ripe": session.total_semi_ripe,
            "total_nearly_ripe": session.total_nearly_ripe,
            "total_ripe": session.total_ripe,
            "recommendation": session.recommendation,
            "created_at": session.created_at,
            "completed_at": session.completed_at,
            "thumbnail_image": thumbnail
        }
        result.append(session_dict)
        
    return result


@router.get("/{session_id}")
def get_session_detail(session_id: int, db: Session = Depends(get_db)):
    session = db.query(ObservationSession).filter(ObservationSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Sesi tidak ditemukan")
        
    return {
        "id": session.id,
        "session_name": session.session_name,
        "status": session.status,
        "sample_quality": session.sample_quality,
        "hrs": session.hrs,
        "harvest_status": session.harvest_status,
        "estimated_shelf_life": session.estimated_shelf_life,
        "total_semi_ripe": session.total_semi_ripe,
        "total_nearly_ripe": session.total_nearly_ripe,
        "total_ripe": session.total_ripe,
        "recommendation": session.recommendation,
        "created_at": session.created_at,
        "completed_at": session.completed_at,
        "detections": session.detections
    }


@router.delete("/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(ObservationSession).filter(ObservationSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Sesi tidak ditemukan")
        
    try:
        # Hapus deteksi yang terkait dengan session ini (manual cascade)
        db.query(Detection).filter(Detection.session_id == session_id).delete()
        
        # Hapus session
        db.delete(session)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Gagal menghapus data dari database: {str(e)}")
        
    return {
        "status": "success", 
        "message": f"Sesi pengamatan dengan ID {session_id} berhasil dihapus permanen."
    }
